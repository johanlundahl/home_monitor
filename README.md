# temp_monitor

##Prerequisites

This project is suitable to run on a Raspberry Pi with python. For this project to make sense there should be a MQTT broker reachable for the Raspberry Pi and something posting messages to that MQTT broker. Please find instructions on how to set up a MQTT broker here: https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/

The MQTT broker can be installed on the same Raspberry Pi running this project. 

MQTT on ESP8266
https://randomnerdtutorials.com/micropython-mqtt-esp32-esp8266/

View all messages sent to the MQTT Broker (locally on the same machine):
$ mosquitto_sub -t /#

TODO:
Add timestamp
Post with name or on different "channel"
Add rules
Post alarms to slack
Keep track of alarm status
Structure of files into modules
Add webapp to project
Install app to crontab -e

## Installation

Clone this git repo

```
$ git clone https://github.com/johanlundahl/temp_monitor
```

Install required python modules

```
$ sudo pip3 install -r requirements.txt
```

Edit config.py and add required configuration parameters for the application by
```
$ nano temp_monitor/config.py
```

Set up crontab jobs to schedule the scripts. Edit crontab by
```
$ crontab -e
```

Define which time the different jobs should be run at, e.g.
```
@reboot python3 /home/pi/temp_monitor/temp_monitor/app.py
```

Reboot your Rasperry Pi and the application will start:
```
sudo reboot
```