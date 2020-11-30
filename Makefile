MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_DIR := $(dir $(MKFILE_PATH))

autostart:
	(crontab -l; echo "@reboot cd $(CURRENT_DIR) && python3 -m home_monitor.app") | crontab -u pi -

config:
	nano home_monitor/app.yaml

init:
	sudo pip3 install -r requirements.txt
	chmod +x home_store/app.py

logging:
	tail -f application.log

run:
	python3 -m home_monitor.app

test:
	python3 -m unittest tests/validator_test.py
	python3 -m unittest tests/alarms_test.py
	python3 -m unittest tests/sensor_test.py

update: 
	git pull
	pip3 install -r requirements.txt	
