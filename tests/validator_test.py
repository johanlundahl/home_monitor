import unittest
from datetime import datetime
from home_monitor.handlers import Validator
from home_monitor.models import Reading


class ValidatorTest(unittest.TestCase):
        
    def setUp(self):
        self.validator = Validator()

    def test_process_first_for_sensor(self):
        self.assertFalse('Room' in self.validator._sensors)
        reading = Reading('Room', 10, 50, datetime.now())
        self.validator.process(reading)
        self.assertTrue('Room' in self.validator._sensors)
        
    def test_process_several_with_same_name(self):
        self.assertFalse('Room' in self.validator._sensors)
        self.assertTrue(len(self.validator._sensors) == 0)
        reading1 = Reading('Room', 10, 50, datetime.now())
        self.validator.process(reading1)
        self.assertTrue('Room' in self.validator._sensors)
        self.assertTrue(len(self.validator._sensors) == 1)
        reading2 = Reading('Room', 20, 60, datetime.now())
        self.validator.process(reading2)
        self.assertTrue('Room' in self.validator._sensors)
        self.assertTrue(len(self.validator._sensors) == 1)
        
    def test_process_several_with_different_names(self):
        reading1 = Reading('bathroom', 10, 50, datetime.now())
        reading2 = Reading('livingroom', 20, 60, datetime.now())
        self.validator.process(reading1)
        self.validator.process(reading2)
        self.assertTrue('bathroom' in self.validator._sensors)
        self.assertTrue('livingroom' in self.validator._sensors)


if __name__ == '__main__':
    unittest.main()