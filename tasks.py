from celery import Celery
from db_filler import make_vacation_data, fill_db


app = Celery('tasks', broker='redis://localhost')

@app.task(expires=120)
def db_fill(url):
    data = make_vacation_data(url)
    fill_db(data, 'test')
    return 'Done'
