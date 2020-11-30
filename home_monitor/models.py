import json
from datetime import datetime

class Sensor:

    def __init__(self, reading, last_reading=datetime.now(), alarm_state=False):
        self._reading = reading
        self._last_reading = last_reading
        self._alarm_state = alarm_state

    @property
    def alarm_state(self):
        return self._alarm_state
    
    @alarm_state.setter
    def alarm_state(self, alarm_state):
        self._alarm_state = alarm_state

    @property
    def reading(self):
        return self._reading

    @reading.setter
    def reading(self, reading):
        self._reading = reading
        self._last_reading = datetime.now()

    @property
    def last_reading(self):
        return self._last_reading

    def __repr__(self):
        return 'Sensor ({} {} {})'.format(self.reading.name, self.last_reading, self.alarm_state)        


class Reading:
    def __init__(self, name, temperature, humidity, timestamp):
        self.name = name
        self.temperature = temperature
        self.humidity = humidity
        self.timestamp = timestamp
        self.date = self.timestamp.strftime('%Y-%m-%d')

    def to_json(self):
        return json.dumps(self, cls=SensorEncoder)

    @classmethod
    def from_json(cls, dct):
        return json.loads(dct, object_hook=SensorDecoder.decode)

    def __str__(self):
        return 'Reading({}, {}, {})'.format(self.name, self.temperature, self.humidity)


class SensorEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Sensor):
            return {'name': obj.reading.name, 'last_reading': obj.last_reading, 'alarm_state': obj.alarm_state}
        if isinstance(obj, Reading):
            return {'name': obj.name, 'temperature': obj.temperature, 'humidity': obj.humidity, 'timestamp': obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
        else:
            return super().default(obj)

class SensorDecoder():
    @classmethod
    def decode(cls, dct):
        if 'temperature' in dct and 'humidity' in dct:
            return Reading(dct['name'], dct['temperature'], dct['humidity'], datetime.now())