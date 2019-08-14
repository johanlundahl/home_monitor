import requests
import config

def post(message, image_url = None):
    payload = {"text": "{}".format(message)}
    if image_url is not None:
        payload['attachments'] = [{'fallback':'Overview of this weeks business.', 'image_url': image_url}]
    r = requests.post(url = config.slack_webhook_url, json = payload)
    return r.status_code, r.text