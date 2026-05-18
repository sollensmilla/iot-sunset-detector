from umqtt.simple import MQTTClient

from config import BROKER
from secrets import MQTT_USER, MQTT_PASSWORD

CLIENT_ID = "esp32-ss226uk"

def connect_mqtt():

    client = MQTTClient(
      CLIENT_ID,
      BROKER,
      user=MQTT_USER,
      password=MQTT_PASSWORD,
      keepalive=60
    )

    client.connect()

    print("Connected to MQTT broker!")

    return client