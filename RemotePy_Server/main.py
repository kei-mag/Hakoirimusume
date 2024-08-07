# RemotePy Server v1.1
# For Raspberry Pi Pico W(H)
#
# == How to use ==
# 1. Obtain `UpyIrTx.py` from RemotePy project:
#    https://github.com/meloncookie/RemotePy/raw/main/micropython/RP2040/FromV1_17/UpyIrRx.py
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
from network import STAT_IDLE, STAT_CONNECTING, STAT_WRONG_PASSWORD, STAT_NO_AP_FOUND, STAT_CONNECT_FAIL, STAT_GOT_IP
from UpyIrTx import UpyIrTx
import _thread

# ----------- Configuration -----------
SSID = "your-wifi-ssid"  # TODO: Enter your Wi-Fi SSID
PASSPHRASE = "your-wifi-password"  # TODO: Enter your Wi-Fi Password
IP_ADDRESS = None  # None: DHCP
HOST_NAME = "RemotePyServer"  # None: Default value will be used.
LISTEN_PORT = 80
GPIO_PIN = 3
CODE_DEFINITION_FILE = "codes.json"
# -------------------------------------

print(f"Starting '{__file__}'...")

index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>RemotePy Server</title>
</head>
<body>
    <h1>Failed to load index.html</h1>
    <b>Controlling IR devices via web browser is not available Due to the error occurred during loading index.html.</b><br>
    It is recommend to reboot Raspberry Pi Pico W by plugging out and plugging in the USB cable.<br>
    If the problem persists after rebooting, please contact the administrator.<br>
    API may still be available.
</body>
</html>"""

led = Pin("LED", Pin.OUT)
led.off()
signals = {}
tx_pin = Pin(GPIO_PIN, Pin.OUT)
tx = UpyIrTx(0, tx_pin)  # 0ch

def connect_network():
    global wlan
    if not wlan.isconnected():
        wlan.active(False)
        utime.sleep(1)
        wlan.active(True)
        wlan.connect(SSID, PASSPHRASE)
        print("Connecting to network...", end="")
        while not wlan.isconnected():
            wlan_status = wlan.status()
            if wlan_status in [STAT_CONNECT_FAIL, STAT_NO_AP_FOUND, STAT_WRONG_PASSWORD]:
                print("\n[ERROR] Failed to connect network: ", end="")
                if wlan_status() == STAT_WRONG_PASSWORD:
                    print("Wi-Fi Passphrase is not correct.")
                elif wlan_status() == STAT_NO_AP_FOUND:
                    print(f"No such Wi-Fi access point: '{SSID}'.")
                elif wlan_status() == STAT_CONNECT_FAIL:
                    print(f"Some trouble has occurred while connecting '{SSID}'.")
                while True:
                    # Blink LED rapidly to show failure of Wi-Fi connection
                    led.value(not led.value())
                    utime.sleep(0.1)
                    # Do nothing more.
            elif wlan_status() == STAT_GOT_IP:
                continue
            elif wlan_status() == STAT_CONNECTING:
                led.value(not led.value())
                print(".", end="")
                utime.sleep(1)
            else:
                print(f"\n[INFO] wlan.status()={wlan_status}")
                print("Connecting to network...", end="")
        print("\nConnected!")
    ifconfig = wlan.ifconfig()
    if IP_ADDRESS:
        print("----- Network Information -----")
        print(f"IP Address: {ifconfig[0]}")
        print(f"Netmask: {ifconfig[1]}")
        print(f"Default Gateway: {ifconfig[2]}")
        print(f"Name Server: {ifconfig[3]}")
        print("-------------------------------")
        print("Changing IP address...", end="\t")
        wlan.ifconfig((IP_ADDRESS, ifconfig[1], ifconfig[2], ifconfig[3]))
        ifconfig = wlan.ifconfig()
        if ifconfig[0] == IP_ADDRESS:
            print("Done!")
        else:
            print("FAILED.")
    print("----- Network Information -----")
    print(f"IP Address: {ifconfig[0]}")
    print(f"Netmask: {ifconfig[1]}")
    print(f"Default Gateway: {ifconfig[2]}")
    print(f"Name Server: {ifconfig[3]}")
    print("-------------------------------")
    led.on()


if HOST_NAME:
    network.hostname("HOST_NAME")
print("Hostname: ", network.hostname())
wlan = network.WLAN(network.STA_IF)
mac_addr = str(wlan.config('mac').hex())
print("Wi-Fi MAC address: ", "-".join([mac_addr[x:x+2] for x in range(0, len(mac_addr), 2)]))
del mac_addr

# Prepare index.html
try:
    print("Loading 'index.html'...")
    index_html = open("index.html", "r", encoding="UTF-8").read()
    try:
        print(f"Loading '{CODE_DEFINITION_FILE}'...")
        command_list_html, signals = parse_codes_json(CODE_DEFINITION_FILE)
        index_html = index_html.replace("{{COMMAND_LIST}}", command_list_html)
    except Exception as e:
        print("[ERROR]", e)
        index_html = create_error_html(e, f"loading {CODE_DEFINITION_FILE}")
except Exception as e:
    print("[ERROR]", e)
index_html = index_html.replace("\r\n", "").replace("\n", "").replace(" ", "")

connect_network()
_thread.start_new_thread(connect_network, ())

# Prepare HTTP server
addr = socket.getaddrinfo(wlan.ifconfig()[0], LISTEN_PORT)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
print(f"Start listening at {wlan.status()[0]}:{LISTEN_PORT}")

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
            response = f"Command '{path[1:]}' was sent."
            print(response)
        else:
            code = "404 Not Found"
            response = f"404 Not Found\n No such command is defined: '{path[1:]}'."
        # print(response)
        cl.send("HTTP/1.0 %s\r\nContent-type: %s\r\n\r\n" % (code, ct))
        cl.send(response)
        cl.close()
    except KeyboardInterrupt:
        break
s.close()
