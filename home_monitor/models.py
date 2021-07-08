from datetime import datetime
import json
from home_monitor.alarms import NormalState, AlarmState, TriggeredState


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
        return isinstance(self._alarm_state, (AlarmState, TriggeredState))

    @property
    def triggered(self):
        return isinstance(self._alarm_state, TriggeredState)

    @property
    def alarm_state(self):
        return self._alarm_state

    @property
    def reading(self):
        return self._reading

    @reading.setter
    def reading(self, reading):
        self._last_updated = datetime.now()
        self._reading = reading
        self._alarm_state = self._alarm_state.on_event(reading)

    def alarm_raised(self):
        self._alarm_state = self._alarm_state.on_event(self._reading)

    @property
    def last_updated(self):
        return self._last_updated

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (f'Sensor ({self.reading.name}, '
                f'{self.last_updated}, {self.alarm_state})')


class Reading:

    def __init__(self, name, temperature, humidity, timestamp):
        self._name = name
        self._temperature = temperature
        self._humidity = humidity
        self._timestamp = timestamp

    @property
    def name(self):
        return self._name

    @property
    def temperature(self):
        return self._temperature

    @property
    def humidity(self):
        return self._humidity

    @property
    def timestamp(self):
        return self._timestamp.strftime('%Y-%m-%d %H:%M:%S')

    def to_json(self):
        return json.dumps(self, cls=SensorEncoder)

    @classmethod
    def from_json(cls, dct):
        return json.loads(dct, object_hook=SensorDecoder.decode)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'Reading({self._name}, {self._temperature}, {self._humidity})'


class SensorEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Sensor):
            return {'name': obj.reading.name,
                    'last_updated': obj.last_updated,
                    'alarm_state': obj.alarm_state
                    }
        if isinstance(obj, Reading):
            return {'name': obj.name,
                    'temperature': obj.temperature,
                    'humidity': obj.humidity,
                    'timestamp': obj.timestamp
                    }
        else:
            return super().default(obj)


class SensorDecoder():

    @classmethod
    def decode(cls, dct):
        if 'temperature' in dct and 'humidity' in dct:
            return Reading(dct['name'], dct['temperature'],
                           dct['humidity'], datetime.now())
