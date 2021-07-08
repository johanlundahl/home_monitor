import abc
import logging
from pytils import http, slack


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, next_command=None):
        self._next = next_command

    def handle(self, sensor):
        self.process(sensor)
        if self.proceed:
            self._next.handle(sensor)

    @property
    def proceed(self):
        return self._next is not None

    @abc.abstractmethod
    def process(self, sensor):
        pass


class PersistHandler(Handler):

    def __init__(self, next_command=None, url=None):
        self._next = next_command
        self._url = url

    def process(self, sensor):
        logging.info(f'{type(self).__name__} processing of {str(sensor)}')
        status_code, data = http.post_json(self._url, sensor.reading.to_json())
        if status_code != 200:
            logging.error((f'Status code {status_code} ',
                           f'when POST\'ing {sensor.reading.to_json()}'))


class AlarmHandler(Handler):

    def __init__(self, next_command=None, slack_webhook_url=''):
        self._next = next_command
        self._slack_webhook_url = slack_webhook_url

    def process(self, sensor):
        logging.info(f'{type(self).__name__} processing of {sensor}')
        if sensor.triggered:
            self.raise_alarm(sensor)
            sensor.alarm_raised()

    def raise_alarm(self, sensor):
        name = sensor.reading.name
        temp = sensor.reading.temperature
        humidity = sensor.reading.humidity
        message = (f'Warning {name}! ',
                   f'Temperature {temp} C, Humidity {humidity} %')
        slack.post(self._slack_webhook_url, message)
