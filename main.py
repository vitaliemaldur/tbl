import asyncio
import aiohttp
from bs4 import BeautifulSoup


class BaseScraper(object):
    url = None

    @classmethod
    async def fetch_page(cls, session):
        with aiohttp.Timeout(10):
            async with session.get(cls.url) as response:
                assert response.status == 200
                return await response.read()

    @classmethod
    async def get_links(cls, session):
        page = await cls.fetch_page(session)
        soup = BeautifulSoup(page, 'html.parser')
        return [a['href'] for a in soup.find_all('a', href=True)]


class QuoraScraper(BaseScraper):
    url = 'https://blog.quora.com'

    @classmethod
    async def get_links(cls, session):
        content = await cls.fetch_page(session)
        soup = BeautifulSoup(content, 'html.parser')
        return [a['href'] for a in soup.find_all('a', class_='BoardItemTitle')]



SCRAPERS = [QuoraScraper]

loop = asyncio.get_event_loop()
with aiohttp.ClientSession(loop=loop) as session:
    for scraper in SCRAPERS:
        links = loop.run_until_complete(scraper.get_links(session))
        print(links)

