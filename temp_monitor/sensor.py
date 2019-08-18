import json

class Sensor:
    def __init__(self, name, temperature, humidity):
        self.name = name
        self.temperature = temperature
        self.humidity = humidity

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
            return {'type': 'Sensor', 'name': obj.name, 'temperature': obj.temperature, 'humidity': obj.humidity}
        else:
            return super().default(obj)

class SensorDecoder():
    @classmethod
    def decode(cls, dct):
        if 'temperature' in dct and 'humidity' in dct:
            return Sensor(dct['name'], dct['temperature'], dct['humidity'])