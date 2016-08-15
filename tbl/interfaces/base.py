import asyncio
import aiohttp


class BaseInterface(object):
    """
    Class that implements basic functionality for interface classes. These
    classes make the connection to social media platforms like Twitter and
    Facebook
    """
    def __init__(self, *args, **kwargs):
        self.session = aiohttp.ClientSession()

    async def bulk_post(self, messages):
        """
        Post messages in bulk through the interface to a specific social media
        platform
        :param messages: messages to post
        :return: a list of true and false values, value from position i show if
        message i was successfully posted or not
        """
        futures = [self.post(m) for m in messages]
        return await asyncio.gather(*futures)

    async def post(self, message, *args, **kwargs):
        """
        Post a message on a specific social media platform
        :param message: message to post
        :param args: other positional arguments
        :param kwargs: other keyword arguments
        :return: True if message was posted successfully otherwise False
        """
        raise NotImplementedError()

    def __del__(self):
        self.session.close()
