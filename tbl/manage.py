import asyncio
import aiohttp
import argparse
import os
import logging

from datetime import datetime
from tbl import db
from tbl.interfaces.twitter import TwitterInterface
from tbl.interfaces.facebook import FacebookInterface
from operator import or_
from functools import reduce
from tbl.scrapers import QuoraScraper, InstagramScraper, FacebookScraper, \
    UberScraper, DigitalOceanScraper, PinterestScraper, SpotifyScraper, \
    NetflixScraper, AirbnbScraper, PayPalScraper, TwitterScraper, \
    DropboxScraper, YoutubeScraper, SlackScraper, YelpScraper, \
    AtlassianScraper, GithubScraper, BufferScraper, YahooScraper


log = logging.getLogger(__name__)


# get facebook credentials
FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN')
FB_PAGE_ID = os.environ.get('FB_PAGE_ID')

# get twitter credentials
TW_CONSUMER_KEY = os.environ.get('TW_CONSUMER_KEY')
TW_CONSUMER_SECRET = os.environ.get('TW_CONSUMER_SECRET')
TW_ACCESS_TOKEN = os.environ.get('TW_ACCESS_TOKEN')
TW_ACCESS_TOKEN_SECRET = os.environ.get('TW_ACCESS_TOKEN_SECRET')

# init twitter interface
twitter = TwitterInterface(TW_CONSUMER_KEY, TW_CONSUMER_SECRET,
                           TW_ACCESS_TOKEN, TW_ACCESS_TOKEN_SECRET)

# init facebook interface
facebook = FacebookInterface(FB_ACCESS_TOKEN, FB_PAGE_ID)

# set available scrapers
SCRAPERS = [QuoraScraper, InstagramScraper, FacebookScraper, UberScraper,
            DigitalOceanScraper, PinterestScraper, SpotifyScraper,
            NetflixScraper, AirbnbScraper, PayPalScraper, TwitterScraper,
            DropboxScraper, YoutubeScraper, SlackScraper, YelpScraper,
            AtlassianScraper, GithubScraper, BufferScraper, YahooScraper]


async def get_all(session, scrapers):
    """
    Gets all the article links from the given list of scrappers
    :param session: aiohttp.ClientSession object
    :param scrapers: list of scrapers
    :return: list of sets of links
    """
    futures = [asyncio.ensure_future(scraper.get_links(session)) for scraper in
               scrapers]
    return await asyncio.gather(*futures)

async def test_scrapers(session, scrapers):
    """
    Test if all scrapers return a non-empty set of links
    :param session: aiohttp.ClientSession object
    :param scrapers: list of scrapers
    :return:
    """
    sets_of_links = await get_all(session, scrapers)
    for idx, links in enumerate(sets_of_links):
        is_ok = reduce(lambda acc, item: acc and len(item) == 2 and all(item),
                       links, True)
        status = 'ok' if len(links) > 0 and is_ok else 'not ok'
        log.info('{:.<50}[{status}]'.format(
            scrapers[idx].__name__,
            status=status))

async def post(session, platform='twitter'):
    """
    Post on social media
    :param session: aiohttp.ClientSession object
    :param platform: platform on which to post
    :return: True or False
    """
    document = await db.get_next_for_post()
    link = document['url']
    title = document['title'] if 'title' in document else None

    if platform == 'twitter':
        result = await twitter.post(session, link, title)
    elif platform == 'facebook':
        result = await facebook.post(session, link, title)
    else:
        log.error('Invalid platform')
        return False

    log.info('{link} posted: {result}'.format(link=link, result=result))

    # mark link as used
    if result:
        update_keys = {'posted_at': datetime.utcnow()}
        await db.update_post(document['_id'], update_keys)

    return result

async def get_and_save_all(session, scrapers):
    """
    Get all links to articles and save them in db
    :param session: aiohttp.ClientSession object
    :param scrapers: list of scrapers
    :return: documents from db
    """
    links = await get_all(session, scrapers)
    return await db.insert_urls(reduce(or_, links))

# setup arguments
parser = argparse.ArgumentParser(
    description='Fetch links, store and share them')
parser.add_argument('-t', '--test',  dest='test', action='store_true',
                    help='test available scrapers')
parser.add_argument('-p', '--post', type=str, choices=('facebook', 'twitter'),
                    help='post on social media')
parser.add_argument('-d', '--debug', help="enable debugging statements",
                    action="store_const", dest="loglevel", const=logging.DEBUG,
                    default=logging.INFO)

if __name__ == '__main__':
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
        if args.test:
            loop.run_until_complete(test_scrapers(session, SCRAPERS))

        if args.post:
            loop.run_until_complete(post(session, args.post))

        if not args.test and not args.post:
            loop.run_until_complete(get_and_save_all(session, SCRAPERS))
