from umqtt.simple import MQTTClient

from config import BROKER

CLIENT_ID = "esp32-ss226uk"

def connect_mqtt():

    client = MQTTClient(
        CLIENT_ID,
        BROKER,
        keepalive=60
    )

    client.connect()

    print("Connected to MQTT broker!")

    return client