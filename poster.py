import asyncio
import logging
import os
from datetime import datetime

from tbl import db
from tbl.posters.twitter import TwitterPoster


log = logging.getLogger(__name__)

# get facebook credentials
FB_ACCESS_TOKEN = os.environ.get('FB_ACCESS_TOKEN')
FB_PAGE_ID = os.environ.get('FB_PAGE_ID')

# get twetter credentials
TW_CONSUMER_KEY = os.environ.get('TW_CONSUMER_KEY')
TW_CONSUMER_SECRET = os.environ.get('TW_CONSUMER_SECRET')
TW_ACCESS_TOKEN = os.environ.get('TW_ACCESS_TOKEN')
TW_ACCESS_TOKEN_SECRET = os.environ.get('TW_ACCESS_TOKEN_SECRET')

twitter = TwitterPoster(TW_CONSUMER_KEY, TW_CONSUMER_SECRET,
                        TW_ACCESS_TOKEN, TW_ACCESS_TOKEN_SECRET)

async def main():
    document = await db.get_next_for_post()
    link = document['url']

    result = await twitter.post(link)
    log.info("{link} posted: {result}".format(link=link, result=result))

    # mark link as used
    if result:
        update_keys = {'posted_at': datetime.utcnow()}
        await db.update_posts(document['_id'], update_keys)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
