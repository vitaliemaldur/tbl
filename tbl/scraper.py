import aiohttp
import asyncio
import feedparser
from bs4 import BeautifulSoup


class Scraper(object):
    """
    Class that implements basic scraper functionality
    """
    def __init__(self, name, url):
        """
        Scraper constructor
        :param name: Name of the scraper
        :param url: Url to the blog or rss feed
        """
        self.name = name
        self.url = url

    async def fetch_page(self, session):
        """
        Get a remote html/rss page
        :param session: session used to fetch the page
        :return:
        """
        with aiohttp.Timeout(10):
            headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X \
            10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.\
            103 Safari/537.36'}
            async with session.get(self.url, headers=headers) as response:
                assert response.status == 200
                return await response.read()

    async def get_links(self):
        """
        Get all links from a fetched page
        :return: a set of links from the page
        """
        loop = asyncio.get_event_loop()
        with aiohttp.ClientSession(loop=loop) as session:
            page = await self.fetch_page(session)
            feed = feedparser.parse(page)
            return {(item.link, item.title) for item in feed.entries}
