import json
import requests

base_url='localhost:7000'

def request(path, method="GET", body=None):
    body_json = json.dumps(body)
    response = requests.request(method=method, url=f"{base_url}/{path}")
    body = json.loads(response.text)
    return response.status_code, body