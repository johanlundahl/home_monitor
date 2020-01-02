# Home Monitor
This project receives sensor values from a MQTT server, checks their values against pre-defined validation rules and sends them to [Home Store](http://github.com/johanlundahl/home_store) for storage.

This project is suitable to run on a Raspberry Pi and is intended to use with [Temp Sensor](http://github.com/johanlundahl/temp_sensor), [Home Store](http://github.com/johanlundahl/home_store), [Home Eye](http://github.com/johanlundahl/home_eye) and [Mosquitto MQTT Broker](https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/).

## Prerequisites
Please find instructions on how to set up a MQTT broker here: https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/

View all messages sent to the MQTT Broker (locally on the same machine):

```
$ mosquitto_sub -t /#
```

## Installation

Clone this git repo

```
$ git clone https://github.com/johanlundahl/home_monitor
```

Install required python modules

```
$ sudo pip3 install -r requirements.txt
```

Edit config.py and add required configuration parameters for the application by
```
$ nano home_monitor/config.py
```

Specify the following configuration parameters in the `home_monitor/config.py` file:
```
mqtt_server = 'ip-address-of-mqtt-broker'
topic_sub = 'mqtt-topic-name'
slack_webhook_url = 'url-to-post-slack-messages-to'
save_sensor_url = 'http://ip-address-to-home-store/api/sensors'
```


## Running

To start the application manually 
```
$ python3 -m home_store.app
```

Make the python script executable:
```
$ chmod +x home_store/app.py
```

To make the application start automatically define a crontab job. Edit crontab by
```
$ crontab -e
```

Define which time the different jobs should be run at, e.g.
```
@reboot python3 /home/pi/home_monitor/home_monitor/app.py
```

Reboot your Rasperry Pi and the application will start:
```
$ sudo reboot
```

## Logging
Application events are logged to the application log file and can be viewed through
```
$ tail -f application.log
```
