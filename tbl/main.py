import asyncio
import os
from tbl import db
from operator import or_
from functools import reduce
from tbl.scrapers import QuoraScraper, InstagramScraper, FacebookScraper, \
    UberScraper, DigitalOceanScraper
from tbl.posters.twitter import TwitterPoster

# get facebook credentials
FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN')
FB_PAGE_ID = os.environ.get('FB_PAGE_ID')

# get twetter credentials
TW_CONSUMER_KEY = os.environ.get('TW_CONSUMER_KEY')
TW_CONSUMER_SECRET = os.environ.get('TW_CONSUMER_SECRET')
TW_ACCESS_TOKEN = os.environ.get('TW_ACCESS_TOKEN')
TW_ACCESS_TOKEN_SECRET = os.environ.get('TW_ACCESS_TOKEN_SECRET')

twitter = TwitterPoster(TW_CONSUMER_KEY, TW_CONSUMER_SECRET,
                        TW_ACCESS_TOKEN, TW_ACCESS_TOKEN_SECRET)

SCRAPERS = [QuoraScraper, InstagramScraper, FacebookScraper, UberScraper,
            DigitalOceanScraper]


async def get_all_links(session, scrapers):
    futures = [asyncio.ensure_future(scraper.get_links(session)) for scraper in
               scrapers]
    links = await asyncio.gather(*futures)
    return await db.insert_urls(reduce(or_, links))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    links = loop.run_until_complete(twitter.post('Test'))
    print(links)
