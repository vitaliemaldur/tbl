import asyncio
import aiohttp


class BasePoster(object):

    def __init__(self, *args, **kwargs):
        self.session = aiohttp.ClientSession()

    async def bulk_post(self, messages):
        futures = [self.post(m) for m in messages]
        return await asyncio.gather(*futures)

    async def post(self, link, *args, **kwargs):
        raise NotImplementedError()
