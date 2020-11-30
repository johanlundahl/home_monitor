import datetime
from home_monitor.handlers import PersistHandler, ValidateHandler 


class SensorManager:
    
    def __init__(self, sensor_url, slack_url, lifetime=24):
        self.save_sensor_url = sensor_url
        self.slack_webhook_url = slack_url

        # set up chain of responsibity commands for handling incoming sensors
        persist_handler = PersistHandler(url=sensor_url)
        ValidateHandler = ValidateHandler(persist_handler)
        self.first_command = ValidateHandler

    def delegate(self, reading):
        self.first_command.handle(reading)
   