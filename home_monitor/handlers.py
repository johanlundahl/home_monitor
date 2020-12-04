import abc
from enum import Enum
import logging
from pytils import http, slack
from home_monitor.models import Sensor, Reading


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, next_command=None):
        self._next = next_command

    def handle(self, sensor):
        self.process(sensor)
        if self.proceed:
            self._next.handle(sensor)

    @property
    def proceed(self):
        return self._next != None

    @abc.abstractmethod
    def process(self, sensor):
        pass


class PersistHandler(Handler):

    def __init__(self, next_command=None, url=None):
        self._next = next_command
        self._url = url

    def process(self, sensor):
        logging.info('{} processing of {}'.format(type(self).__name__, str(sensor)))
        status_code, data = http.post_json(self._url, sensor.reading.to_json())
        if status_code != 200:
            logging.error('Status code {} when POST\'ing {}'.format(status_code, sensor.reading.to_json()))
    

class AlarmHandler(Handler):

    def __init__(self, next_command=None, slack_webhook_url=''):
        self._next = next_command
        self._slack_webhook_url = slack_webhook_url
        
    def process(self, sensor):
        logging.info('{} processing of {}'.format(type(self).__name__, str(sensor)))
        if sensor.triggered:
            self.raise_alarm(sensor)
            sensor.alarm_raised()

    def raise_alarm(self, sensor):
        message = 'Warning {}! Temperature {} C, Humidity {} %'.format(sensor.reading.name, 
            sensor.reading.temperature, 
            sensor.reading.humidity)
        slack.post(self._slack_webhook_url, message)

