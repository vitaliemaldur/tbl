import asyncio
from scrapers import *

SCRAPERS = [QuoraScraper, InstagramScraper, FacebookScraper, UberScraper,
            DigitalOceanScraper]

async def get_all_links(session, scrapers):
    links = set()
    for scraper in scrapers:
        links |= await scraper.get_links(session)
    return links


loop = asyncio.get_event_loop()
with aiohttp.ClientSession(loop=loop) as session:
    links = loop.run_until_complete(get_all_links(session, SCRAPERS))
    print(links)

