import tweepy
from tweepy.api import API
import json
import requests
import logging
import time

import random
import jokes
import Wallpaper
import pyjokes

from dotenv import load_dotenv
import os
load_dotenv()

consumer_key = os.getenv('consumer_key')
consumer_secret_key = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) 

logger = logging.getLogger() 
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)

def get_quote():
    url = "https://api.quotable.io/random"

    response = {}    
    try:
        response = requests.get(url)
        res = json.loads(response.text)
        print(res)
        if res['length'] > 170:
            logger.info("Length exceded..")
            get_quote()
    except:
        logger.info("Error while calling API...")

    return res['content'] + "\n\t\t\t-" + res['author']


def get_joke():
    r = random.randrange(1,387)
    print(r)
    jo = ""
    try:
        j= jokes.joke[r]
        print(j)
        jo = j["setup"] + "\n\t\t\t\t" + j["punchline"]
        print(jo)
    except:
        get_joke()
    return jo 

def get_geekjoke():
    joke = pyjokes.get_joke(language="en", category="neutral")
    print(joke)
    return joke

def get_last_tweet(file):
    f = open(file, 'r')
    lastId = int(f.read().strip())
    f.close()
    return lastId


def put_last_tweet(file, Id):
    f = open(file, 'w')
    f.write(str(Id))
    f.close()
    logger.info("Updated the file with the latest tweet Id")
    return


def respondToTweet(file='tweet_id.txt'):
    last_id = get_last_tweet(file)

    q = "#quote"
    j = "#joke"
    g = "#geekjoke"
    new_id = 0

    mentions = api.mentions_timeline(since_id = last_id, tweet_mode='extended')
    
    logger.info("someone mentioned me...")

    if len(mentions) == 0:
        return

    for mention in reversed(mentions):
        logger.info(str(mention.id) + '-' + mention.full_text)
        new_id = mention.id

        logger.info("liking and replying to tweet")
        
        if '#joke' in mention.full_text.lower():
            try:
                api.create_favorite(mention.id)
                print('Tweet Liked')
            except tweepy.TweepError as e:
                print(e.reason)
                print("error so no like")

        if '#geekjoke' in mention.full_text.lower():
            try:
                api.create_favorite(mention.id)
                print('Tweet Liked')
            except tweepy.TweepError as e:
                print(e.reason)
                print("error so no like")

        if '#quote' in mention.full_text.lower():
            try:                
                api.create_favorite(mention.id)
                print('Tweet Liked')
            except tweepy.TweepError as e:
                print(e.reason)
                print("error so no like")

        if '#joke' in mention.full_text.lower():
            logger.info("Responding back with joke to -{}".format(mention.id))
            tweet = get_joke()

            try: 
                logger.info("get wallpaper")            
                Wallpaper.get_wallpaper(tweet)

                logger.info("upload image")
                media = api.media_upload("created_image.png")

                _status = '@' + mention.user.screen_name + " Here's a joke:\n"
                api.update_status(status = _status, in_reply_to_status_id = mention.id, auto_populate_reply_metadata = True,
                                    media_ids=[media.media_id])
                time.sleep(30)
            except:
                logger.info("Already replied to {}".format(mention.id))

        if '#geekjoke' in mention.full_text.lower():
            logger.info("Responding back with Geek joke to -{}".format(mention.id))
            tweet = get_geekjoke()
            try:
                logger.info("get wallpaper")
                Wallpaper.get_wallpaper(tweet)

                logger.info("upload image")
                media = api.media_upload("created_image.png")

                _status = '@' + mention.user.screen_name + " Here's a geek joke:\n"
                api.update_status(status = _status, in_reply_to_status_id = mention.id, auto_populate_reply_metadata = True,
                                    media_ids=[media.media_id])
                time.sleep(30)
            except:
                logger.info("Already replied to {}".format(mention.id))

        
        if '#quote' in mention.full_text.lower():
            logger.info("Responding back with QUOTE to -{}".format(mention.id))
            tweet = get_quote()
            try:
                logger.info("get wallpaper")
                Wallpaper.get_wallpaper(tweet)

                logger.info("upload image")
                media = api.media_upload("created_image.png")

                _status = '@' + mention.user.screen_name + " Here's a Quote\n"
                api.update_status(status = _status, in_reply_to_status_id = mention.id, auto_populate_reply_metadata = True,
                                    media_ids=[media.media_id])
                time.sleep(30)
            except:
                logger.info("Already replied to {}".format(mention.id))

    put_last_tweet(file, new_id)

def main():
    respondToTweet()

# __name__
if __name__=="__main__":
    main()