from datetime import datetime
import http.server
import os

from bme280 import BME280
from picamera import PiCamera
import imgur
import json

ADDR = "localhost"
PORT = 8000

bme280 = BME280(1, 0x76)
camera = PiCamera()
client_id = os.getenv("IMGUR_CLIENT_ID")


class CustomHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = {}
        data = bme280.read_data()
        if data:
            temp, press, humid = data
            body["temp"], body["humid"], body["press"] = data
        else:
            temp = press = humid = "---"
            body["temp"] = body["humid"] = body["press"] = None
        image = camera.capture_bytes()
        cur_time = datetime.now()
        ret = imgur.upload_as_anonymous(
            client_id,
            image,
            capture_datetime=cur_time.strftime("%Y/%d/%m %H:%M:%S"),
            description=f"Temperature: {temp:.1f}°C, Humidity: {humid:.1f}%, Pressure: {press:.1f}hPa",
        )
        body["photo"] = {}
        if isinstance(ret, tuple) and len(ret) == 2:
            body["photo"]["uri"], body["photo"]["deletehash"] = ret
        else:
            body["photo"]["uri"] = body["photo"]["deletehash"] = None
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())


with http.server.HTTPServer((ADDR, PORT), CustomHTTPRequestHandler) as httpd:
    print("HTTP SERVER for Rabbit's House Report")
    print("serving at port", PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
print("Stopped server.")
