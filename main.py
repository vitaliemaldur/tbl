import asyncio
import db
from operator import or_
from functools import reduce
from scrapers import *


SCRAPERS = [QuoraScraper, InstagramScraper, FacebookScraper, UberScraper,
            DigitalOceanScraper]

async def get_all_links(session, scrapers):
    futures = [asyncio.ensure_future(scraper.get_links(session)) for scraper in scrapers]
    links = await asyncio.gather(*futures)
    return await db.insert_urls(reduce(or_, links))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
        links = loop.run_until_complete(get_all_links(session, SCRAPERS))
        print(links)

