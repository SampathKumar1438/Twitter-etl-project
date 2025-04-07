import tweepy
import pandas as pd 
import json
from datetime import datetime
import s3fs 

def run_twitter_etl():

    access_key = "qh5nJpRJhnDLpFzKowNLUFESg" 
    access_secret = "0z0ZAGWluCzMsABkJsijktThK1CW2jWhE9eKNyGZjy3OSHvVsl" 
    consumer_key = "1909159036651462656-omep3GAClI3TLjKO7H1GwyZqy9jHM1"
    consumer_secret = "49CXjRNiewRlpVkKGhRflWgs6vFuCtGklNXkswD6wCkhc"


    # Twitter authentication
    auth = tweepy.OAuthHandler(access_key, access_secret)   
    auth.set_access_token(consumer_key, consumer_secret) 

    # # # Creating an API object 
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name='@elonmusk', 
                            # 200 is the maximum allowed count
                            count=200,
                            include_rts = False,
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
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
    df.to_csv("s3://twitter-etl-project/twitter_etl_datas.csv")