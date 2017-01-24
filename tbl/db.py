import asyncio
import logging

import motor.motor_asyncio


log = logging.getLogger(__name__)

# connect to mongodb
client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
# get posts collection
posts_collection = client['tbl']['posts']


async def insert_post(url, title, pub_date):
    """
    Insert an post in db
    :param url: url to insert
    :param title: title of article
    :param pub_date: publication date of the article
    :return: created document
    """
    document = await posts_collection.find_one({'url': {'$eq': url}})
    if not document:
        document = await posts_collection.insert({
            'url': url,
            'title': title,
            'published_at': pub_date,
            'posted_at': None
        })
        log.info('New URL found: %s', url)
    elif 'title' not in document or 'published_at' not in document:
        document = await update_post(document['_id'],
                                     {'title': title, 'published_at': pub_date})
        log.info('URL %s updated', document['url'])
    return document


async def insert_posts(posts):
    """
    Insert a list of (url, title)
    :param posts: list of (url, title, pub_date) to insert
    :return: a list of documents created
    """
    futures = [insert_post(url, title, pub_date)
               for url, title, pub_date in posts]
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


async def delete_posts(domain):
    """
    Delete all posts with a specific domain
    :param domain: domain of the blog
    :return: number of deleted documents
    """
    regex = '/{domain}/'.format(domain=domain)
    result = await posts_collection.delete_many({'url': {'$regex': regex}})
    log.info('Removed {} links'.format(result.deleted_count))
    return result.deleted_count


async def get_next_for_post():
    """
    Get a random document from db with an url that wasn't posted
    :return: the selected document
    """
    # select most recent post
    results = await posts_collection.find({
        'posted_at': None,
    }).sort('published_at', -1).to_list(1)

    # if not url found, log to console
    if not results:
        raise Exception('No url found to post')

    return results[0]
