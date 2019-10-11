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


def process_rows(file: str, country: str):
    with open(file, 'r', encoding='utf-8', errors='backslashreplace') as fp:
        reader = csv.reader(fp)
        next(reader)
        for i, row in enumerate(reader):
            video = YoutubeVideo(None, *row, country, i)
            video = video._replace(trending_date=datetime.strptime(video.trending_date, '%y.%d.%m').isoformat())
            print(f'Inserting row {video.csv_row} from {country}')
            db.insert_video(video)


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

