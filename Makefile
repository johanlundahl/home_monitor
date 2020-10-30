
init:
	sudo pip3 install -r requirements.txt
	chmod +x home_store/app.py

run:
	python3 -m home_monitor.app

logging:
	tail -f application.log