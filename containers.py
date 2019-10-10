from typing import NamedTuple


class YoutubeVideo(NamedTuple):
    video_id: str
    trending_date: str
    title: str
    channel_title: str
    category_id: int
    publish_time: str
    tags: str
    views: int
    likes: int
    dislikes: int
    comment_count: int
    thumbnail_link: str
    comments_disabled: bool
    ratings_disabled: bool
    video_error_or_removed: bool
    description: str
    country_id: str
    csv_row: int  # Generated attribute based on the row number in the original CSV file
