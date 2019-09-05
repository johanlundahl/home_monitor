import requests
from temp_monitor import config
import json

def post(obj):
	print(obj)
	headers = {'content-type': 'application/json'}
	response = requests.post(config.save_sensor_url, data = obj, headers = headers)
	print(response.status_code)