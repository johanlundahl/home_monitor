import unittest
from datetime import datetime
from pytils import config
from home_monitor.handlers import AlarmHandler
from home_monitor.models import Reading, Sensor


class AlarmHandlerTest(unittest.TestCase):

    def setUp(self):
        cfg = config.init('home_monitor/app-test.yaml')
        slack_url = cfg.slack_webhook_url
        self.alarmHandler = AlarmHandler(next_command=None,
                                         slack_webhook_url=slack_url)

    def test_process_first_normal_sensor(self):
        reading = Reading('outdoor', 10, 20, datetime.now())
        sensor = Sensor.create(reading)
        self.alarmHandler.process(sensor)

    def test_process_several_normal_sensors(self):
        reading = Reading('outdoor', 10, 20, datetime.now())
        sensor = Sensor.create(reading)
        self.alarmHandler.process(sensor)
        sensor.reading = Reading('outdoor', -10, 20, datetime.now())
        self.alarmHandler.process(sensor)
        # What to assert?


if __name__ == '__main__':
    unittest.main()
