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


async def insert_url(url, title):
    """
    Insert an url in db
    :param url: url to insert
    :param title: title of article
    :return: created document
    """
    document = await posts_collection.find_one({'url': {'$eq': url}})
    if not document:
        document = await posts_collection.insert({
            'url': url,
            'title': title,
            'created_at': datetime.utcnow(),
            'posted_at': None,
            '_random_value': random.random(),
        })
        log.info('New URL found: %s', url)
    elif 'title' not in document:
        document = await update_post(document['_id'], {'title': title})
    return document

async def insert_urls(urls):
    """
    Insert a list of (url, title)
    :param urls: list of (url, title) to insert
    :return: a list of documents created
    """
    futures = [insert_url(url, title) for url, title in urls]
    return await asyncio.gather(*futures)

async def update_post(pk, keys):
    """
    Update a document
    :param pk: pk of the document
    :param keys: dict with keys to update
    :return: updated document
    """
    result = await posts_collection.update({'_id': pk}, {'$set': keys})
    if not result.get('ok'):
        raise Exception('Document _id={} not updated'.format(pk))
    return await posts_collection.find_one({'_id': pk})

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
        raise Exception('No url found to post')

    return results[0]
