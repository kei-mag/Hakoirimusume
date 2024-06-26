import datetime
import http.server
import json
import os
import re
from urllib.parse import parse_qs, urlparse

import imgur
from ruamel.yaml import YAML

CONFIG_FILE = "./config.yml"
DASHBOARD_HTML_FILE = "templates/dashboard.html"
SHUTTING_DOWN_HTML_FILE = "templates/shutting_down.html"
RELOAD_INTERVAL = 600  # sec.
ACCEPT_ADDR = "0.0.0.0"
ENV_VAL_FORM = re.compile(r"\${(.+)}")

# ----- Default config values -----
port = 80
imgur_client_id = ""
enable_camera = False
i2c_bus = 1
i2c_addr = 0x76
sensor_data_file = "./sensor_data.csv"
# ---------------------------------

dashboard_html = """
<!DOCTYPE HTML>
<html lang="en">
<head>
<title>Hakoirimusume Sensor Server</title>
<body>
<h1>Dashboard is unavailable</h1>
<p>Sensor Dashboard is not currently available</p>
<p>Please check the status of server applications.</p>
</body>
</html>
"""
shutting_down_html = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta http-equiv="refresh" content="10;URL=/">
    <meta charset="UTF-8">
    <title>シャットダウン中</title>
</head>
<body>
        <h1>サーバーをシャットダウンしています</h1>
                <p>シャットダウンには30秒ほどかかります。本体のLEDが消灯するまで電源コードを抜かないでください。</p>
                
            </body>
            </html>
"""
camera = None
bme280 = None


def main():
    global camera, bme280, dashboard_html
    os.chdir(os.path.dirname(__file__))
    print("Hakoirimusume Sensor Server")
    load_config()
    print("----- Running Info -----")
    print(f"Working directory: {os.getcwd}")
    print(f"Loaded config file: {os.path.abspath(CONFIG_FILE)}")
    print(f"Listening PORT: {port}")
    print("Imgur Client ID: *** (Not be shown for security)")
    print(f"Enable Camera: {enable_camera}")
    print(f"BME280 I2C-BUS: {i2c_bus}")
    print(f"BME280 I2C-ADDR: 0x{i2c_addr:x}")
    print(f"Sensor Data File: {os.path.abspath(sensor_data_file)}")
    print("------------------------")
    try:
        from bme280 import BME280
        bme280 = BME280(i2c_bus, i2c_addr)
    except Exception as e:
        print("Error has occurred while initializing BME280. Continue without BME 280: ", e)
    if enable_camera:
        try:
            from picamera import PiCamera
            camera = PiCamera()
        except Exception as e:
            print("Error has occurred while initializing PiCamera. Continue without PiCamera: ", e)
    try:
        with open(DASHBOARD_HTML_FILE, "r", encoding="UTF-8") as file:
            dashboard_html = file.read()
            dashboard_html = dashboard_html.replace("{{INTERVAL}}", str(RELOAD_INTERVAL))
    except Exception as e:
        print("Error has occurred while reading dashboard.html, dashboard is not available: ", e)
    with http.server.HTTPServer((ACCEPT_ADDR, port), CustomHTTPRequestHandler) as httpd:
        print("serving at port", port)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
    print("Stopped server.")


def load_config():
    global port, imgur_client_id, enable_camera, i2c_bus, i2c_addr, sensor_data_file
    yaml=YAML(typ='safe')
    config = yaml.load(open(CONFIG_FILE))
    port = replace_env(config.get("server.port", port))
    imgur_client_id = replace_env(config.get("imgur.client-id", imgur_client_id))
    # if "server" in config:
    #     port = replace_env(config["server"].get("port", port))
    # if "imgur" in config:
    #     imgur_client_id = replace_env(config["imgur"].get("client-id", imgur_client_id))
    if "hardware" in config:
        hardware_config = config["hardware"]
        enable_camera = hardware_config.get("pi-camera", enable_camera)
        i2c_bus = hardware_config.get("bme280.i2c-bus", i2c_bus)
        i2c_addr = hardware_config.get("bme280.i2c-address", i2c_addr)
    #     if "bme280" in hardware_config:
    #         i2c_bus = replace_env(hardware_config["bme280"].get("i2c-bus", i2c_bus))
    #         i2c_addr = replace_env(hardware_config["bme280"].get("i2c-address", i2c_addr))
    #     if "filepath" in config:
    #         sensor_data_file = replace_env(config["filepath"].get("sensor-data", sensor_data_file))
    sensor_data_file = replace_env(config.get("filepath.sensor-data", sensor_data_file))


def replace_env(value):
    if isinstance(value, str):
        match = ENV_VAL_FORM.search(value)
        if match:
            return ENV_VAL_FORM.sub(os.getenv(match.group(1), ""), value)
    return value


class CustomHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def _send_response(self, content, content_type="text/html"):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(content.encode())

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query, keep_blank_values=True)
        if path == "/":
            temp = press = humid = "---"
            if bme280:
                try:
                    temp, press, humid = bme280.read_data()
                except Exception as e:
                    print("Failed to get BME280 data: ", e)
                else:
                    temp = f"{temp:.1f}"
                    humid = f"{humid:.1f}"
                    press = f"{press:.0f}"
            cur_time = datetime.datetime.now()
            content = dashboard_html
            content = content.replace("{{DATETIME}}", cur_time.strftime("%Y/%m/%d %H:%M:%S"))
            content = content.replace("{{TEMP}}", temp)
            content = content.replace("{{HUMID}}", humid)
            content = content.replace("{{PRESS}}", press)
            self._send_response(content)
        elif path == "/get":
            temp = press = humid = None
            if bme280:
                try:
                    temp, press, humid = bme280.read_data()
                except Exception as e:
                    print("Failed to get BME280 data: ", e)
            cur_time = datetime.datetime.now()
            # Calculate offset time without pytz package
            offset = cur_time.replace(tzinfo=datetime.UTC) - datetime.datetime.now(datetime.UTC)
            total_seconds = offset.total_seconds()
            hours, remainder = divmod(total_seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            offset_str = "{:+03d}:{:02d}".format(int(hours), int(minutes))
            timestamp_iso = cur_time.replace(microsecond=0).isoformat() + offset_str
            content = {"time": timestamp_iso}
            content["temp"] = temp
            content["humid"] = humid
            content["press"] = press
            if "withcamera" in query:
                content["photo"] = None
                content["deletehash"] = None
                if camera:
                    try:
                        content["photo"], content["deletehash"] = imgur.upload_as_anonymous(
                            imgur_client_id,
                            camera.capture_bytes(),
                            capture_datetime=cur_time.strftime("%Y/%m%d %H:%M:%S"),
                            description=f"Temperature: {temp:.1f}, Humidity: {humid:.1f}%, Pressure: {press:.1f}hPa",
                        )
                    except Exception as e:
                        print("Failed to get PiCamera data: ", e)
            self._send_response(json.dumps(content), content_type="application/json")
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/":
            content = """
            <!DOCTYPE html>
            <html lang="ja">
            <head>
                <meta http-equiv="refresh" content="10;URL=/">
                <meta charset="UTF-8">
                <title>シャットダウン中</title>
            </head>
            <body>
                <h1>サーバーをシャットダウンしています</h1>
                <p>シャットダウンには30秒ほどかかります。本体のLEDが消灯するまで電源コードを抜かないでください。</p>
                
            </body>
            </html>
            """
            # シャットダウンの処理
            self._send_response(content)
            os.system("sudo shutdown -h now")
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    main()
