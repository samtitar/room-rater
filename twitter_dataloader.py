import datetime
import tweepy
import csv
import urllib.request

from pathlib import Path
from twitter_config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

def get_tweets(screen_name, save_csv=True):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    tweets = []
    tweet_count = 0

    statuses = tweepy.Cursor(api.user_timeline, id=screen_name).items()
    for status in statuses:
        if 'media' in status.entities.keys():
            if tweet_count % 50 == 0:
                print('{} tweets downloaded'.format(tweet_count))
            tweet_count += 1

            try:
                rating = int(status.text.split('/10')[0][-2:])
                tweet_data = [status.id_str, rating,
                            status.entities['media'][0]['media_url']]
                tweets.append(tweet_data)
            except:
                continue
    
    save_in_dir(tweets)

    if save_csv:
        with open(f'data/tweets.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'rating', 'media'])
            writer.writerows(tweets)
    return tweets

def save_in_dir(tweets):
    # Create class dirs
    for i in range(11):
        Path('data/dataset/{}'.format(i)).mkdir(parents=True, exist_ok=True)

    for i, tweet in enumerate(tweets):
        if i % 100 == 0:
            print('{}/{} images downloaded'.format(i, len(tweets)))
        
        rating = max(min(tweet[1], 10), 0)
        urllib.request.urlretrieve(tweet[2],
            'data/dataset/{}/{}.jpg'.format(rating, i))

if __name__ == '__main__':
    get_tweets('ratemyskyperoom')