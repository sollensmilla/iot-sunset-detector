import time

from lib.wifi import connect_wifi
from lib.mqtt_handler import connect_mqtt
from lib.sensor import ColorSensor

from services.publisher import publish_sensor_data

connect_wifi()

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