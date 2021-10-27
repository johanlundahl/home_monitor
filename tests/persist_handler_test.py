from datetime import datetime
import unittest
from unittest.mock import patch
from home_monitor.handlers import PersistHandler, AlarmHandler
from home_monitor.models import Reading, Sensor


class PersistHandlerTest(unittest.TestCase):

    @patch('home_monitor.handlers.PersistHandler.process')
    def test_handle_single_handler(self, mock):
        reading = Reading('outdoor', 10, 20, datetime.now())
        sensor = Sensor.create(reading)
        handler = PersistHandler()
        handler.handle(sensor)
        self.assertTrue(mock.called)
        self.assertFalse(handler.proceed)

    @patch('home_monitor.handlers.PersistHandler.process')
    @patch('home_monitor.handlers.AlarmHandler.process')
    def test_handle_several_handlers(self, p_mock, a_mock):
        reading = Reading('outdoor', 10, 20, datetime.now())
        sensor = Sensor.create(reading)
        p_handler = PersistHandler()
        a_handler = AlarmHandler(next_command=p_handler)
        a_handler.handle(sensor)

        self.assertTrue(a_mock.called)
        self.assertTrue(a_handler.proceed)
        self.assertTrue(p_mock.called)
        self.assertFalse(p_handler.proceed)


if __name__ == '__main__':
    unittest.main()
