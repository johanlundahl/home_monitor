from home_monitor.handlers import PersistHandler, AlarmHandler
from home_monitor.models import Sensor


class SensorManager:

    def __init__(self, sensor_url, slack_url):
        self.save_sensor_url = sensor_url
        self.slack_webhook_url = slack_url

        persist_handler = PersistHandler(url=sensor_url)
        alarmHandler = AlarmHandler(persist_handler)
        self.first_command = alarmHandler
        self._sensors = {}

    def handle(self, reading):
        self.update_sensor(reading)
        self.delegate(self._sensors[reading.name])

    def update_sensor(self, reading):
        if reading.name in self._sensors:
            sensor = self._sensors[reading.name]
            sensor.reading = reading
        else:
            self._sensors[reading.name] = Sensor.create(reading)

    def delegate(self, sensor):
        self.first_command.handle(sensor)
