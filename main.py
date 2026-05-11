import network
import time
import json

from machine import I2C, Pin
from umqtt.simple import MQTTClient

from secrets import WIFI_SSID, WIFI_PASSWORD

# -------------------
# WIFI
# -------------------

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

print("Connecting to WiFi...")

while not wifi.isconnected():
    time.sleep(1)
    print("Waiting for WiFi...")

print("WiFi connected!")
print("IP:", wifi.ifconfig()[0])

# -------------------
# MQTT
# -------------------

BROKER = "broker.emqx.io"
TOPIC = b"lnu/iot/ss226uk/sensor"

client = MQTTClient(
    client_id="esp32-ss226uk",
    server=BROKER,
    keepalive=60
)

client.connect()

print("Connected to MQTT broker!")

# -------------------
# SENSOR
# -------------------

i2c = I2C(0, scl=Pin(22), sda=Pin(21))

ADDR = 0x44

# Configure sensor
i2c.writeto_mem(ADDR, 0x0A, bytes([0x12, 0x34]))

# -------------------
# LOOP
# -------------------

while True:
    try:
        data = i2c.readfrom_mem(ADDR, 0x00, 2)

        value = (data[0] << 8) | data[1]

        payload = {
            "value": value,
            "timestamp": time.time()
        }

        json_payload = json.dumps(payload)

        client.publish(TOPIC, json_payload)

        print("Published:", json_payload)

    except Exception as e:
        print("Error:", e)

    time.sleep(2)