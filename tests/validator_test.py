import unittest
from datetime import datetime
from home_monitor.handlers import ValidateHandler
from home_monitor.models import Reading


class ValidateHandlerTest(unittest.TestCase):
        
    def setUp(self):
        self.ValidateHandler = ValidateHandler()

    def test_process_first_for_sensor(self):
        self.assertFalse('Room' in self.ValidateHandler._sensors)
        reading = Reading('Room', 10, 50, datetime.now())
        self.ValidateHandler.process(reading)
        self.assertTrue('Room' in self.ValidateHandler._sensors)
        
    def test_process_several_with_same_name(self):
        self.assertFalse('Room' in self.ValidateHandler._sensors)
        self.assertTrue(len(self.ValidateHandler._sensors) == 0)
        reading1 = Reading('Room', 10, 50, datetime.now())
        self.ValidateHandler.process(reading1)
        self.assertTrue('Room' in self.ValidateHandler._sensors)
        self.assertTrue(len(self.ValidateHandler._sensors) == 1)
        reading2 = Reading('Room', 20, 60, datetime.now())
        self.ValidateHandler.process(reading2)
        self.assertTrue('Room' in self.ValidateHandler._sensors)
        self.assertTrue(len(self.ValidateHandler._sensors) == 1)
        
    def test_process_several_with_different_names(self):
        reading1 = Reading('bathroom', 10, 50, datetime.now())
        reading2 = Reading('livingroom', 20, 60, datetime.now())
        self.ValidateHandler.process(reading1)
        self.ValidateHandler.process(reading2)
        self.assertTrue('bathroom' in self.ValidateHandler._sensors)
        self.assertTrue('livingroom' in self.ValidateHandler._sensors)


if __name__ == '__main__':
    unittest.main()