from config.settings import AUTH_SERVICE_URL, WEB_SERVICE_JWT
from . import post_external_request


def get_auth_service_headers():
    headers = {'Authorization': 'Bearer ' + WEB_SERVICE_JWT}
    return headers


def is_user_token_valid(token):
    headers = get_auth_service_headers()
    url = AUTH_SERVICE_URL + 'api/verify-token/'
    status, _ = post_external_request(url, headers, token=token)
    return status == 200


def get_users_info(users_ids: list):
    headers = get_auth_service_headers()
    url = AUTH_SERVICE_URL + 'api/users-info/'
    status, content = post_external_request(url, headers, users_ids=users_ids)
    if status == 200:
        return content['users']
    return None
