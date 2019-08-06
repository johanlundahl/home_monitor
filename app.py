import paho.mqtt.client as mqtt
import json
import slack
import config

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print('Connected to {} (with result code {})'.format(config.mqtt_server, str(rc)))
    client.subscribe(config.topic_sub)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == config.topic_sub:
        vals = json.loads(msg.payload)
        if vals['temperature'] < 18 or vals['temperature'] > 30:
            #print('Temperature is to low or high!')
            slack.post('Temperature is to low or high! Temperature is {} C and humidity is {} %.'.format(vals['temperature'], vals['humidity']))
            
        if vals['humidity'] < 30 or vals['humidity'] > 70:
            #print('Humidity is to low or high!')
            slack.post('Humidity is to low or high! Temperature is {} C and humidity is {} %.'.format(vals['temperature'], vals['humidity']))
    print(msg.topic+" "+str(msg.payload))

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(config.mqtt_server, 1883, 60)
    client.loop_forever()