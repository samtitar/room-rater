import datetime
import tweepy
import csv
import urllib.request
import argparse
import os

from pathlib import Path

# Be sure to store twitter API keys in twitter_config.py
from twitter_config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

def get_tweets(screen_name, filename='data/tweets.csv'):
    '''Downloads all tweets to CSV file'''

    # Setup authentication
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    tweets = []
    tweet_count = 0

    # Create cursor and loop over all results
    statuses = tweepy.Cursor(api.user_timeline, id=screen_name).items()
    for status in statuses:
        # Only get tweets with media
        if 'media' in status.entities.keys():
            if tweet_count % 50 == 0:
                print('{} tweets downloaded'.format(tweet_count))
            tweet_count += 1

            try:
                # Get rating from tweet
                rating = int(status.text.split('/10')[0][-2:])
                tweet_data = [status.id_str, rating,
                            status.entities['media'][0]['media_url']]
                tweets.append(tweet_data)
            except:
                continue

    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'rating', 'media'])
        writer.writerows(tweets)

def download_media(csv_path='data/tweets.csv', data_dir='data/twitter'):
    '''Download media from CSV file'''
    
    # Create all directories
    for i in range(11):
        Path('{}/{}'.format(data_dir, i)).mkdir(parents=True, exist_ok=True)

    with open(csv_path, 'r') as csv_file:
        tweet_reader = csv.reader(csv_file)
        next(tweet_reader)

        # Loop trough CSV
        for i, (_, rating, media) in enumerate(tweet_reader):
            if i % 50 == 0:
                print('Downloaded {} tweet media'.format(i))
            rating = max(min(int(rating), 10), 0) # Clamp rating between 0 - 10
            urllib.request.urlretrieve(media, '{}/{}/{}.jpg'
                .format(data_dir, rating, i))

def arg_dir_type(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f'readable_dir:{path} is not a valid directory path')

def arg_mode_type(mode):
    if mode == 'download-all':
        return 0
    elif mode == 'download-csv':
        return 1
    elif mode == 'download-media':
        return 2
    else:
        raise argparse.ArgumentTypeError(f'Invalid mode selected {mode}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download roomrater tweets.')
    parser.add_argument('screenname', type=str, help='Twitter account name.')
    parser.add_argument('mode', type=arg_mode_type, help='Operation mode (download-all, download-csv or download-media).')
    parser.add_argument('csvpath', type=argparse.FileType('r', encoding='UTF-8'), help='Destination/Origin of CSV file')
    parser.add_argument('datadir', type=arg_dir_type)
    args = parser.parse_args()

    if args.mode is 0 or args.mode is 1:
        print('Downloading tweets into CSV')
        get_tweets(args.screenname, filename=args.csvpath)

    if args.mode is 0 or args.mode is 2:
        print('Downloading tweet media into dataset')
        download_media(csv_path=args.csvpath.name, data_dir=args.datadir)