import network
import time

from secrets import WIFI_SSID, WIFI_PASSWORD

def connect_wifi():

    wifi = network.WLAN(network.STA_IF)

    wifi.active(True)

    wifi.connect(
        WIFI_SSID,
        WIFI_PASSWORD
    )

    print("Connecting to WiFi...")

    while not wifi.isconnected():

        time.sleep(1)

    print("WiFi connected:", wifi.ifconfig())

    return wifi