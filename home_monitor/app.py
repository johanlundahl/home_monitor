import paho.mqtt.client as mqtt
import json
from datetime import datetime
from pytils import http, log
from pytils.config import cfg
from home_monitor.manager import SensorManager
from home_monitor.model.sensor import Sensor, Reading
import time


manager = SensorManager()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    log.info('Connected to MQTT server {} (with result code {})'.format(cfg.mqtt.server, str(rc)))
    client.subscribe(cfg.mqtt.topic)
    log.info('Subscribing to topic {}'.format(cfg.mqtt.topic))
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    log.info('Receiving message: {}'.format(msg.payload))

    if msg.topic == cfg.mqtt.topic:
        reading = Reading.from_json(msg.payload)
        global manager
        manager.update(reading)

def start_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(cfg.mqtt.server, 1883, 60)
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
        log.init()
        run()
    except Exception:
        log.exception('Application Exception')