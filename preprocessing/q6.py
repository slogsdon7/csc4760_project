import db
import pandas as pd
db = db.DB()



SQL = '''
WITH shared_videos(c1, c2, shared_videos)
         AS (SELECT v1.country c1, v2.country c2, count(DISTINCT v1.video_id)
             FROM video v1
                      JOIN video v2
                           ON (v2.video_id = v1.video_id) --AND (v2.trending_date = v1.trending_date)
             WHERE c1 != c2
             GROUP BY c1, c2),
     total_videos(country, videos)
         AS (SELECT country, count(DISTINCT video_id)
         FROM video
         GROUP BY country
    )
SELECT c1,
       c2,
       (CAST(shared_videos as float) / (tv1.videos + tv2.videos)) percent_shared,
       shared_videos,
       (tv1.videos + tv2.videos)                                  total_videos
FROM shared_videos
         JOIN total_videos tv1 ON tv1.country = shared_videos.c1
         JOIN total_videos tv2 ON tv2.country = shared_videos.c2;'''

def process():
    rows = db.conn.execute(SQL).fetchall()
    labels = ['c1', 'c2', 'shared_percent', 'shared_count', 'total_count']
    df = pd.DataFrame.from_records(rows, columns=labels, index='c1')
    df.to_csv('processed_data/q6.csv')


if __name__ == '__main__':
    process()
