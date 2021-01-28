from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Vacancy
from parse_single_vacation import parse_single_vacation

engine = create_engine('sqlite:///vacancy-collection.db', echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


vacancyOne = Vacancy(title="Чистый Pyth", key_skills="Дэн Бейде", salary=str(565),
                  description="Дэн Бейде", link = "Дэн Бейде")


url = 'https://hh.ru/vacancy/41892877'

res = parse_single_vacation(url)
print(res)
# vacancyOne = Vacancy(**res)
session.add(vacancyOne)
session.commit()
if __name__ == '__main__':
    pass
