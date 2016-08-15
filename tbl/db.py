import asyncio
import random
import logging
from datetime import datetime

import motor.motor_asyncio


log = logging.getLogger(__name__)

# connect to mongodb
client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
# get posts collection
posts_collection = client['tbl']['posts']


async def insert_url(url):
    """
    Insert an url in db
    :param url: url to insert
    :return: created document
    """
    document = await posts_collection.find_one({'url': {'$eq': url}})
    if not document:
        document = await posts_collection.insert({
            'url': url,
            'created_at': datetime.utcnow(),
            'posted_at': None,
            '_random_value': random.random(),
        })
        log.info('New URL found: %s', url)

    return document

async def insert_urls(urls):
    """
    Insert a list of urls
    :param urls: list of urls to insert
    :return: a list of documents created
    """
    futures = [insert_url(url) for url in urls]
    return await asyncio.gather(*futures)

async def update_posts(pk, keys):
    """
    Update a document
    :param pk: pk of the document
    :param keys: dict with keys to update
    :return:
    """
    result = await posts_collection.update({'_id': pk}, keys)
    if not result.get('ok'):
        log.error('Document %s was not updated', pk)

async def get_next_for_post():
    """
    Get a random document from db with an url that wasn't posted
    :return: the selected document
    """
    # select first random document
    results = await posts_collection.find({
        'posted_at': None,
    }).sort('_random_value').to_list(1)

    # if not url found, log to console
    if not results:
        log.warning('No url found to post')
        return

    return results[0]
