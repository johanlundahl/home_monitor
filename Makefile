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

update: 
	git pull
	pip3 install -r requirements.txt	
