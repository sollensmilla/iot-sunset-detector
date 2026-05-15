import time

from lib.wifi import connect_wifi
from lib.mqtt_handler import connect_mqtt
from lib.sensor import ColorSensor

from services.publisher import publish_sensor_data

from utils.time_utils import sync_time

connect_wifi()

sync_time()

client = connect_mqtt()

sensor = ColorSensor()

while True:

    try:

        publish_sensor_data(
            client,
            sensor
        )

    except Exception as e:

        print("Main loop error:", e)

    time.sleep(2)