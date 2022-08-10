import datetime
from pathlib import Path
import sqlite3

from django.core.management.base import BaseCommand, CommandError
import pandas as pd


class Command(BaseCommand):
    help = 'Load YaMDB database'

    DB_PATH = 'db.sqlite3'
    DB_URI = f'file:{DB_PATH}?mode=rw'

    TABLES_PATH = Path('./static/data/')

    DB_TABLES = {
        'titles.csv': 'titles_title',
        'category.csv': 'titles_category',
        'genre.csv': 'titles_genre',
        'genre_title.csv': 'titles_title_genre',
        'comments.csv': 'reviews_comment',
        'review.csv': 'reviews_review',
        'users.csv': 'users_user'
    }

    CONVERTERS = {
        'pub_date': lambda x: pd.to_datetime(x).tz_localize(None),
        'bio': str,
        'first_name': str,
        'last_name': str,
    }

    COLUMNS = {
        'author': 'author_id',
        'review': 'review_id',
        'title': 'title_id',
        'genre': 'genre_id',
        'category': 'category_id',
    }

    def handle(self, *args, **options):
        try:
            sqlite_connection = sqlite3.connect(self.DB_URI, uri=True)
            self.stdout.write(
                self.style.SUCCESS('Успешное подключение к SQLite')
            )

            for table in self.TABLES_PATH.glob('*.csv'):
                if table.name in self.DB_TABLES:
                    df = pd.read_csv(table, converters=self.CONVERTERS)
                    df.rename(columns=self.COLUMNS, inplace=True)

                    if table.name == 'users.csv':
                        df = df.assign(
                            password='12345',
                            last_login=pd.NaT,
                            is_superuser=False,
                            is_staff=False,
                            is_active=True,
                            date_joined=datetime.datetime.now(),
                        )
                    elif table.name == 'titles.csv':
                        df = df.assign(description=None)

                    df.to_sql(
                        name=self.DB_TABLES[table.name],
                        con=sqlite_connection,
                        if_exists='replace',
                        index=False,
                        index_label='id'
                    )

        except sqlite3.Error as error:
            sqlite_connection = None
            raise CommandError(
                f'Ошибка при подключении к sqlite: {error}'
            ) from error
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                self.stdout.write(
                    self.style.SUCCESS('Соединение с SQLite закрыто')
                )
