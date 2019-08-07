import paho.mqtt.client as mqtt
import json
import slack
import config
from datetime import datetime
import validator
from sensor import Sensor

sensor_checker = validator.Checker().all()
sensor_checker.add_rule(lambda x: x.temperature > 15, 'Temperature is to low.')
sensor_checker.add_rule(lambda x: x.temperature < 30, 'Temperature is to high.')
sensor_checker.add_rule(lambda x: x.humidity > 30, 'Humidity is to low.')
sensor_checker.add_rule(lambda x: x.humidity < 70, 'Humidity is to high.')

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
        vals = json.loads(msg.payload)
        sensor = Sensor.from_json(vals)
        if not sensor_checker.validate(sensor):
            alarm = sensor_checker.evaluate(sensor)
            message = 'Warning {}! {} Temperature {} C, Humidity {} %'.format(sensor.name, alarm, sensor.temperature, sensor.humidity)
            print(message)
            slack.post(message)

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(config.mqtt_server, 1883, 60)
    client.loop_forever()