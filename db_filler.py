from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_settings import Vacancy, Base
from parse_single_vacation import parse_single_vacation

def fill_db(vacation_data, vacancy = None):
    if vacation_data:

        engine = create_engine(f'sqlite:///vacancy-{vacancy}.db')
        Base.metadata.create_all(engine)

        DBSession = sessionmaker(bind=engine)

        session = DBSession()

        session.add(vacation_data)
        session.commit()

def make_vacation_data(url):
    try:
        vacancyOne = Vacancy(**parse_single_vacation(url))
    except AttributeError as e:
        print(e)
        return []

    # vacancyOne = Vacancy(**res)

    return vacancyOne

if __name__ == '__main__':
    # url = 'https://hh.ru/vacancy/45571638'
    url = 'https://hh.ru/vacancy/45571633ываыва'
    data = make_vacation_data(url)
    fill_db(data, 'программист')