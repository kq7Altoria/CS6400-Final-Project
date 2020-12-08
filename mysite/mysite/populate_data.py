import csv
from animes.models import *
from tqdm import tqdm


def format_date(date):
    date = date.split('/')
    # month
    date[0] = '0' + date[0] if int(date[0]) < 10 else date[0]
    # day
    date[1] = '0' + date[1] if int(date[1]) < 10 else date[1]
    # year
    date[2] = '20' + date[2] if int(date[1]) <= 21 else '19' + date[2]
    date[0], date[2] = date[2], date[0]
    date[1], date[2] = date[2], date[1]
    date = '-'.join(date)
    return date

anime_flag = False
user_flag = True
anime_data_path = 'animes/data/data_anime.csv'

if anime_flag:
    recorded_companies = set()
    recorded_tag = set()
    print('Start reading the anime data...')
    with open(anime_data_path) as f:
        reader = csv.reader(f)
        # consume the first row
        next(reader)
        for row in tqdm(reader):
            # print(row)
            if row[4] != '-':
                start_date = format_date(row[4])
            else:
                start_date = 'Not Available'
            if row[5] != '-':
                end_date = format_date(row[5])
            else:
                end_date = 'Not Available'
            # Create anime work object and insert it into the database
            anime, created = AnimeWork.objects.get_or_create(
            anime_name = row[0],
            anime_description = row[19],
            anime_rating = row[15],
            anime_airing_start_date = start_date,
            anime_airing_end_date = end_date
            )
            companies = row[10].split(',')
            tags = row[12].split(',')
            # Associate production companies to anime works
            for company in companies:
                comp, created = ProductionCompany.objects.get_or_create(
                company_name = company
                )
                comp.company_anime_works.add(anime)

            # Associate tags to anime works
            for tag in tags:
                t, created = Tag.objects.get_or_create(
                tag_name = tag
                )
                t.tag_anime_works.add(anime)
