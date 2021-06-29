from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_settings import Vacancy, Base
from parse_single_vacation import parse_single_vacation

def fill_db(vacation_data, vacancy = None):

    engine = create_engine(f'sqlite:///vacancy-{vacancy}.db')
    Base.metadata.create_all(engine)

    DBSession = sessionmaker(bind=engine)

    session = DBSession()

    url = 'https://hh.ru/vacancy/45571638'

    res = parse_single_vacation(url)
    # print(res)
    # vacancyOne = Vacancy(**res)
    # print(vacancyOne)
    session.add(vacation_data)
    session.commit()

def make_vacation_data(url):
    res = parse_single_vacation(url)
    vacancyOne = Vacancy(**res)

    return vacancyOne

if __name__ == '__main__':
    # url = 'https://hh.ru/vacancy/45571638'
    url = 'https://hh.ru/vacancy/45571638'
    data = make_vacation_data(url)
    fill_db(data, 'программист')