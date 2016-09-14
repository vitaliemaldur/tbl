import asyncio


class BaseInterface(object):
    """
    Class that implements basic functionality for interface classes. These
    classes make the connection to social media platforms like Twitter and
    Facebook
    """

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

    async def post(self, session, link, message=None):
        """
        Post a link with a message on a specific social media platform
        :param session: aiohttp.ClientSession object
        :param link: link to post
        :param message: message to post
        :return: True if message was posted successfully otherwise False
        """
        raise NotImplementedError()
