MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_DIR := $(dir $(MKFILE_PATH))

init:
	sudo pip3 install -r requirements.txt
	chmod +x home_store/app.py

autostart:
	(crontab -l; echo "@reboot cd $(CURRENT_DIR) && python3 -m home_monitor.app") | crontab -u pi -

run:
	python3 -m home_monitor.app

logging:
	tail -f application.log