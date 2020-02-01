# csc4760_project: Youtube Trending Videos Analysis 
[Click here to view output of analysis notebook](https://github.com/slogsdon7/csc4760_project/blob/master/analysis.ipynb)


## Dependencies 
[Youtube Dataset](https://www.kaggle.com/datasnaek/youtube-new)

You will need pandas, seaborn, matplotlib, scikit-learn, jupyter, and at least Python 3.6.

## Setup
1. Download the dataset from above and extract the files to the directory named 'data' in the project directory. The directory should look roughly like this when you're done. 
```
├── Archive.zip
├── README.md
├── analysis.ipynb
├── containers.py
├── data
│   ├── CA_category_id.json
│   ├── CAvideos.csv
│   ├── DE_category_id.json
│   ├── DEvideos.csv
│   ├── FR_category_id.json
│   ├── FRvideos.csv
│   ├── GB_category_id.json
│   ├── GBvideos.csv
│   ├── IN_category_id.json
│   ├── INvideos.csv
│   ├── JP_category_id.json
│   ├── JPvideos.csv
│   ├── KR_category_id.json
│   ├── KRvideos.csv
│   ├── MX_category_id.json
│   ├── MXvideos.csv
│   ├── RU_category_id.json
│   ├── RUvideos.csv
│   ├── US_category_id.json
│   └── USvideos.csv
├── db.py
├── db_loader.py


```
1. Run `pip install -r requirements.txt` in the project directory. You may already have these and wish to skip this step, but it is there just in case.
2. Run `jupyter notebook` in the project directory to get started
3. The first cell of analysis.ipynb will run the preprocessing routines if needed, or you can run `python db_loader.py` in the root project directory. 


## Dev Info

To get a dataframe with all the videos:

````python
from db import DB

db = DB()
df = db.fetch_videos_as_df()

````

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

 

