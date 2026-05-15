import time
import json

from config import TOPIC

from utils.rgb import normalize_rgb

def publish_sensor_data(client, sensor):

    lux = sensor.read_lux()

    red_raw, green_raw, blue_raw = (
        sensor.read_rgb_raw()
    )

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

    client.publish(
        TOPIC,
        msg
    )

    print("Published:", msg)