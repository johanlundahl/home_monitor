import datetime
from home_monitor.handlers import Persist, Validator 
from home_monitor.models import Reading


class SensorManager:
    
    def __init__(self, sensor_url, slack_url, lifetime=24):
        self.save_sensor_url = sensor_url
        self.slack_webhook_url = slack_url

        # set up chain of responsibity commands for handling incoming sensors
        persist = Persist(url=sensor_url)
        validator = Validator(persist)
        self.first_command = validator

    def delegate(self, reading: Reading):
        self.first_command.handle(reading)
   