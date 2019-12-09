import csv
import glob
import os.path
import json
from datetime import datetime
from containers import YoutubeVideo
import db


def extract_country_from_fname(filename: str):
    return os.path.basename(filename)[0:2]


def glob_files(path, extension):
    for path in glob.glob(f'{path}/*{extension}'):
        yield path, extract_country_from_fname(path)


def str_to_bool(s):
    return s.lower() == 'true'

def fix_row_id(video: YoutubeVideo):
    return video._replace(video_id = video.thumbnail_link[23:-12])

def process_rows(file: str, country: str, db):
    skipped = []
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
            if video.video_id == '#NAME?' or video.video_id == '#VALUE!':
                fix_row_id(video)

            videos.append(video)
        db.bulk_insert_video(videos)
    return skipped



def load_categories(files, db):
    for file, country in files:
        with open(file, 'r') as fp:
            data = json.load(fp)
            print(f'loading {file}...')
            for item in data['items']:
                with db.conn:
                    db.conn.execute("INSERT OR IGNORE INTO category (id, name, assignable) VALUES (?,?,?)",
                                    (item['id'], item['snippet']['title'], item['snippet']['assignable']))


def load_data(files, db):
    skipped = []
    for file, country in files:
        print(f'loading {file}...')
        with db.conn:
            db.conn.execute("INSERT OR IGNORE INTO country (code) VALUES (?)", (country,))
        skipped.append(process_rows(file, country, db))
    return [item for l in skipped for item in l]

def get_files(path: str) -> tuple:
    if not os.path.exists(path):
        raise Exception(f'Error: Directory at "{os.path.abspath(path)}" does not exist.')
    csv_files = list(glob_files(path, 'csv'))
    json_files = list(glob_files(path, 'json'))

    count = len(csv_files)
    if count < 10:
        raise Exception(f'Error: Data directory has {count} csv files. Expected 10')
    count = len(json_files)
    if count < 10:
        raise Exception(f'Error: Data directory has {count} csv files. Expected 10')

    return csv_files, json_files

def run(path: str, db_path: str):
    db_ = db.DB(db_path)
    csv_files, json_files = get_files(path)
    load_categories(json_files)
    return load_data(csv_files)

if __name__ == '__main__':
    skipped = run('data')


