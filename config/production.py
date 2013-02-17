"""Production configuration (imported by __init__.py)"""
#!/usr/bin/python
# -*- coding: utf-8 -*-
import twitter
import twitter_tokens  # not git controlled

twitter_api = twitter.Api(consumer_key=twitter_tokens.CONSUMER_KEY,
                          consumer_secret=twitter_tokens.CONSUMER_SECRET,
                          access_token_key=twitter_tokens.ACCESS_TOKEN,
                          access_token_secret=twitter_tokens.ACCESS_TOKEN_SECRET)
