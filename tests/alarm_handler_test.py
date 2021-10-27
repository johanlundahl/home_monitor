import unittest
from unittest.mock import patch
from datetime import datetime
from pytils import config
from home_monitor.handlers import AlarmHandler
from home_monitor.models import Reading, Sensor


class AlarmHandlerTest(unittest.TestCase):

    def setUp(self):
        cfg = config.init('tests/app-test.yaml')
        slack_url = cfg.slack_webhook_url
        self.alarmHandler = AlarmHandler(next_command=None,
                                         slack_webhook_url=slack_url)

    def test_process_first_normal_sensor(self):
        reading = Reading('outdoor', 10, 20, datetime.now())
        sensor = Sensor.create(reading)
        self.alarmHandler.process(sensor)

    @patch('home_monitor.handlers.slack.post')
    def test_process_several_normal_sensors(self, mock):
        mock.return_value = 200, ''
        reading = Reading('outdoor', 10, 20, datetime.now())
        sensor = Sensor.create(reading)
        self.alarmHandler.process(sensor)
        sensor.reading = Reading('outdoor', -10, 20, datetime.now())
        self.alarmHandler.process(sensor)
        # What to assert?


if __name__ == '__main__':
    unittest.main()
