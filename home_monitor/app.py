import logging
import time
import paho.mqtt.client as mqtt
from pytils import config
from home_monitor.manager import SensorManager
from home_monitor.models import Reading


cfg = config.init()
manager = SensorManager(cfg.save_sensor_url, cfg.slack_webhook_url)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.info(f'Connected to MQTT {cfg.mqtt.server} with result {str(rc)}')
    client.subscribe(cfg.mqtt.topic)
    logging.info('Subscribing to topic {}'.format(cfg.mqtt.topic))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    logging.info('Receiving message: {}'.format(msg.payload))

    if msg.topic == cfg.mqtt.topic:
        reading = Reading.from_json(msg.payload)
        global manager
        manager.handle(reading)


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
        run()
    except Exception:
        logging.exception('Application Exception')
