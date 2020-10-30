# Home Monitor
This project receives sensor values from a MQTT server, checks their values against pre-defined validation rules and sends them to [Home Store](http://github.com/johanlundahl/home_store) for storage.

This project is suitable to run on a Raspberry Pi and is intended to use with [Temp Sensor](http://github.com/johanlundahl/temp_sensor), [Home Store](http://github.com/johanlundahl/home_store), [Home Eye](http://github.com/johanlundahl/home_eye) and [Mosquitto MQTT Broker](https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/).

## Prerequisites
Please find instructions on how to set up a MQTT broker here: https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/

View all messages sent to the MQTT Broker (locally on the same machine):

```
$ mosquitto_sub -t /#
```
or
```
$ mosquitto_sub -v -t 'sensors'
```

## Installation

Clone this git repo

```
$ git clone https://github.com/johanlundahl/home_monitor
```

Install required python modules

```
$ make init
```

Edit config.py and add required configuration parameters for the application by
```
$ nano home_monitor/app.yaml
```

Specify the following configuration parameters in the `home_monitor/app.yaml` file:
``` yaml
mqtt:
  server: "ip of mqtt server"
  topic: "sensors"

... 

slack_webhook_url: = ""

...

save_sensor_url: "http://localhost:5000/api/sensors"

```


## Running

To start the application manually 
```
$ make run
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
$ make logging
```

## How to use the application
The application do not have a graphic interface. It subscribes to a topic on a MQTT broker. Any received value is posted to [Home Store](http://github.com/johanlundahl/home_store) where it is persisted. Received values are checked against the defined warning rules in the `home_monitor/manager.py` file. If the received value fulfil any of the rules then a warning is posted to a Slack channel.

Read the [Incoming Webhooks for Slack](https://slack.com/intl/en-se/help/articles/115005265063-Incoming-WebHooks-for-Slack) tutorial to learn more on how to set up your Slack channel so that it can receive messages from external apps.