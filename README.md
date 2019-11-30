# csc4760_project

[Youtube Dataset](https://www.kaggle.com/datasnaek/youtube-new)

## Setup
1. Download the dataset from above and extract the files to a directory named `data/`
2. Run `process.py` using Python to initialize and populate the sqlite database. This will take a few minutes.


## Usage

In `containers.py`, there is a helpful `YoutubeVideo` [namedtuple](https://docs.python.org/3/library/collections.html#collections.namedtuple) class which maps directly to a row from the video table.


````python
from containers import YoutubeVideo
from db import DB

db = DB()

row = db.conn.execute('SELECT * FROM video LIMIT 1').fetchone()
video = YoutubeVideo(*row)

print(video.views)
# 310130
print(video.publish_time)
# '2017-11-13T06:06:22.000Z'
````

 

