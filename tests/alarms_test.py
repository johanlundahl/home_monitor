import unittest
from datetime import datetime
from home_monitor.models import Reading
from home_monitor.alarms import AlarmState, NormalState


class StateTest(unittest.TestCase):

    def test_on_event_unchanged_state(self):
        state = NormalState()
        self.assertTrue(isinstance(state, NormalState))
        reading = Reading('outdoor', 10, 50, datetime.now())
        state = state.on_event(reading)
        self.assertTrue(isinstance(state, NormalState))

    def test_on_event_change_state(self):
        state = NormalState()
        self.assertEqual(type(state), NormalState)
        reading = Reading('outdoor', -10, 50, datetime.now())
        state = state.on_event(reading)
        self.assertEqual(type(state), AlarmState)

    def test_on_event_change_to_normal(self):
        state = AlarmState()
        self.assertEqual(type(state), AlarmState)
        reading = Reading('outdoor', 5, 50, datetime.now())
        state = state.on_event(reading)
        self.assertEqual(type(state), NormalState)
        
    def test_on_event_unchanged_alarm_state(self):
        state = AlarmState()
        self.assertEqual(type(state), AlarmState)
        reading = Reading('outdoor', -5, 50, datetime.now())
        state = state.on_event(reading)
        self.assertEqual(type(state), AlarmState)
        

if __name__ == '__main__':
    unittest.main()