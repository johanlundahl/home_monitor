# home_monitor

## Prerequisites

This project is suitable to run on a Raspberry Pi with python. For this project to make sense there should be a MQTT broker reachable for the Raspberry Pi and something posting messages to that MQTT broker. Please find instructions on how to set up a MQTT broker here: https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/

The MQTT broker can be installed on the same Raspberry Pi running this project. 

MQTT on ESP8266
https://randomnerdtutorials.com/micropython-mqtt-esp32-esp8266/

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

## Running

To start the application manually 
```
$ python3 -m home_store.app
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
sudo reboot
```