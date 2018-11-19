# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 11:57:48 2018

@author: rarossi
"""
import json
from tweepy import OAuthHandler, Stream, API
from tweepy.streaming import StreamListener

api_key = 'bO2FyX6SZJbC3dz6B0DQJZYRM'
api_key_secret = 'Jo94xuUGcBwu4x9eaNlBWjN9deH9kpKnpwCv1TbvJ6vLRkyvVS'
access_token = '1062654999874945025-6UjG392Ed3xJW0YJr7OmgXdnMZIIma'
access_token_secret = 'wMk3lVpVpzCTGtBfaFZENbV2kATrb3vCqdmmjznNeBZ8J'

auth = OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)


class PrintListener(StreamListener):
    def on_status(self, status):
        if not status.text[:3] == 'RT ':
            print(status.text)
            print(status.author.screen_name,
                  status.created_at,
                  status.source,
                  '\n')

    def on_error(self, status_code):
        print('Error code: {}'.format(status_code))
        return True  # keep stream alive

    def on_timeout(self):
        print('Listener timed out.')
        return True  # keep it alive


def print_to_terminal():
    listener = PrintListener()
    stream = Stream(auth, listener)
    languages = ('en',)
    stream.sample(languages=languages)


def pull_down_tweets(screen_name):
    api = API(auth)
    tweets = api.user_timeline(screen_name=screen_name, count=200)
    for tweet in tweets:
        print(json.dumps(tweet._json, indent=4))


if __name__ == '__main__':
    # print_to_terminal()
    # pull_down_tweets(auth.username)
    pull_down_tweets('RafaelRossi')

