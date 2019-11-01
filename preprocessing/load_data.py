import csv
import glob
from os import path
import json
from datetime import datetime
from containers import YoutubeVideo
from db import DB

db = DB()


def extract_country_from_fname(filename: str):
    return path.basename(filename)[0:2]


def files():
    for path in glob.glob('data/*.csv'):
        yield path, extract_country_from_fname(path)


def str_to_bool(s):
    return s.lower() == 'true'


def process_rows(file: str, country: str):
    with open(file, 'r', encoding='utf-8', errors='backslashreplace') as fp:
        reader = csv.reader(fp)
        next(reader)
        videos = []
        for i, row in enumerate(reader):
            video = YoutubeVideo(None, *row, country, i)
            video = video._replace(
                trending_date=datetime.strptime(video.trending_date, '%y.%d.%m').isoformat(),
                ratings_disabled=str_to_bool(video.ratings_disabled),
                comments_disabled=str_to_bool(video.comments_disabled),
                video_error_or_removed=str_to_bool(video.video_error_or_removed)
            )
            videos.append(video)
        db.bulk_insert_video(videos)


def load_categories():
    for file, country in files():
        with open(f'data/{country}_category_id.json', 'r') as fp:
            data = json.load(fp)
            for item in data['items']:
                db.conn.execute("INSERT OR IGNORE INTO category (id, name) VALUES (?,?)", (item['id'], item['snippet']['title']))


def load_data():
    for file, country in files():
        print(f'loading {file}...')
        with db.conn:
            db.conn.execute("INSERT OR IGNORE INTO country (code) VALUES (?)", (country,))
        process_rows(file, country)


if __name__ == '__main__':
    load_categories()
    load_data()

