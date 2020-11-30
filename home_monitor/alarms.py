import abc
from pytils import validator


class State(metaclass=abc.ABCMeta):

    def __init__(self):
        self.alarm_checker = validator.Checker().any()
        self.alarm_checker.add_rule(lambda x: x.temperature < 15 and x.name == 'basement', 'Temperature is to low.')
        self.alarm_checker.add_rule(lambda x: x.temperature > 30 and x.name == 'basement', 'Temperature is to high.')
        self.alarm_checker.add_rule(lambda x: x.humidity < 30 and x.name == 'basement', 'Humidity is to low.')
        self.alarm_checker.add_rule(lambda x: x.humidity > 70 and x.name == 'basement', 'Humidity is to high.')
        self.alarm_checker.add_rule(lambda x: x.temperature <= 0 and x.name == 'outdoor', 'Its cold outside! Save paint and batteries :)')

    @abc.abstractmethod
    def on_event(self, reading):
        pass

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.__class__.__name__


class NormalState(State):

    def on_event(self, reading):
        is_alarm = self.alarm_checker.validate(reading)
        if is_alarm:
            return AlarmState()
        return self


class AlarmState(State):

    def on_event(self, reading):
        is_alarm = self.alarm_checker.validate(reading)
        if not is_alarm:
            return NormalState()
        return self
