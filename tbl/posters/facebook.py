import os 
import aiohttp

from urllib.parse import quote_plus


# get facebook page access token and page id from env
FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN')
FB_PAGE_ID = os.environ.get('FB_PAGE_ID') 

API_URL = 'https://graph.facebook.com/v2.7/{page_id}/feed?message={message}&link={link}&access_token={access_token}'


async def post(link, message=''):
    url = API_URL.format(
        page_id=FB_PAGE_ID, 
        message=quote_plus(message),
        link=quote_plus(link),
        access_token=FB_ACCESS_TOKEN,
    )

    async with aiohttp.ClientSession() as session:
        async with session.post(url) as resp:
            print(resp.status)
            print(await resp.text())

