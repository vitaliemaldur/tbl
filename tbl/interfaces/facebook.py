from urllib.parse import quote_plus
from tbl.interfaces.base import BaseInterface


class FacebookInterface(BaseInterface):
    """
    Class for posting on Facebook
    """
    api_url = 'https://graph.facebook.com/v2.7/{page_id}/feed?message={message}\
    &link={link}&access_token={access_token}'

    def __init__(self, token, page_id):
        """
        Constructor
        :param token: API token
        :param page_id: Page ID
        """
        self.token = token
        self.page_id = page_id
        super().__init__()

    async def post(self, message, *args, **kwargs):
        """
        Post a message on Facebook page
        :param message: message to post
        :param args: other positional arguments
        :param kwargs: other keyword arguments
        :return: True if message was posted successfully otherwise False
        """
        url = self.api_url.format(
            page_id=self.page_id,
            message=quote_plus(kwargs.get('message', '')),
            link=quote_plus(message),
            access_token=self.token,
        )

        with self.session as session:
            async with session.post(url) as resp:
                return resp.status == 200
