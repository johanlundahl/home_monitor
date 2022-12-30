from dataclasses import dataclass
from pytils.config import Configuration


@dataclass
class MQTT:
    url: str = 'localhost'
    topic: str = 'sensors'


@dataclass
class Slack:
    url: str = 'localhost'


@dataclass
class HomeStore:
    url: str = 'http://localhost:5000/api/v2/sensors'


@dataclass
class Config(Configuration):
    mqtt: MQTT = MQTT()
    slack: Slack = Slack()
    home_store: HomeStore = HomeStore()


if __name__ == '__main__':
    config = Config.init()
