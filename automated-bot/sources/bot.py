from aiohttp import ClientSession


from rest_client import signup_request, login_request, create_post_request, like_post_request


class Bot:
    client_session = None

    def __init__(self, username, session: ClientSession, password='RaNd0m_pA$$', first_name='Bot', last_name='Bot'):
        self.credentials = {
            'username': username,
            'password': password,
            'first_name': first_name,
            'last_name': last_name
        }
        self.client_session = session
        self.jwt_token = None

        self.signed_up = False
        self.logged_in = False

        self.authored_posts_ids = []
        self._liked_posts_ids = []

    async def signup(self):
        self.signed_up = await signup_request(self)
        return self.signed_up

    async def login(self):
        self.jwt_token = await login_request(self)
        self.logged_in = self.jwt_token is not None
        return self.logged_in

    async def create_post(self, title: str, content: str):
        post_id = await create_post_request(self, title, content)
        if post_id:
            self.authored_posts_ids.append(post_id)
        return post_id

    async def like_post(self, post_id: int):
        successfully_liked = await like_post_request(self, post_id)
        if successfully_liked:
            self._liked_posts_ids.append(post_id)
        return successfully_liked
