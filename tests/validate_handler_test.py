import unittest
from datetime import datetime
from home_monitor.handlers import ValidateHandler
from home_monitor.models import Reading


class ValidateHandlerTest(unittest.TestCase):
        
    def setUp(self):
        self.validateHandler = ValidateHandler()

    def test_process_first_for_sensor(self):
        self.assertFalse('Room' in self.validateHandler._sensors)
        reading = Reading('Room', 10, 50, datetime.now())
        self.validateHandler.process(reading)
        self.assertTrue('Room' in self.validateHandler._sensors)
        
    def test_process_several_with_same_name(self):
        self.assertFalse('Room' in self.validateHandler._sensors)
        self.assertTrue(len(self.validateHandler._sensors) == 0)
        reading1 = Reading('Room', 10, 50, datetime.now())
        self.validateHandler.process(reading1)
        self.assertTrue('Room' in self.validateHandler._sensors)
        self.assertTrue(len(self.validateHandler._sensors) == 1)
        reading2 = Reading('Room', 20, 60, datetime.now())
        self.validateHandler.process(reading2)
        self.assertTrue('Room' in self.validateHandler._sensors)
        self.assertTrue(len(self.validateHandler._sensors) == 1)
        
    def test_process_several_with_different_names(self):
        reading1 = Reading('bathroom', 10, 50, datetime.now())
        reading2 = Reading('livingroom', 20, 60, datetime.now())
        self.validateHandler.process(reading1)
        self.validateHandler.process(reading2)
        self.assertTrue('bathroom' in self.validateHandler._sensors)
        self.assertTrue('livingroom' in self.validateHandler._sensors)


if __name__ == '__main__':
    unittest.main()