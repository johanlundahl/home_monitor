import unittest
from datetime import datetime
from home_monitor.models import Sensor, Reading
from home_monitor.alarms import NormalState, AlarmState, TriggeredState


class SensorTest(unittest.TestCase):

    def test_create_normal_state(self):
        reading = Reading('indoor', 19, 57, datetime.now())
        sensor = Sensor.create(reading)
        self.assertFalse(sensor.alarm)

    def test_create_alarm_state(self):
        reading = Reading('outdoor', -19, 57, datetime.now())
        sensor = Sensor.create(reading)
        self.assertTrue(sensor.alarm)

    def test_update_normal_to_triggered_state(self):
        reading = Reading('outdoor', 1, 57, datetime.now())
        sensor = Sensor.create(reading)
        self.assertTrue(isinstance(sensor.alarm_state, NormalState))
        sensor.reading = Reading('outdoor', -2, 55, datetime.now())
        self.assertTrue(isinstance(sensor.alarm_state, TriggeredState))
    
    def test_update_triggered_to_normal_state(self):
        reading = Reading('outdoor', -1, 57, datetime.now())
        sensor = Sensor.create(reading)
        self.assertTrue(isinstance(sensor.alarm_state, TriggeredState))
        sensor.reading = Reading('outdoor', 2, 55, datetime.now())
        self.assertTrue(isinstance(sensor.alarm_state, NormalState))
        
    def test_update_triggered_to_alarm_state(self):
        reading = Reading('outdoor', -1, 57, datetime.now())
        sensor = Sensor.create(reading)
        self.assertTrue(isinstance(sensor.alarm_state, TriggeredState))
        sensor.reading = Reading('outdoor', -2, 55, datetime.now())
        self.assertTrue(isinstance(sensor.alarm_state, AlarmState))

    def test_update_alaram_to_normal_state(self):
        reading = Reading('outdoor', -1, 57, datetime.now())
        sensor = Sensor.create(reading)
        sensor.reading = Reading('outdoor', -2, 55, datetime.now())
        self.assertTrue(isinstance(sensor.alarm_state, AlarmState))
        sensor.reading = Reading('outdoor', 2, 55, datetime.now())
        self.assertTrue(isinstance(sensor.alarm_state, NormalState))

    def test_update_alarm_to_alarm_state(self):
        reading = Reading('outdoor', -1, 57, datetime.now())
        sensor = Sensor.create(reading)
        sensor.reading = Reading('outdoor', -2, 55, datetime.now())
        self.assertTrue(isinstance(sensor.alarm_state, AlarmState))
        sensor.reading = Reading('outdoor', -3, 55, datetime.now())
        self.assertTrue(isinstance(sensor.alarm_state, AlarmState))


if __name__ == '__main__':
    unittest.main()