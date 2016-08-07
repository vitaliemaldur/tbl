# Tech Blog Links
This is a scraper that will get links from a set of web pages and will post them on social media 

## Setup
  - Install `mongodb`
  - Install `python3.5` and just `python setup.py install`
  
If you want to contribute be sure that you:
  - install the package and requirements 
  
  ```bash
  pip install -r requirements-dev.txt
  python setup.py develop
  ```
  - run `flake8 .` in the root of the project and fix the errors, before pushing your changes


## Run
```bash
export FB_PAGE_ID=<your_fb_page_id> 
export FB_ACCESS_TOKEN=<your_fb_page_token>
export TW_CONSUMER_KEY=<your_twitter_consumer_key>
export TW_CONSUMER_SECRET=<your_twitter_consumer_secret>
export TW_ACCESS_TOKEN=<your_twitter_token>
export TW_ACCESS_TOKEN_SECRET=<your_twitter_token_secret>

python tbl/manage.py                #to fetch and store the links
python tbl/manage.py --post=twitter #to post a random link on twitter
python tbl/manage.py --test=true    #to test all available scrapers
```
  
## OAuth Tokens
  
### Facebook access token
Debug tool: https://developers.facebook.com/tools/debug/accesstoken

Steps to get the extended token:
  1. Go to [Graph Explorer](https://developers.facebook.com/tools/explorer/) and generate a user token with scope
  
  ```bash
  manage_pages,publish_pages
  ```

  2. Generate a extended user token
  
  ```bash
  curl -i -X GET "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={USER_TOKEN}"
  ```
  3. Take the access token from the response and go in graph explorer and request an page access token: `{PAGE_ID}?fields=access_token`
 
Check the token with the debug tool, should countain **Expires: Never**
  
### Twitter access tokens
  1. Go to [Twitter Application Manager](https://apps.twitter.com/) and create an app
  2. Generate access token using this [guide](https://dev.twitter.com/oauth/overview/application-owner-access-tokens)
  3. Go to Keys & Access Tokens tab on your new created app
