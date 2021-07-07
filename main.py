import argparse

from db_filler import vacancy_to_SQlite
from sync_parser import url_of_vacancies_to_list

parser = argparse.ArgumentParser()
parser.add_argument("vacancy", metavar='V', help="enter the vacancy for parsing on hh.ru")
parser.add_argument("--page",'-P', type=int, default=3,
                    help="enter the number of pages:int to parse on hh.ru (default: 3)")
parser.add_argument("--celery",'-C', action="store_true",
                    help="for using celery enter -C (default: False)")
args = parser.parse_args()


num_of_pages = args.page
vacancy = args.vacancy
celery = args.celery

if celery:
    print('celery test')
else:
    urls = url_of_vacancies_to_list(vacancy, num_of_pages)
    for url in urls:
        vacancy_to_SQlite(url,vacancy)




if __name__ == '__main__':
    pass
    # start('программист')
