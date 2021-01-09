import random

from aiohttp import ClientSession
import asyncio

from bot import Bot
from exceptions import BotsBuilderError
from rest_client import get_names


async def arange(count):
    for i in range(count):
        yield i


class BotsBuilder:
    bots = []
    posts_ids = []

    def __init__(self, session: ClientSession, bots_count, max_posts_per_bot, max_likes_per_bot):
        self.session = session
        self.bots_count = bots_count
        self.max_posts_per_bot = max_posts_per_bot
        self.max_likes_per_bot = max_likes_per_bot

    async def create_bots(self):
        names = await get_names(self.session, self.bots_count)
        if not names:
            raise BotsBuilderError('Builder could not get names for bots from external service.')
        for i in range(self.bots_count):
            bot = Bot(username=names[i], session=self.session)
            bot.posts_amount = random.randint(0, self.max_posts_per_bot)
            bot.likes_amount = random.randint(1, self.max_likes_per_bot)
            self.bots.append(bot)

    async def signup_bots(self):
        for bot in self.bots:
            await bot.signup()

    async def login_bots(self):
        for bot in self.bots:
            await bot.login()

    async def create_posts(self):
        for bot in self.bots:
            if bot.logged_in:
                async for i in arange(bot.posts_amount):
                    await asyncio.sleep(1)  # Wait some time before the next request
                    await bot.create_post(f'Hello, my name is {bot.credentials.get("username")}', content='My post!')
                self.posts_ids += bot.authored_posts_ids

    async def like_posts(self):
        for bot in self.bots:
            posts_to_like = set(random.choices(self.posts_ids, k=bot.likes_amount))
            for post_id in posts_to_like:
                await bot.like_post(post_id)


