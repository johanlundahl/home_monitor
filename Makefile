MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))

init:
	sudo pip3 install -r requirements.txt
	chmod +x home_store/app.py

autostart:
	(crontab -l; echo "@reboot cd $(MKFILE_PATH) && python3 -m home_monitor.app") | crontab -u pi -

run:
	python3 -m home_monitor.app

logging:
	tail -f application.log