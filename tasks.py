from celery import Celery
from db_filler import vacancy_to_SQlite

app = Celery('tasks', broker='redis://localhost')


@app.task(expires=120)
def db_fill_task(url, vacancy='test_db'):
    vacancy_to_SQlite(url, vacancy)
    return 'db_fill_task - Done'
