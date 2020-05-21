import tweepy
import csv

# Twitter API credentials
CONSUMER_KEY = ""
CONSUMER_SECRET = ""

ACCESS_KEY = ""
ACCESS_SECRET = ""


def get_tweets(screen_name, exclude_replies=True):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    tweets = []
    new_tweets = api.user_timeline(screen_name=screen_name, count=200,
                                    exclude_replies=exclude_replies)
    tweets.extend(new_tweets)
    
    # Get oldest tweet ID
    oldest_id = tweets[-1].id - 1
    
    # Get tweets from timeline
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(handle=screen_name, count=200,
                                        exclude_replies=exclude_replies,
                                        max_id=oldest_id)
        tweets.extend(new_tweets)
        oldest_id = tweets[-1].id - 1
    outtweets = [(tweet.id_str, tweet.created_at, tweet.text) for tweet in tweets]
    
    # CSV  
    with open(f'new_{screen_name}_tweets.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)