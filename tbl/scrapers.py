import aiohttp
from urllib.parse import urljoin
from bs4 import BeautifulSoup, Comment


class BaseScraper(object):
    url = None
    rss = False

    @classmethod
    async def fetch_page(cls, session):
        with aiohttp.Timeout(10):
            headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X \
            10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.\
            103 Safari/537.36'}
            parser = 'html.parser' if not cls.rss else 'xml'
            async with session.get(cls.url, headers=headers) as response:
                assert response.status == 200
                return BeautifulSoup(await response.read(), parser)

    @classmethod
    async def get_links(cls, session):
        page = await cls.fetch_page(session)
        if cls.rss:
            return {item.link.text for item in page.find_all('item')}
        return {a['href'] for a in page.find_all('a', href=True)}


class QuoraScraper(BaseScraper):
    url = 'https://engineering.quora.com/'

    @classmethod
    async def get_links(cls, session):
        page = await cls.fetch_page(session)
        return {a['href'] for a in page.find_all('a', class_='BoardItemTitle')}


class InstagramScraper(BaseScraper):
    url = 'https://engineering.instagram.com/'

    @classmethod
    async def get_links(cls, session):
        page = await cls.fetch_page(session)
        return {a['href'] for a in page.select('article > a')}


class FacebookScraper(BaseScraper):
    url = 'https://developers.facebook.com/blog/'

    @classmethod
    async def get_links(cls, session):
        page = await cls.fetch_page(session)
        links = set()
        for comment in page.findAll(
                text=lambda text: isinstance(text, Comment)):
            html = BeautifulSoup(comment.extract(), 'html.parser')
            links |= {a['href'] for a in html.find_all('a') if
                      cls.url in a['href']}
        return links


class UberScraper(BaseScraper):
    url = 'https://eng.uber.com/'

    @classmethod
    async def get_links(cls, session):
        page = await cls.fetch_page(session)
        return {span.a['href'] for span in
                page.find_all('span', class_='post_link')}


class DigitalOceanScraper(BaseScraper):
    url = 'https://www.digitalocean.com/company/blog/'

    @classmethod
    async def get_links(cls, session):
        page = await cls.fetch_page(session)
        return {urljoin(cls.url, a['href']) for a in
                page.select('article > h2 > a')}
