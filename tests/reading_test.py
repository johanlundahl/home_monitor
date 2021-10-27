from datetime import datetime
import json
import unittest
from home_monitor.models import Reading


class ReadingTest(unittest.TestCase):

    def test_from_json(self):
        dct = {
            'temperature': 23,
            'humidity': 65,
            'name': 'house'
        }
        reading = Reading.from_json(json.dumps(dct))
        self.assertTrue(isinstance(reading, Reading))

    def test_reading_to_json(self):
        reading = Reading('house', 25, 55, datetime.now())
        j = reading.to_json()
        self.assertIn('name', j)
        self.assertIn('temperature', j)
        self.assertIn('humidity', j)
        self.assertIn('timestamp', j)


if __name__ == '__main__':
    unittest.main()
