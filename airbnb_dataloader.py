import csv
import urllib.request
import urllib.error
import argparse
import os
import pandas as pd

from pathlib import Path

def list_columns(csv_path='data/airbnb.csv'):
    with open(csv_path, 'r') as file:
        header = file.readline()
        cols = header.split(';')

        for i, col in enumerate(cols):
            print(f'{i}:\t {col}')

def minimize_data(rows_per_rating=500, csv_path='data/airbnb.csv', out_path='data/airbnb_min.csv'):
    '''Minimize original CSV file to minimized file
    by taking n rows from each possible rating (0-11)'''

    # Prepare dataframes
    result_df = pd.DataFrame(columns=['media', 'rating'])
    resour_df = pd.read_csv(csv_path, sep=';')
    coi = ['Picture', 'Review scores cleanliness'] # Columns of interest

    # Minimize resource dataframe
    resour_df = resour_df[coi]
    resour_df = resour_df.rename(columns={'Picture': 'media', 'Review scores cleanliness': 'rating'})

    # Store n rows for each rating in new dataframe
    for rating in range(11):
        rating_df = resour_df.loc[resour_df['rating'] == float(rating)]
        rating_df = rating_df.head(rows_per_rating)
        result_df = result_df.append(rating_df)
    result_df.to_csv(out_path)

def download_media(csv_path='data/airbnb_min.csv', data_dir='data/airbnb'):
    # Create all directories
    for i in range(2, 11):
        Path('{}/{}'.format(data_dir, i)).mkdir(parents=True, exist_ok=True)
    
    df = pd.read_csv(csv_path)

    for index, row in df.iterrows():
        image, rating = row['media'], row['rating']

        if image != '' and rating != '':
            try:
                rating = int(rating)
                urllib.request.urlretrieve(image, '{}/{}/{}.jpg'
                    .format(data_dir, rating, index))
            except (urllib.error.HTTPError, urllib.error.ContentTooShortError):
                print(f'Failed to download image {image}')
        
        if index % 10 == 0:
            print(f'Downloaded {index} images.')

def arg_dir_type(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f'readable_dir:{path} is not a valid directory path')

def arg_mode_type(mode):
    if mode == 'download-all':
        return 0
    elif mode == 'minimize-csv':
        return 1
    elif mode == 'download-media':
        return 2
    elif mode == 'list-columns':
        return 3
    else:
        raise argparse.ArgumentTypeError(f'Invalid mode selected {mode}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download airbnb pictures.')
    parser.add_argument('mode', type=arg_mode_type, help='Operation mode (download-all, download-csv or download-media).')
    parser.add_argument('csvpath', type=argparse.FileType('r', encoding='UTF-8'), help='Destination/Origin of CSV file')
    parser.add_argument('datadir', type=arg_dir_type)
    parser.add_argument('-R', type=int, default=500)
    args = parser.parse_args()

    if args.mode is 1 or args.mode is 0:
        minimize_data(rows_per_rating=args.R)

    if args.mode is 2 or args.mode is 0:
        download_media()
    
    if args.mode is 3:
        list_columns()