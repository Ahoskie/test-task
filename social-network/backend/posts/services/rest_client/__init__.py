import json
import requests


def get_external_request(url, headers, **kwargs):
    try:
        response = requests.get(
            url,
            kwargs,
            headers=headers
        )
        status = response.status_code
        content = json.loads(response.content)
    except requests.exceptions.ConnectionError:
        status = 502
        content = {}
    return status, content


def post_external_request(url, headers, **kwargs):
    headers['Content-type'] = 'application/json'
    try:
        response = requests.post(
            url,
            data=json.dumps(kwargs),
            headers=headers
        )
        status = response.status_code
        content = json.loads(response.content)
    except requests.exceptions.ConnectionError:
        status = 502
        content = {}
    return status, content
