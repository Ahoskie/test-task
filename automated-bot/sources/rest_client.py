import json
import aiohttp

from conf.settings import AUTH_SERVICE_API_URL, SOCIAL_NETWORK_SERVICE_API_URL, RANDOM_NAMES_API_URL


def get_auth_service_headers(bot):
    headers = {'Authorization': 'Bearer ' + bot.jwt_token}
    return headers


async def get_external_request(session: aiohttp.ClientSession, url, headers={}, **kwargs):
    try:
        response = await session.get(
            url,
            params=kwargs,
            headers=headers
        )
        status = response.status
        content = await response.json()
    except aiohttp.ClientResponseError:
        status = 502
        content = {}
    return status, content


async def post_external_request(session: aiohttp.ClientSession, url, headers={}, **kwargs):
    headers['Content-type'] = 'application/json'
    try:
        response = await session.post(
            url,
            data=json.dumps(kwargs),
            headers=headers
        )
        status = response.status
        content = await response.json()
    except aiohttp.ClientResponseError:
        status = 502
        content = {}
    return status, content


async def signup_request(bot):
    """
    Returns True if signup request is successful
    """
    url = AUTH_SERVICE_API_URL + 'signup/'
    status, _ = await post_external_request(bot.client_session, url, **bot.credentials)
    return status == 201


async def login_request(bot):
    """
    Returns token string if login request is successful
    """
    url = AUTH_SERVICE_API_URL + 'login/'
    status, content = await post_external_request(bot.client_session, url, **bot.credentials)
    if status == 200:
        return content['access']


async def create_post_request(bot, title: str, content: str):
    """
    Returns post id if request is successful
    """
    url = SOCIAL_NETWORK_SERVICE_API_URL + 'posts/'
    headers = get_auth_service_headers(bot)
    data = {
        'title': title,
        'content': content
    }
    status, content = await post_external_request(bot.client_session, url, headers=headers, **data)
    if status == 201:
        return content['id']


async def like_post_request(bot, post_id: int):
    """
    Returns True if the post was successfully liked
    """
    url = SOCIAL_NETWORK_SERVICE_API_URL + 'like-post/'
    headers = get_auth_service_headers(bot)
    data = {
        'post_id': post_id
    }
    status, _ = await post_external_request(bot.client_session, url, headers=headers, **data)
    if status == 200:
        return True


async def get_names(session: aiohttp.ClientSession, amount: int):
    url = RANDOM_NAMES_API_URL + str(amount)
    status, content = await get_external_request(session, url)
    if status == 200:
        return content
