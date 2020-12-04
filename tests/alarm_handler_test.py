import unittest
from datetime import datetime
from home_monitor.handlers import AlarmHandler
from home_monitor.models import Reading, Sensor


class AlarmHandlerTest(unittest.TestCase):
        
    def setUp(self):
        webhook = 'https://hooks.slack.com/services/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'
        self.alarmHandler = AlarmHandler(None, webhook)

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