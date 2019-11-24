import paho.mqtt.client as mqtt
import json
from datetime import datetime
from pytils import validator, http, slack
from home_monitor import config
from home_monitor.model.sensor import Sensor
import time

sensor_checker = validator.Checker().all()
sensor_checker.add_rule(lambda x: x.temperature > 15, 'Temperature is to low.')
sensor_checker.add_rule(lambda x: x.temperature < 30, 'Temperature is to high.')
sensor_checker.add_rule(lambda x: x.humidity > 30, 'Humidity is to low.')
sensor_checker.add_rule(lambda x: x.humidity < 70, 'Humidity is to high.')

sensor_readings = {}

# TODO: logging
# TODO: move http and slack to pytils
# TODO: move alarm functionality to module
# TODO: add sensor name to Checker rules

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print('Connected to MQTT server {} (with result code {})'.format(config.mqtt_server, str(rc)))
    client.subscribe(config.topic_sub)
    print('Subscribing to topic {}'.format(config.topic_sub))
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('{} {}'.format(ts, msg.payload))

    if msg.topic == config.topic_sub:
        sensor = Sensor.from_json(msg.payload)
        status_code = http.post_json(config.save_sensor_url, sensor.to_json())
        
        global sensor_readings
        sensor_readings[sensor.name] = (datetime.now(), sensor)
        if not sensor_checker.validate(sensor):
            alarm = sensor_checker.evaluate(sensor)
            notify(alarm, sensor)        

def notify(alarm, sensor):
    message = 'Warning {}! {} Temperature {} C, Humidity {} %'.format(sensor.name, alarm, sensor.temperature, sensor.humidity)
    print(message)
    slack.post(config.slack_webhook_url, message)

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
        time.sleep(10)
        for name in sensor_readings:
            dt, sensor = sensor_readings[name]
            if (datetime.now()-dt).seconds > 60*5:
                print((datetime.now()-dt).seconds, 'seconds since last reading')
            
    stop_client(client)

if __name__ == '__main__':
    run()