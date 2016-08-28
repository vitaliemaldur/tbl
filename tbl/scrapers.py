import aiohttp
import feedparser
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class BaseScraper(object):
    """
    Class that implments basic functionality for scraper classes
    """
    url = None

    @classmethod
    async def fetch_page(cls, session):
        """
        Get a remote html/rss page
        :param session: session used to fetch the page
        :return:
        """
        with aiohttp.Timeout(10):
            headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X \
            10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.\
            103 Safari/537.36'}
            async with session.get(cls.url, headers=headers) as response:
                assert response.status == 200
                return await response.read()

    @classmethod
    async def get_links(cls, session):
        """
        Get all links from a fetched page
        :param session: session used to fetch the page
        :return: a set of links from the page
        """
        page = await cls.fetch_page(session)
        feed = feedparser.parse(page)
        return {(item.link, item.title) for item in feed.entries}


class QuoraScraper(BaseScraper):
    url = 'https://engineering.quora.com/'

    @classmethod
    async def get_links(cls, session):
        page = BeautifulSoup(await cls.fetch_page(session), 'html.parser')
        links = page.find_all('a', class_='BoardItemTitle')
        return {(a['href'], a.strong.span.p.text) for a in links}


class FacebookScraper(BaseScraper):
    url = 'https://code.facebook.com/posts/rss'


class DigitalOceanScraper(BaseScraper):
    url = 'https://www.digitalocean.com/company/blog/'

    @classmethod
    async def get_links(cls, session):
        page = BeautifulSoup(await cls.fetch_page(session), 'html.parser')
        return {(urljoin(cls.url, a['href']), a.text) for a in
                page.select('article > h2 > a')}


class InstagramScraper(BaseScraper):
    url = 'https://engineering.instagram.com/feed'


class UberScraper(BaseScraper):
    url = 'https://eng.uber.com/feed/'


class PinterestScraper(BaseScraper):
    url = 'https://engineering.pinterest.com/blog/rss'


class SpotifyScraper(BaseScraper):
    url = 'https://labs.spotify.com/feed/'


class NetflixScraper(BaseScraper):
    url = 'http://techblog.netflix.com/feeds/posts/default'


class AirbnbScraper(BaseScraper):
    url = 'http://nerds.airbnb.com/feed/'


class PayPalScraper(BaseScraper):
    url = 'https://www.paypal-engineering.com/feed/'


class TwitterScraper(BaseScraper):
    url = 'https://blog.twitter.com/api/blog.rss?name=engineering'


class DropboxScraper(BaseScraper):
    url = 'https://blogs.dropbox.com/tech/feed/'


class YoutubeScraper(BaseScraper):
    url = 'https://youtube-eng.blogspot.com/feeds/posts/default?alt=rss'


class SlackScraper(BaseScraper):
    url = 'https://medium.com/feed/slack-developer-blog'


class AtlassianScraper(BaseScraper):
    url = 'https://developer.atlassian.com/blog/feed.xml'


class GithubScraper(BaseScraper):
    url = 'http://githubengineering.com/atom.xml'


class BufferScraper(BaseScraper):
    url = 'https://overflow.buffer.com/feed/'


class YahooScraper(BaseScraper):
    url = 'https://yahooeng.tumblr.com/rss'


class YelpScraper(BaseScraper):
    url = 'http://engineeringblog.yelp.com/feed.xml'
