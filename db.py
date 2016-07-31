import asyncio
import motor.motor_asyncio
from datetime import datetime


client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
db = client['links']
posts_collection = db['posts']


async def insert_url(url):
    document = await posts_collection.find_one({'url': {'$eq': url}})
    if not document:
        document = await posts_collection.insert({
            'url': url,
            'created_at': datetime.now()
        })
    return document

async def insert_urls(urls):
    futures = [insert_url(url) for url in urls]
    return await asyncio.gather(*futures)
