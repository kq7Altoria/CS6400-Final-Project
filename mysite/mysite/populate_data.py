import csv
from animes.models import *


def format_date(date):
    # month
    date = date.split('/')
    print(date)
    date[0] = '0' + date[0] if int(date[0]) < 10 else date[0]
    # day
    date[1] = '0' + date[1] if int(date[1]) < 10 else date[1]
    # year
    date[2] = '20' + date[2] if int(date[1]) <= 21 else '19' + date[2]
    date[0], date[2] = date[2], date[0]
    date[1], date[2] = date[2], date[1]
    date = '-'.join(date)
    return date
anime_flag = True
user_flag = False
anime_data_path = 'animes/data/anime_data_cleaned_v1.csv'

if anime_flag:
    with open(anime_data_path) as f:
        reader = csv.reader(f)
        # consume the first row
        next(reader)
        cnt = 0
        for row in reader:
            # print(row)
            start_date = format_date(row[5])
            end_date = format_date(row[6])
            print(cnt)
            _, created = AnimeWork.objects.get_or_create(
            anime_name = row[1],
            anime_description = row[20],
            anime_rating = row[16],
            anime_avatar_url = 'www.baidu.com',
            anime_cover_image_url = 'www.baidu.com',
            # anime_airing_start_date = start_date,
            # anime_airing_end_date = end_date
            )
            cnt += 1
