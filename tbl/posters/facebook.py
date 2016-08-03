from urllib.parse import quote_plus
from tbl.posters.base import BasePoster


class FacebookPoster(BasePoster):
    api_url = 'https://graph.facebook.com/v2.7/{page_id}/feed?message={message}&link={link}&access_token={access_token}'

    def __init__(self, token, page_id):
        self.token = token
        self.page_id = page_id
        super().__init__()

    async def post(self, link, *args, **kwargs):
        url = self.api_url.format(
            page_id=self.page_id,
            message=quote_plus(kwargs.get('message', '')),
            link=quote_plus(link),
            access_token=self.token,
        )

        with self.session as session:
            async with session.post(url) as resp:
                return resp.status == 200

