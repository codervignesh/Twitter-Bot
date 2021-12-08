import tweepy
import json
import requests
import logging
import random
import jokes

from tweepy.api import API
import Wallpaper
import time
import pyjokes

import time

from dotenv import load_dotenv
import os
load_dotenv()

consumer_key = os.getenv('consumer_key')
consumer_secret_key = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

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
        jo = j["setup"] + "\t\t\t\t" + j["punchline"]
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

    mentions1 = api.search(q, since_id = last_id, count=15)
    mentions2 = api.search(j, since_id = last_id, count=15)
    mentions3 = api.search(g, since_id = last_id, count=15)

    for mention in reversed(mentions1):
        logger.info(str(mention.id) + '-' + mention.text)
        new_id = mention.id

        logger.info("liking and replying to tweet")
        
        if '#quote' in mention.text.lower():
            logger.info("Responding back with QUOTE to -{}".format(mention.id))
            tweet = get_quote()

            try:

                status = api.get_status(mention.id)
                favorited = status.favorited 

                if(favorited == False):
                    api.create_favorite(mention.id)
                    print('Tweet Liked')
                print('If not tweet liked above tweet not liked')
            
            except tweepy.TweepError as e:
                print(e.reason)
                print("error so no like")

            try:

                logger.info("get wallpaper")
                Wallpaper.get_wallpaper(tweet)

                logger.info("upload image")
                media = api.media_upload("created_image.png")

                _status = '@' + mention.user.screen_name + " Here's a Quote:\n"
                api.update_status(status = _status, in_reply_to_status_id = mention.id, auto_populate_reply_metadata = True,
                                    media_ids=[media.media_id])
                time.sleep(120)
                print("wait 2mins")
            except:
                logger.info("Already replied to {}".format(mention.id))
        
    put_last_tweet(file, new_id)

    for mention in reversed(mentions2):
        logger.info(str(mention.id) + '-' + mention.text)
        new_id = mention.id

        if '#joke' in str(mention).lower():
            logger.info("Responding back with joke to -{}".format(mention.id))
            tweet = get_joke()

            try:
                status = api.get_status(mention.id)
                favorited = status.favorited 

                if(favorited == False):
                    api.create_favorite(mention.id)
                    print('Tweet Liked')
                print('If not tweet liked above tweet not liked')
            except tweepy.TweepError as e:
                print(e.reason)
                print("error so no like")

            try: 

                logger.info("get wallpaper")            
                Wallpaper.get_wallpaper(tweet)

                logger.info("upload image")
                media = api.media_upload("created_image.png")

                _status = '@' + mention.user.screen_name + " Here's a joke:\n"
                api.update_status(status = _status, in_reply_to_status_id = mention.id, auto_populate_reply_metadata = True,
                                    media_ids=[media.media_id])
                time.sleep(120)
                print("wait 2mins")
            except:
                logger.info("Already replied to {}".format(mention.id))
    put_last_tweet(file, new_id)

    for mention in reversed(mentions3):
        logger.info(str(mention.id) + '-' + mention.text)
        new_id = mention.id

        if '#geekjoke' in str(mention).lower():
            logger.info("Responding back with Geek joke to -{}".format(mention.id))
            tweet = get_geekjoke()

            try:
                status = api.get_status(mention.id)
                favorited = status.favorited 

                if(favorited == False):
                    api.create_favorite(mention.id)
                    print('Tweet Liked')
                print('If not tweet liked above tweet not liked')
            except tweepy.TweepError as e:
                print(e.reason)
                print("error so no like")

            try:

                logger.info("get wallpaper")
                Wallpaper.get_wallpaper(tweet)

                logger.info("upload image")
                media = api.media_upload("created_image.png")

                logger.info("liking and replying to tweet")

                api.create_favorite(mention.id)
                _status = '@' + mention.user.screen_name + " Here's a geek joke:\n"
                api.update_status(status = _status, in_reply_to_status_id = mention.id, auto_populate_reply_metadata = True,
                                    media_ids=[media.media_id])
                time.sleep(120)
                print("wait 2mins")

            except:
                logger.info("Already replied to {}".format(mention.id))


    put_last_tweet(file, new_id)

def main():
    respondToTweet()

# __name__
if __name__=="__main__":
    main()