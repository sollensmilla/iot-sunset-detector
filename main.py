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

print("WiFi connected:", wifi.ifconfig())

# -------------------
# MQTT
# -------------------

BROKER = "broker.emqx.io"
TOPIC = b"lnu/iot/ss226uk/sensor"

client = MQTTClient(
    "esp32-ss226uk",
    BROKER,
    keepalive=60
)

client.connect()

print("Connected to MQTT broker!")

# -------------------
# I2C / SENSOR
# -------------------

i2c = I2C(
    0,
    scl=Pin(22),
    sda=Pin(21),
    freq=100000
)

ADDR = 0x44

print("I2C scan:", i2c.scan())

# -------------------
# REGISTERS
# -------------------

REG_CH0 = 0x00
REG_CH1 = 0x01
REG_CH2 = 0x02
REG_CH3 = 0x03

REG_CONFIG = 0x0A

# -------------------
# SENSOR CONFIG
# -------------------

try:

    # Continuous conversion mode
    config = bytes([0x32, 0x30])

    i2c.writeto_mem(
        ADDR,
        REG_CONFIG,
        config
    )

    print("Sensor configured")

except Exception as e:

    print("Sensor init error:", e)

time.sleep(2)

# -------------------
# READ RAW CHANNEL
# -------------------

def read_channel_raw(register):

    data = i2c.readfrom_mem(
        ADDR,
        register,
        3
    )

    b0 = data[0]
    b1 = data[1]
    b2 = data[2]

    exponent = (b0 >> 4) & 0x0F

    mantissa = (
        ((b0 & 0x0F) << 16)
        | (b1 << 8)
        | b2
    )

    raw = mantissa * (2 ** exponent)

    return raw

# -------------------
# NORMALIZE RGB
# -------------------

def normalize_rgb(r, g, b):

    # Compress dynamic range
    r = int(r ** 0.5)
    g = int(g ** 0.5)
    b = int(b ** 0.5)

    # Manual balancing
    r = r * 1.0
    g = g * 4.0
    b = b * 1.5

    max_val = max(r, g, b)

    if max_val == 0:
        return 0, 0, 0

    r8 = int((r / max_val) * 255)
    g8 = int((g / max_val) * 255)
    b8 = int((b / max_val) * 255)

    return r8, g8, b8

# -------------------
# LOOP
# -------------------

while True:

    try:

        # Read channels
        ch0 = read_channel_raw(REG_CH0)

        red_raw = read_channel_raw(REG_CH1)
        green_raw = read_channel_raw(REG_CH2)
        blue_raw = read_channel_raw(REG_CH3)

        # Convert lux
        lux = round(ch0 * 0.00215, 2)

        # Normalize RGB
        r, g, b = normalize_rgb(
            red_raw,
            green_raw,
            blue_raw
        )

        payload = {
            "timestamp": time.time(),

            "lux": lux,

            "red_raw": red_raw,
            "green_raw": green_raw,
            "blue_raw": blue_raw,

            "r": r,
            "g": g,
            "b": b
        }

        msg = json.dumps(payload)

        client.publish(TOPIC, msg)

        print("Published:", msg)

    except Exception as e:

        print("Error:", e)

        try:
            client.connect()
            print("MQTT reconnected")
        except:
            print("Reconnect failed")

    time.sleep(2)