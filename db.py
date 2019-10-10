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
    video_id               text,
    id                     INTEGER
        primary key,
    trending_date          date,
    title                  text,
    channel_title          text,
    category_id            int,
    publish_time           datetime,
    tags                   text,
    views                  int,
    likes                  int,
    dislikes               int,
    comments               int,
    thumbnail_link         text,
    comments_disabled      boolean,
    ratings_disabled       boolean,
    video_error_or_removed boolean,
    description            text,
    country_id             int
        references country,
    comment_count          int,
    csv_row                int
);

create unique index if not exists video_country_id__csv_row_uindex
    on video (country_id, csv_row);
"""


class DB:
    def __init__(self, path: str = 'db.sqlite') -> None:
        self.conn = sqlite3.connect(path)
        self.create_tables()

    def create_tables(self) -> None:
        self.conn.executescript(COUNTRY_TABLE_SQL)
        self.conn.executescript(VIDEO_TABLE_SQL)

    def insert_video(self, video: YoutubeVideo):
        n = len(video._fields)
        SQL = f"INSERT INTO video ({', '.join(video._fields)}) VALUES ({', '.join(repeat('?', n))})"
        with self.conn:
            self.conn.execute(SQL, video)

