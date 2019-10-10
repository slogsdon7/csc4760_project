import csv
import glob
from os import path
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
    c_id = db.conn.execute("SELECT id FROM country WHERE code = ?", (country,)).fetchone()[0]
    with open(file, 'r', encoding='utf-8', errors='backslashreplace') as fp:
        reader = csv.reader(fp)
        next(reader)
        for i, row in enumerate(reader):
            video = YoutubeVideo(*row, c_id, i)
            video = video._replace(trending_date=datetime.strptime(video.trending_date, '%y.%d.%m').isoformat())
            db.insert_video(video)


if __name__ == '__main__':
    for file, country in files():
        print(f'loading {file}...')
        with db.conn:
            db.conn.execute("INSERT OR IGNORE INTO country (code) VALUES (?)", (country,))
        process_rows(file, country)

