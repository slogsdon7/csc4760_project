from typing import NamedTuple, Union


class YoutubeVideo(NamedTuple):
    id: Union[int, None]  # Generated DB ID
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
    comments_disabled: Union[bool, str]
    ratings_disabled: Union[bool, str]
    video_error_or_removed: Union[bool, str, int]
    description: str
    country: str
    csv_row: int  # Generated attribute based on the row number in the original CSV file
