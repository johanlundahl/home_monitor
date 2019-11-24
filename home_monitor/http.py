import requests
from temp_monitor import config
import json

def post(obj, name):
	print(obj)
	headers = {'content-type': 'application/json'}
	response = requests.post(config.save_sensor_url, data = obj, headers = headers)
	return response.status_code