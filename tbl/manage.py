import asyncio
import json
import argparse
import os
import logging

from datetime import datetime
from functools import reduce
from operator import or_
from urllib.parse import urlparse

import aiohttp

from tbl import db
from tbl.interfaces.twitter import TwitterInterface
from tbl.interfaces.facebook import FacebookInterface
from tbl.scraper import Scraper


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


async def get_all(blogs_config):
    """
    Gets all the article posts from the given list of blogs
    :param blogs_config: list of configurations for blogs
    :return: list of sets of links
    """
    scrapers = []
    for blog in blogs_config:
        scrapers.append(Scraper(name=blog['name'], url=blog['url']))

    futures = [asyncio.ensure_future(s.get_posts()) for s in scrapers]
    return await asyncio.gather(*futures)


async def test_scrapers(blogs_config):
    """
    Test if all configurations return a non-empty set of posts
    :param blogs_config: list of configurations for blogs
    :return:
    """
    sets_of_posts = await get_all(blogs_config)
    for idx, links in enumerate(sets_of_posts):
        is_ok = reduce(lambda acc, item: acc and len(item) == 3 and all(item),
                       links, True)
        status = 'ok' if len(links) > 0 and is_ok else 'not ok'
        log.info('{:.<50}[{status}]'.format(blogs_config[idx]['name'],
                                            status=status))


async def post(platform='twitter'):
    """
    Post on social media
    :param platform: platform on which to post
    :return: True or False
    """
    document = await db.get_next_for_post()
    link = document['url']
    title = document['title'] if 'title' in document else None

    loop = asyncio.get_event_loop()
    with aiohttp.ClientSession(loop=loop) as session:
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


async def remove(blogs_config, blog_name):
    """
    Remove all the links of the specified scraper
    :param blogs_config: list of configurations for blogs
    :param blog_name: blog name
    :return: number of removed urls
    """
    for blog in blogs_config:
        if blog['name'] == blog_name:
            parsed_url = urlparse(blog['url'])
            result = await db.delete_posts(parsed_url.netloc)
            return result

    log.error('Invalid base url')
    return 0


async def get_and_save_all(blogs_config):
    """
    Get all posts and save them in db
    :param blogs_config: list of configurations for blogs
    :return: documents from db
    """
    posts = await get_all(blogs_config)
    return await db.insert_posts(reduce(or_, posts))

# setup arguments
parser = argparse.ArgumentParser(
    description='Fetch links, store and share them')
parser.add_argument('-f', '--file', dest='file', required=True,
                    help='Configuration file for the script',
                    type=argparse.FileType('r', encoding='UTF-8'))
parser.add_argument('-t', '--test', dest='test', action='store_true',
                    help='test available scrapers')
parser.add_argument('-p', '--post', type=str, choices=('facebook', 'twitter'),
                    help='post on social media')
parser.add_argument('-r', '--remove', type=str, dest='remove',
                    help='remove all links of a specific scraper')
parser.add_argument('-d', '--debug', help="enable debugging statements",
                    action="store_const", dest="loglevel", const=logging.DEBUG,
                    default=logging.INFO)

if __name__ == '__main__':
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    loop = asyncio.get_event_loop()

    with args.file as config_file:
        blogs_config = json.load(config_file)

        if args.test:
            loop.run_until_complete(test_scrapers(blogs_config))

        if args.post:
            loop.run_until_complete(post(args.post))

        if args.remove:
            loop.run_until_complete(remove(blogs_config, args.remove))

        if not any((args.test, args.post, args.remove)):
            loop.run_until_complete(get_and_save_all(blogs_config))
