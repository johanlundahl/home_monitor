import unittest
from datetime import datetime
from home_monitor.manager import SensorManager
from home_monitor.models import Reading


class ManagerTest(unittest.TestCase):

    def setUp(self):
        self.manager = SensorManager('', '')

    def test_handle_first(self):
        reading = Reading('outdoor', 1, 2, datetime.now())
        self.assertFalse('outdoor' in self.manager._sensors)
        self.manager.update_sensor(reading)
        self.assertTrue('outdoor' in self.manager._sensors)

    def test_handle_several_with_same_name(self):
        reading = Reading('indoor', 2, 3, datetime.now())
        self.manager.update_sensor(reading)
        reading = Reading('indoor', 4, 5, datetime.now())
        self.manager.update_sensor(reading)
        self.assertTrue('indoor' in self.manager._sensors)
        self.assertEqual(1, len(self.manager._sensors))

    def test_handle_several_with_different_names(self):
        room1 = Reading('Room 1', 21, 56, datetime.now())
        room2 = Reading('Room 2', 19, 50, datetime.now())
        self.manager.update_sensor(room1)
        self.manager.update_sensor(room2)
        self.assertTrue('Room 1' in self.manager._sensors)
        self.assertTrue('Room 2' in self.manager._sensors)


if __name__ == '__main__':
    unittest.main()
