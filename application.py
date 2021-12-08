from flask import Flask
import tweet_reply_me

import atexit
from apscheduler.schedulers.background import BackgroundScheduler

def job():
    tweet_reply_me.respondToTweet('tweet_id.txt')
    # To run reply_to_all.py
    # tweet_reply_all.respondToTweet('tweet_id.txt') 
    print("Success")

scheduler = BackgroundScheduler()
scheduler.add_job(func=job, trigger="interval", seconds=30)
scheduler.start() 

application = Flask(__name__)

@application.route("/")
def index():
    return "Github: https://github.com/codervignesh \n LinkedIn: https://www.linkedin.com/in/vignesh-r-/ "

atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    application.run(port=5000, debug=True)