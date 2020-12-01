import unittest
from datetime import datetime
from home_monitor.handlers import AlarmHandler
from home_monitor.models import Reading


class AlarmHandlerTest(unittest.TestCase):
        
    def setUp(self):
        self.alarmHandler = AlarmHandler()

    def test_process_first_normal_sensor(self):
        reading = Reading('abc', 10, 20, datetime.now())
        self.alarmHandler.process(reading)
        self.assertEqual(1, len(self.alarmHandler._alarmed))
        
    def test_process_several_normal_sensors(self):
        reading1 = Reading('abc', 10, 20, datetime.now())
        self.alarmHandler.process(reading1)
        reading2 = Reading('abc', 10, 20, datetime.now())
        self.alarmHandler.process(reading2)
        self.assertEqual(1, len(self.alarmHandler._alarmed))


if __name__ == '__main__':
    unittest.main()