import asyncio
import logging
from datetime import datetime

from tbl.db import get_next_for_post, update_posts
from tbl.posters import facebook


log = logging.getLogger(__name__)

async def main():
    document = await get_next_for_post()

    link = document['url']
    print ('Next to post is this url:', link)

    # post to social networks
    # TODO: add other social posters
    await facebook.post(link)

    # mark link as used
    await update_posts(document['_id'], {'posted_at': datetime.utcnow()})


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

