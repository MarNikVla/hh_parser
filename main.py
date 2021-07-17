"""
    Main module (entry point)
    usage: main.py [-h] [--page PAGE] [--celery] vacancy

    positional arguments:
      vacancy               enter the vacancy for parsing on hh.ru

    optional arguments:
      -h, --help            show this help message and exit
      --page PAGE, -P PAGE  enter the number of pages:int to parse on hh.ru (default: 3)
      --celery, -C          for using celery enter -C (default: False), you should pre-start celery
      worker: 'celery -A tasks worker -P solo --loglevel=info'
"""

import argparse

from db_filler import vacancy_to_SQlite
from sync_parser import url_of_vacancies_to_list
from decorators import execution_time_decorator
from tasks import db_fill_task

parser = argparse.ArgumentParser()
parser.add_argument("vacancy", help="enter the vacancy for parsing on hh.ru")
parser.add_argument("--page", '-P', type=int, default=3,
                    help="enter the number of pages:int to parse on hh.ru (default: 3)")
parser.add_argument("--celery", '-C', action="store_true",
                    help="for using celery enter -C (default: False), you should pre-start celery worker: "
                         "'celery -A tasks worker -P solo --loglevel=info'")
args = parser.parse_args()

@execution_time_decorator
def main(args):
    num_of_pages = args.page
    vacancy = args.vacancy
    celery = args.celery
    urls = url_of_vacancies_to_list(vacancy, num_of_pages)

    if celery:
        for url in urls:
            db_fill_task.delay(url, vacancy)
    else:
        for url in urls:
            vacancy_to_SQlite(url, vacancy)


if __name__ == '__main__':
    main(args)

