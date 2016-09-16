import base64
import hmac
import operator
import time
import uuid
from hashlib import sha1
from urllib.parse import quote, urlencode

from tbl.interfaces.base import BaseInterface


class TwitterInterface(BaseInterface):
    """
    Class for posting on Twitter
    """
    api_url = 'https://api.twitter.com/1.1/statuses/update.json'

    def __init__(self, consumer_key, consumer_secret, token,
                 token_secret):
        """
        Constructor
        :param consumer_key: consumer key
        :param consumer_secret: consumer secret
        :param token: API token
        :param token_secret: API token secret
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.token = token
        self.token_secret = token_secret
        super().__init__()

    def get_signature(self, method, api_url, tweet, timestamp, unique):
        """
        Get signature for the API call
        :param method: http method POST/GET/PUT ...
        :param api_url: API url that will be called
        :param tweet: message to post
        :param timestamp: timestamp in seconds
        :param unique: unique id
        :return: the signature for the API call
        """
        params = {
            'status': tweet,
            'oauth_consumer_key': self.consumer_key,
            'oauth_nonce': unique,
            'oauth_signature_method': 'HMAC-SHA1',
            'oauth_timestamp': timestamp,
            'oauth_token': self.token,
            'oauth_version': '1.0'
        }
        # sort parameters using after the keys
        params = sorted(params.items(), key=operator.itemgetter(0))

        # create base string for hashing
        base_string = '{method}&{url}&{params}'.format(
            method=quote(method.upper(), safe=''),
            url=quote(api_url, safe=''),
            params=quote(urlencode(params, safe='~', quote_via=quote),
                         safe='~')
        ).encode('utf8')

        # create signing key
        signature_key = '{consumer_key}&{token_secret}'.format(
            consumer_key=quote(self.consumer_secret, safe=''),
            token_secret=quote(self.token_secret, safe='')
        ).encode('utf8')

        hashed = hmac.new(signature_key, base_string, sha1).digest()
        return base64.b64encode(hashed).decode('utf8')

    async def post(self, session, link, message=None):
        """
        Post a link with a message on Twitter
        :param session: aiohttp.ClientSession object
        :param link: link to post
        :param message: message to post
        :return: True if message was posted successfully otherwise False
        """
        timestamp = int(time.time())
        unique = str(uuid.uuid4())

        if message:
            tweet = '{message} {link}'.format(message=message, link=link)
        else:
            tweet = link

        # get the signature
        signature = self.get_signature('POST', self.api_url, tweet,
                                       timestamp, unique)

        # build auth header
        oauth = 'OAuth oauth_consumer_key="{oauth_consumer_key}",\
        oauth_nonce="{oauth_nonce}",\
        oauth_signature="{oauth_signature}",\
        oauth_signature_method="{oauth_signature_method}",\
        oauth_timestamp="{oauth_timestamp}",\
        oauth_token="{oauth_token}",\
        oauth_version="{oauth_version}"'.format(
            oauth_consumer_key=quote(self.consumer_key, safe=''),
            oauth_nonce=quote(unique, safe=''),
            oauth_signature=quote(signature, safe=''),
            oauth_signature_method=quote('HMAC-SHA1', safe=''),
            oauth_timestamp=quote(str(timestamp), safe=''),
            oauth_token=quote(self.token, safe=''),
            oauth_version=quote("1.0", safe='')
        )

        headers = {'Authorization': oauth}
        data = urlencode({'status': tweet}, safe='~', quote_via=quote)
        url = '{base_url}?{data}'.format(base_url=self.api_url, data=data)

        async with session.post(url, headers=headers) as resp:
            return resp.status == 200
