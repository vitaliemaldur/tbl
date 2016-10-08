from urllib.parse import quote_plus
from tbl.interfaces.base import BaseInterface


class FacebookInterface(BaseInterface):
    """
    Class for posting on Facebook
    """
    api_url = 'https://graph.facebook.com/v2.7/{page_id}/feed?' \
              'message={message}&link={link}&access_token={access_token}'

    def __init__(self, token, page_id):
        """
        Constructor
        :param token: API token
        :param page_id: Page ID
        """
        self.token = token
        self.page_id = page_id
        super().__init__()

    async def post(self, session, link, message=None):
        """
        Post a link with a message on Facebook page
        :param session: aiohttp.ClientSession object
        :param link: link to post
        :param message: message to post
        :return: True if message was posted successfully otherwise False
        """
        url = self.api_url.format(
            page_id=self.page_id,
            message=quote_plus(message or ''),
            link=quote_plus(link),
            access_token=self.token,
        )

        async with session.post(url) as resp:
            return resp.status == 200
