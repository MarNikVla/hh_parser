from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_settings import Vacancy, Base
from parse_single_vacancy import parse_single_vacancy


def fill_SQlite_db(vacancy_data: Vacancy, vacancy='test_db'):
    if vacancy_data:
        engine = create_engine(f'sqlite:///vacancy_{vacancy}.db')
        Base.metadata.create_all(engine)

        DBSession = sessionmaker(bind=engine)

        session = DBSession()

        session.add(vacancy_data)
        session.commit()


def make_vacancy_data(url: str) -> Vacancy or list:
    try:
        vacancy = Vacancy(**parse_single_vacancy(url))
    except AttributeError as e:
        # print(e)
        return []
    return vacancy

def vacancy_to_SQlite(url, vacancy):
    data = make_vacancy_data(url)
    fill_SQlite_db(data, vacancy)


if __name__ == '__main__':
    pass
