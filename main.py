import argparse

from db_filler import vacancy_to_SQlite
from sync_parser import url_of_vacancies_to_list
from decorators import execution_time_decorator
from tasks import db_fill_task

parser = argparse.ArgumentParser()
parser.add_argument("vacancy", metavar='V', help="enter the vacancy for parsing on hh.ru")
parser.add_argument("--page", '-P', type=int, default=3,
                    help="enter the number of pages:int to parse on hh.ru (default: 3)")
parser.add_argument("--celery", '-C', action="store_true",
                    help="for using celery enter -C (default: False)")
args = parser.parse_args()

# num_of_pages = args.page
# vacancy = args.vacancy
# celery = args.celery


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
    # start('программист')
