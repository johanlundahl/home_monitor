import abc
import logging
from pytils import http
from home_monitor.models import Sensor, Reading


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, next_command=None):
        self._next = next_command

    def handle(self, reading):
        self.process(reading)
        if self.proceed:
            self._next.handle(reading)

    @property
    def proceed(self):
        return self._next != None

    @abc.abstractmethod
    def process(self, reading):
        pass


class ValidateHandler(Handler):

    def __init__(self, next_command=None):
        self._next = next_command
        self._sensors = {}

    def process(self, reading: Reading):
        logging.info('{} processing of {}'.format(type(self).__name__, str(reading)))
        sensor = self.get_sensor(reading)
        sensor.reading = reading
    
    def get_sensor(self, reading: Reading):
        if reading.name not in self._sensors:
            self._sensors[reading.name] = Sensor.create(reading)
        return self._sensors[reading.name]            


class PersistHandler(Handler):

    def __init__(self, next_command=None, url=None):
        self._next = next_command
        self._url = url

    def process(self, reading):
        logging.info('{} processing of {}'.format(type(self).__name__, str(reading)))
        status_code, data = http.post_json(self._url, reading.to_json())
        if status_code != 200:
            logging.error('Status code {} when POST\'ing {}'.format(status_code, reading.to_json()))
    

class AlarmHandler(Handler):

    def __init__(self, next_command=None):
        self._next = next_command
        self._alarmed = {}

    def process(self, request):
        request.history.append('notify if alarm')
        # check if alarm and if have been notified before
        # do not alarm if sensor is not in dict

    #def notify(self, alarm, sensor):
        #    message = 'Warning {}! {} Temperature {} C, Humidity {} %'.format(sensor.name, alarm, sensor.temperature, sensor.humidity)
        #    slack.post(self.slack_webhook_url, message)
