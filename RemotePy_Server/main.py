# RemotePy Server v1.0
# For Raspberry Pi Pico W(H)
#
# == How to use ==
# 1. Obtain `UpyIrTx.py` from https://raw.githubusercontent.com/meloncookie/RemotePy/main/micropython/RP2040/FromV1_17/UpyIrTx.py
# 2. Copy `main.py`, `htmlutil.py`, `index.html` and `UpyIrTx.py` to your Raspberry Pi Pico W(H).
# 3. Create `codes.json` by `cgir rec` command (https://github.com/IndoorCorgi/cgir)
#    or create it by yourself with original format.
# 4. Copy `codes.json` to your Raspberry Pi Pico W(H).
# 5. Run `main.py` or turn on your Raspberry Pi Pico W(H) without PC.
#
# Please see README.md for more detailed information.

import socket

import network
import utime
from htmlutil import create_error_html, parse_codes_json
from machine import Pin
from network import STAT_CONNECT_FAIL, STAT_NO_AP_FOUND, STAT_WRONG_PASSWORD
from UpyIrTx import UpyIrTx

# ----------- Configuration -----------
SSID = "your-wifi-ssid"  # TODO: Enter your Wi-Fi SSID
PASSPHRASE = "your-wifi-password"  # TODO: Enter your Wi-Fi Password
IP_ADDRESS = None  # None: DHCP
LISTEN_PORT = 80
GPIO_PIN = 3
CODE_DEFINITION_FILE = "codes.json"
# -------------------------------------

index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>RemotePy Server</title>
</head>
<body>
    <h1>Failed to load index.html</h1>
    <b>Because of an error during loading template html file, controlling ir devices via web browser is not available.</b><br>
    It is recommend to reboot Raspberry Pi Pico W by plug out and plug in the USB cable.<br>
    If the problem persists after rebooting, please contact the administrator.<br>
    API may still be available.
</body>
</html>"""

led = Pin("LED", Pin.OUT)
led.off()
signals = {}
tx_pin = Pin(GPIO_PIN, Pin.OUT)
tx = UpyIrTx(0, tx_pin)  # 0ch

# Prepare index.html
try:
    index_html = open("index.html", "r", encoding="UTF-8").read()
    try:
        command_list_html, signals = parse_codes_json(CODE_DEFINITION_FILE)
        index_html = index_html.replace("{{COMMAND_LIST}}", command_list_html)
    except Exception as e:
        print("[ERROR]", e)
        index_html = create_error_html(e, f"loading {CODE_DEFINITION_FILE}")
except Exception as e:
    pass
# index_html = index_html.replace("\n", "").replace(" ", "")

# Connect to network
wlan = network.WLAN(network.STA_IF)
if not wlan.isconnected():
    wlan.active(False)
    utime.sleep(1)
    wlan.active(True)
    wlan.connect(SSID, PASSPHRASE)
    print("Connecting to network...", end="")
    while not wlan.isconnected():
        if wlan.status() in [STAT_WRONG_PASSWORD, STAT_NO_AP_FOUND, STAT_CONNECT_FAIL]:
            print("Failed to connect network\nwlan.status(): ", wlan.status())
            print(
                f"(STAT_WRONG_PASSWORD={STAT_WRONG_PASSWORD}, STAT_NO_AP_FOUND={STAT_NO_AP_FOUND}, STAT_CONNECT_FAIL={STAT_CONNECT_FAIL})"
            )
            while True:
                led.value(not led.value())
                utime.sleep(0.1)
        led.value(not led.value())
        print(".", end="")
        utime.sleep(1)
    print("Connected!")
wlan_status = wlan.ifconfig()
if IP_ADDRESS:
    print("----- Network Information -----")
    print(f"IP Address: {wlan_status[0]}")
    print(f"Netmask: {wlan_status[1]}")
    print(f"Default Gateway: {wlan_status[2]}")
    print(f"Name Server: {wlan_status[3]}")
    print("-------------------------------")
    print("Changing IP address...", end="\t")
    wlan.ifconfig((IP_ADDRESS, wlan_status[1], wlan_status[2], wlan_status[3]))
    wlan_status = wlan.ifconfig()
    if wlan_status[0] == IP_ADDRESS:
        print("Done!")
    else:
        print("FAILED.")
print("----- Network Information -----")
print(f"IP Address: {wlan_status[0]}")
print(f"Netmask: {wlan_status[1]}")
print(f"Default Gateway: {wlan_status[2]}")
print(f"Name Server: {wlan_status[3]}")
print("-------------------------------")
led.on()

# Prepare HTTP server
addr = socket.getaddrinfo(wlan.ifconfig()[0], LISTEN_PORT)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
print(f"Start listening at {wlan_status[0]}:{LISTEN_PORT}")

# Listen to HTTP request
while True:
    try:
        led.on()
        cl, addr = s.accept()
        led.off()
        req = str(cl.recv(1024), "utf-8").split("\r\n")
        # print("----------")
        # print(req)
        # print("----------")
        path = "none"
        for l in req:
            if "GET" in l:
                path = l.split(" ")[1]
                break
        code = "200 OK"
        ct = "text/html"
        if path == "/":
            response = index_html
        elif path == "/favicon.ico":
            response = ""
        elif path[1:] in signals:
            tx.send(signals[path[1:]])
            print(f"command '{path[1:]}' was sent.")
            response = f"""<html><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><body><h1>SUCCESS</h1>Command '{path[1:]}' was sent.<br>
            <button style=\"font-size:20pt;\" onClick=\"location.href='../'\">TOP</button></body></html>"""
        else:
            code = "404 Not Found"
            response = f"""<html><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><body><h1>Not Found</h1>No such command is defined: '{path[1:]}'.<br>
            <button style=\"font-size:20pt;\" onClick=\"location.href='../'\">TOP</button></body></html>"""
        # print(response)
        cl.send("HTTP/1.0 %s\r\nContent-type: %s\r\n\r\n" % (code, ct))
        cl.send(response)
        cl.close()
    except KeyboardInterrupt:
        break
s.close()
