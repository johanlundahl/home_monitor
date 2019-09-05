import json
from datetime import datetime

class Sensor:
    def __init__(self, name, temperature, humidity, timestamp):
        self.name = name
        self.temperature = temperature
        self.humidity = humidity
        self.timestamp = timestamp

    def to_json(self):
        return json.dumps(self, cls=SensorEncoder)

    @classmethod
    def from_json(cls, dct):
        return json.loads(dct, object_hook=SensorDecoder.decode)

    def __str__(self):
        return 'Sensor({}, {}, {})'.format(self.name, self.temperature, self.humidity)


class SensorEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Sensor):
            return {'name': obj.name, 'temperature': obj.temperature, 'humidity': obj.humidity, 'timestamp': obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
        else:
            return super().default(obj)

class SensorDecoder():
    @classmethod
    def decode(cls, dct):
        if 'temperature' in dct and 'humidity' in dct:
            return Sensor(dct['name'], dct['temperature'], dct['humidity'], datetime.now())