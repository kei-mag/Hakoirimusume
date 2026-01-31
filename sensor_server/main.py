import datetime
import http.server
import json
import os
import re
import csv
from urllib.parse import parse_qs, urlparse

import imgur

try:
    import tomllib
except ImportError:
    import tomli as tomllib

CONFIG_FILE = "./config.toml"
DASHBOARD_HTML_FILE = "public/dashboard.html"
ACCEPT_ADDR = "0.0.0.0"
ENV_VAL_FORM = re.compile(r"\${(.+)}")

# ----- Default config values -----
port = 80
imgur_client_id = ""
enable_camera = False
i2c_bus = 1
i2c_addr = 0x76
sensor_data_file = "./sensor_data.csv"
log_level = "ALL"
# ---------------------------------

camera = None
bme280 = None

def main():
    global camera, bme280
    os.chdir(os.path.dirname(__file__))
    print("Hakoirimusume Sensor Server (Enhanced)")
    load_config()

    # Initialize Devices
    try:
        from bme280 import BME280
        bme280 = BME280(i2c_bus, i2c_addr)
        print("BME280 initialized.")
    except Exception as e:
        print("BME280 Init Error: ", e)

    if enable_camera:
        try:
            from picamera import PiCamera
            camera = PiCamera()
            print("PiCamera initialized.")
        except Exception as e:
            print("PiCamera Init Error: ", e)

    # Start Server
    server_address = (ACCEPT_ADDR, port)
    try:
        from http.server import ThreadingHTTPServer
        ServerClass = ThreadingHTTPServer
    except ImportError:
        ServerClass = http.server.HTTPServer

    with ServerClass(server_address, CustomHTTPRequestHandler) as httpd:
        print(f"Serving at {ACCEPT_ADDR}:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
    print("Stopped server.")


def dict_get(d, key, default=None):
    keys = key.split(".")
    for k in keys:
        if k in d:
            d = d[k]
        else:
            return default
    return d


def load_config():
    global port, imgur_client_id, enable_camera, i2c_bus, i2c_addr, sensor_data_file, log_level
    try:
        config = tomllib.load(open(CONFIG_FILE, mode="rb"))
        port = replace_env(dict_get(config, "server.port", port))
        imgur_client_id = replace_env(dict_get(config, "imgur.client-id", imgur_client_id))
        enable_camera = dict_get(config, "hardware.pi-camera", enable_camera)
        i2c_bus = dict_get(config, "hardware.bme280.i2c-bus", i2c_bus)
        i2c_addr = dict_get(config, "hardware.bme280.i2c-address", i2c_addr)
        sensor_data_file = replace_env(dict_get(config, "datalog.filepath", sensor_data_file))
        log_level = dict_get(config, "datalog.level", log_level)

        cwd = os.getcwd()
        os.chdir(os.path.dirname(CONFIG_FILE))
        sensor_data_file = os.path.abspath(sensor_data_file)
        os.chdir(cwd)
    except Exception as e:
        print(f"Config load failed: {e}")


def replace_env(value):
    if isinstance(value, str):
        match = ENV_VAL_FORM.search(value)
        if match:
            return ENV_VAL_FORM.sub(os.getenv(match.group(1), ""), value)
    return value


def get_current_iso_timestamp(cur_time=None):
    if cur_time is None:
        # Aware datetime with local timezone
        cur_time = datetime.datetime.now().astimezone()
    else:
        if cur_time.tzinfo is None:
            cur_time = cur_time.astimezone()

    return cur_time.replace(microsecond=0).isoformat()


def write_log(timestamp, temp, hum, press, image_url=None, deletehash=None):
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(sensor_data_file), exist_ok=True)
        with open(sensor_data_file, "a") as file:
            file.write(f"{timestamp},{temp},{hum},{press},{image_url},{deletehash}\n")
    except Exception as e:
        print(f"Log write error: {e}")


def read_history_24h():
    """Read data from the last 24 hours"""
    data = []
    if not os.path.exists(sensor_data_file):
        return data

    try:
        now = datetime.datetime.now().astimezone()
        one_day_ago = now - datetime.timedelta(hours=24)

        # Read file (might be large, but Pi Zero can handle simple CSV read)
        with open(sensor_data_file, "r") as f:
            reader = csv.reader(f)
            # Read all lines (or use seek for optimization if file is > 10MB)
            rows = list(reader)

            # Iterate backwards to find relevant data
            for row in reversed(rows):
                if len(row) < 4: continue
                try:
                    # Parse timestamp
                    ts_str = row[0]
                    dt = datetime.datetime.fromisoformat(ts_str)

                    # Stop if older than 24h
                    if dt < one_day_ago:
                        break

                    # Parse values
                    t = float(row[1]) if row[1] not in ["---", "None"] else None
                    h = float(row[2]) if row[2] not in ["---", "None"] else None
                    p = float(row[3]) if row[3] not in ["---", "None"] else None

                    if t is not None:
                        # Append dict
                        data.append({
                            "ts": dt.timestamp(), # UNIX timestamp for easier JS handling
                            "temp": t,
                            "humid": h,
                            "press": p
                        })
                except ValueError:
                    continue

        # Reverse back to chronological order
        data.reverse()

    except Exception as e:
        print(f"History read error: {e}")

    return data


class CustomHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def _send_response(self, content, content_type="text/html", status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if isinstance(content, str):
            self.wfile.write(content.encode("utf-8"))
        else:
            self.wfile.write(content)

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query, keep_blank_values=True)

        # 1. Dashboard
        if path == "/":
            try:
                with open(DASHBOARD_HTML_FILE, "r", encoding="UTF-8") as file:
                    self._send_response(file.read())
            except Exception as e:
                self._send_response(f"Dashboard Error: {e}", status=500)

        # 2. Static Files (Images)
        elif path.endswith((".jpg", ".jpeg", ".png", ".ico")):
            if ".." in path:
                self.send_error(403)
                return

            # Look in public folder as requested by user
            possible_paths = [
                path.lstrip("/"),
                os.path.join("public", path.lstrip("/")),
                os.path.join("docs", path.lstrip("/"))
            ]

            served = False
            for p in possible_paths:
                if os.path.exists(p) and os.path.isfile(p):
                    try:
                        with open(p, "rb") as f:
                            ext = os.path.splitext(p)[1].lower()
                            mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"
                            self._send_response(f.read(), content_type=mime)
                            served = True
                            break
                    except:
                        pass
            if not served:
                self.send_error(404)

        # 3. API: Current Data
        elif path == "/api/sensor" or path == "/get":
            temp = press = humid = None
            if bme280:
                try:
                    temp, press, humid = bme280.read_data()
                except Exception as e:
                    print("BME280 Read Error: ", e)

            cur_timestamp = get_current_iso_timestamp()
            cur_time_obj = datetime.datetime.now().astimezone()

            content = {
                "time": cur_timestamp,
                "temp": temp,
                "humid": humid,
                "press": press
            }

            if "withcamera" in query:
                content["photo"] = None
                content["deletehash"] = None
                if camera:
                    try:
                        image = camera.capture_bytes()
                        desc = f"T:{temp}, H:{humid}, P:{press}"
                        ret = imgur.upload_as_anonymous(
                            imgur_client_id,
                            image,
                            capture_datetime=cur_time_obj.strftime("%Y/%m/%d %H:%M:%S"),
                            description=desc
                        )
                        if isinstance(ret, tuple) and len(ret) == 2:
                            content["photo"], content["deletehash"] = ret
                    except Exception as e:
                        print("Camera Error: ", e)

                write_log(cur_timestamp, temp, humid, press, content.get("photo"), content.get("deletehash"))
            else:
                if log_level == "ALL":
                    write_log(cur_timestamp, temp, humid, press)

            self._send_response(json.dumps(content), content_type="application/json")

        # 4. API: History (24h)
        elif path == "/api/history":
            try:
                data = read_history_24h()
                self._send_response(json.dumps(data), content_type="application/json")
            except Exception as e:
                self._send_response(json.dumps({"error": str(e)}), content_type="application/json", status=500)

        # 5. API: Shutdown
        elif path == "/api/shutdown":
            self._send_response(json.dumps({"status": "accepted"}), content_type="application/json")
            try:
                os.system("sudo shutdown -h now")
            except Exception as e:
                print(f"Shutdown failed: {e}")

        else:
            self.send_error(404)

    def do_POST(self):
        # Backward compatibility
        if self.path == "/":
            self._send_response("Shutting down...", content_type="text/plain")
            os.system("sudo shutdown -h now")
        elif self.path == "/api/shutdown":
            self._send_response(json.dumps({"status": "accepted"}), content_type="application/json")
            os.system("sudo shutdown -h now")
        else:
            self.send_error(404)

if __name__ == "__main__":
    main()
