import tweepy
import pandas as pd 
import json
from datetime import datetime
import twitter_api

def run_twitter_etl(screen_name='@elonmusk'):

    access_key = twitter_api.access_key
    access_secret = twitter_api.access_secret
    consumer_key = twitter_api.consumer_key
    consumer_secret = twitter_api.consumer_secret


    # Twitter authentication
    auth = tweepy.OAuthHandler(access_key, access_secret)   
    auth.set_access_token(consumer_key, consumer_secret) 

    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name=screen_name, 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = False,
                            tweet_mode = 'extended'
                            )

    list = []
    for tweet in tweets:
        text = tweet._json["full_text"]

        refined_tweet = {"user": tweet.user.screen_name,
                        'text' : text,
                        'favorite_count' : tweet.favorite_count,
                        'retweet_count' : tweet.retweet_count,
                        'created_at' : tweet.created_at}
        
        list.append(refined_tweet)

    df = pd.DataFrame(list)
    df.to_csv('s3://airflow-project-bucket/refined_tweets.csv')
