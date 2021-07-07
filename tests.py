
from db_filler import vacancy_to_SQlite
from tasks import db_fill_task
from sync_parser import url_of_vacancies_to_list
import subprocess
import os
# os.system('dir c:\\')

# urls= url_of_vacancies_to_list('токарь',2)

# def populate_db_celery(vacancy, num_of_pages = 2):
#     urls = url_of_vacancies_to_list(vacancy, num_of_pages)
#     for url in urls:
#         db_fill_task.delay(url,vacancy)
#
# def populate_db(vacancy, num_of_pages = 2):
#     urls = url_of_vacancies_to_list(vacancy, num_of_pages)
#     for url in urls:
#         vacancy_to_SQlite(url,vacancy)




if __name__ == '__main__':
    subprocess.run('celery -A tasks worker -P solo --loglevel=info')
    # os.system('celery -A tasks worker -P solo --loglevel=info')
    # populate_db('токарь',1)
    # import time
    # start_time = time.time()
    # populate_db_celery('токарь',1)
    # print("--- %s seconds ---" % (time.time() - start_time))