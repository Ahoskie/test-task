import asyncio
import aiohttp

from exceptions import BotsBuilderError
from bots_builder import BotsBuilder
from conf.settings import NUMBER_OF_USERS, MAX_POSTS_PER_USER, MAX_LIKES_PER_USER


async def main():
    session = aiohttp.ClientSession()
    try:
        bot_builder = BotsBuilder(session, NUMBER_OF_USERS, MAX_POSTS_PER_USER, MAX_LIKES_PER_USER)
        print('Creating bots objects...')
        await bot_builder.create_bots()
        print('Signing up bots...')
        await bot_builder.signup_bots()
        print('Getting tokens for bots...')
        await bot_builder.login_bots()
        print('Creating posts for bots...')
        await bot_builder.create_posts()
        print('Setting likes to posts...')
        await bot_builder.like_posts()
    except BotsBuilderError as e:
        print(e.message)
    await session.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
