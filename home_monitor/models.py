from datetime import datetime
import json
from home_monitor.alarms import NormalState, AlarmState


class Sensor:

    def __init__(self):
        self._last_updated = None
        self._alarm_state = NormalState()
        self._reading = None

    @classmethod
    def create(cls, reading):
        sensor = Sensor()
        sensor.reading = reading
        return sensor

    @property
    def alarm(self):
        return isinstance(self._alarm_state, AlarmState)

    @property
    def reading(self):
        return self._reading
    
    @reading.setter
    def reading(self, reading):
        self._last_updated = datetime.now()
        self._reading = reading
        self._alarm_state = self._alarm_state.on_event(reading)

    @property
    def last_updated(self):
        return self._last_updated

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