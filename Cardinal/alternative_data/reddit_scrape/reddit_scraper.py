import requests
import inspect
import yake
import pytrends
import traceback
import praw
import time
import json
import os
from dotenv import load_dotenv

load_dotenv() 

reddit = praw.Reddit(
    client_id=os.getenv('APP_ID'),
    client_secret=os.getenv('APP_SECRET'),
    password=os.getenv("password"),
    user_agent='test_test by u/ShakeOk5179',
    username=os.getenv("username"),
)

try:
    reddit.user.me()
except:
    print("verification failed")


reddit_sentiment=[]
recent_thread_comment_list=[]

for item in reddit.subreddit("wallstreetbets").hot(limit=2):
    try:
        post_dict={}
        post_dict["title"]=item.title
        post_dict["body"]=item.selftext
        post_dict["opinions"]=[]
        for j in item.comments:
            try:
                post_dict["opinions"].append(j.body)
            except Exception:
                traceback.print_exc()
        reddit_sentiment.append(post_dict)
        time.sleep(61)
    except Exception:
        traceback.print_exc()

with open("redditor.json", "w") as final:
   json.dump(reddit_sentiment, final)