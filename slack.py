import requests

# URL to slack app web hook
slack_webhook_url = 'https://hooks.slack.com/services/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'

def post(message, image_url = None):
    payload = {"text": "{}".format(message)}
    if image_url is not None:
        payload['attachments'] = [{'fallback':'Overview of this weeks business.', 'image_url': image_url}]
    r = requests.post(url = slack_webhook_url, json = payload)
    return r.status_code, r.text