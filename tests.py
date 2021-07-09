import sys

from tasks import app
import subprocess
import os




if __name__ == '__main__':
    # argv = ['worker', '--loglevel=info', '--pool=solo']
    # app.worker_main(argv)
    # args = ['celery -A tasks worker -P solo --loglevel=info']

    process = subprocess.Popen('celery -A tasks worker -P solo --loglevel=info', stdout=sys.stdout)
    process.wait(20)
    print('fdfdf')

    # subprocess.run('celery -A tasks worker -P solo --loglevel=info')
    # os.system('celery -A tasks worker -P solo --loglevel=info')
    # populate_db('токарь',1)
    # import time
    # start_time = time.time()
    # populate_db_celery('токарь',1)
    # print("--- %s seconds ---" % (time.time() - start_time))