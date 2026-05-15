import json

from config import TOPIC

from utils.rgb import normalize_rgb
from utils.cct import estimate_cct
from utils.time_utils import current_iso_time as current_timestamp

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

    cct = estimate_cct(r, g, b)

    payload = {
       "timestamp": current_timestamp(),
       "lux": lux,
       "cct": cct,

       "rgb": {
           "r": r,
           "g": g,
           "b": b
       }
   }

    msg = json.dumps(payload)

    client.publish(
        TOPIC,
        msg
    )

    print("Published:", msg)