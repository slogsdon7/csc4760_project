import sqlite3
from containers import YoutubeVideo
from itertools import repeat

COUNTRY_TABLE_SQL = """
create table if not exists country
(
    id   INTEGER
        primary key,
    code text,
    name text
);

create unique index if not exists country_code_uindex
    on country (code);
    """

VIDEO_TABLE_SQL = """
create table if not exists video
(
    id                     INTEGER
        primary key,
    video_id               text,
    trending_date          date,
    title                  text,
    channel_title          text,
    category_id            int,
    publish_time           datetime,
    tags                   text,
    views                  int,
    likes                  int,
    dislikes               int,
    comment_count          int,
    thumbnail_link         text,
    comments_disabled      boolean,
    ratings_disabled       boolean,
    video_error_or_removed boolean,
    description            text,
    country                text,
    csv_row                int
);

create unique index if not exists video_country_id__csv_row_uindex
    on video (country, csv_row);
    
create index if not exists video_video_id_index
    on video (video_id);
    

"""

CATEGORY_TABLE_SQL = """
create table if not exists category
(
    id int
        constraint category_pk
            primary key,
    name text
);

"""


class DB:

    def __init__(self, path: str = 'db.sqlite') -> None:
        self.conn = sqlite3.connect(path)
        self.create_tables()

    def create_tables(self) -> None:
        self.conn.executescript(COUNTRY_TABLE_SQL)
        self.conn.executescript(VIDEO_TABLE_SQL)
        self.conn.executescript(CATEGORY_TABLE_SQL)

    def insert_video(self, video: YoutubeVideo) -> None:
        n = len(video._fields)
        SQL = f"INSERT OR IGNORE INTO video ({', '.join(video._fields)}) VALUES ({', '.join(repeat('?', n))})"
        with self.conn:
            self.conn.execute(SQL, video)

    def bulk_insert_video(self, videos) -> None:
        n = len(YoutubeVideo._fields)
        SQL = f"INSERT OR IGNORE INTO video ({', '.join(YoutubeVideo._fields)}) VALUES ({', '.join(repeat('?', n))})"
        with self.conn:
            self.conn.execute("BEGIN;")
            for video in videos:
                self.conn.execute(SQL, video)

    def fetch_videos(self):
        with self.conn:
            for row in self.conn.execute("SELECT * FROM video;"):
                yield YoutubeVideo(*row)
