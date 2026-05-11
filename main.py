import network
import time

from secrets import WIFI_SSID, WIFI_PASSWORD

wifi = network.WLAN(network.STA_IF)

wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

print("Connecting to WiFi...")

while not wifi.isconnected():
    time.sleep(1)
    print("Waiting...")

print("Connected!")
print("IP address:", wifi.ifconfig()[0])