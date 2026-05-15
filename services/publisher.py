import json

from config import (
    TOPIC,
    MIN_LUX_FOR_CCT     
)

from utils.rgb import normalize_rgb
from utils.cct import estimate_cct
from utils.smoothing import ExponentialSmoother
from utils.time_utils import current_iso_time as current_timestamp

lux_smoother = ExponentialSmoother(0.2)

r_smoother = ExponentialSmoother(0.2)
g_smoother = ExponentialSmoother(0.2)
b_smoother = ExponentialSmoother(0.2)

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

    # Smooth values to reduce noise
    lux = round(
        lux_smoother.update(lux),
        2
    )

    r = int(r_smoother.update(r))
    g = int(g_smoother.update(g))
    b = int(b_smoother.update(b))

    # Ignore unstable CCT in low light
    if lux < MIN_LUX_FOR_CCT:

        cct = None

    else:

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