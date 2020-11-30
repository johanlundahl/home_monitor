import unittest
from datetime import datetime
from home_monitor.models import Sensor, Reading


class SensorTest(unittest.TestCase):

    def test_create_normal_state(self):
        reading = Reading('indoor', 19, 57, datetime.now())
        sensor = Sensor.create(reading)
        self.assertFalse(sensor.alarm)

    def test_create_alarm_state(self):
        reading = Reading('outdoor', -19, 57, datetime.now())
        sensor = Sensor.create(reading)
        self.assertTrue(sensor.alarm)

    def test_update_reading_to_alarm_state(self):
        reading = Reading('outdoor', -1, 57, datetime.now())
        sensor = Sensor.create(reading)
        self.assertTrue(sensor.alarm)
        sensor.reading = Reading('outdoor', 2, 55, datetime.now())
        self.assertFalse(sensor.alarm)


if __name__ == '__main__':
    unittest.main()