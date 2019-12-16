import paho.mqtt.client as mqtt
import json
from datetime import datetime
from pytils import http, logger
from home_monitor import config
from home_monitor.manager import SensorManager
from home_monitor.model.sensor import Sensor, Reading
import time


manager = SensorManager()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logger.info('Connected to MQTT server {} (with result code {})'.format(config.mqtt_server, str(rc)))
    client.subscribe(config.topic_sub)
    logger.info('Subscribing to topic {}'.format(config.topic_sub))
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    logger.info('Receiving message: {}'.format(msg.payload))

    if msg.topic == config.topic_sub:
        reading = Reading.from_json(msg.payload)
        global manager
        manager.update(reading)

def start_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(config.mqtt_server, 1883, 60)
    client.loop_start()
    return client

def stop_client(client):
    client.disconnect()
    client.loop_stop()

def run():
    client = start_client()
    while True:
        time.sleep(60)
    stop_client(client)

if __name__ == '__main__':
    try:
        logger.init()
        run()
    except Exception:
        logger.exception('Application Exception')