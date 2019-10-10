import csv
import glob
from os import path
from itertools import repeat
from datetime import datetime
from containers import YoutubeVideo
from db import DB

db = DB()
conn = db.conn


def extract_country_from_fname(filename: str):
    return path.basename(filename)[0:2]


def files():
    for path in glob.glob('youtube-new/*.csv'):
        yield path, extract_country_from_fname(path)


def insert_video(video: YoutubeVideo):
    n = len(video._fields)
    SQL = f"INSERT INTO video ({', '.join(video._fields)}) VALUES ({', '.join(repeat('?', n))})"
    with conn:
        conn.execute(SQL, video)


def process_rows(file: str, country: str):
    c_id = conn.execute("SELECT id FROM country WHERE code = ?", (country,)).fetchone()[0]
    with open(file, 'r', encoding='utf-8', errors='backslashreplace') as fp:
        reader = csv.reader(fp)
        next(reader)
        for i, row in enumerate(reader):
            video = YoutubeVideo(*row, c_id, i)
            video = video._replace(trending_date=datetime.strptime(video.trending_date, '%y.%d.%m').isoformat())
            insert_video(video)


if __name__ == '__main__':
    for file, country in files():
        print(f'loading {file}...')
        with conn:
            conn.execute("INSERT OR IGNORE INTO country (code) VALUES (?)", (country,))
        process_rows(file, country)

