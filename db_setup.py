import sys
from sqlalchemy import Column, Integer, String, Text

# для определения таблицы и модели
from sqlalchemy.ext.declarative import declarative_base

# для настроек
from sqlalchemy import create_engine

# создание экземпляра declarative_base
Base = declarative_base()

# здесь добавим классы
class Vacancy(Base):
    __tablename__ = 'vacancy'

    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    key_skills = Column(Text(), nullable=True)
    salary = Column(String(150), default=0, nullable=True)
    description = Column(Text(), nullable=True)
    link = Column(String(250), nullable=False)


# создает экземпляр create_engine в конце файла
engine = create_engine('sqlite:///vacancy-collection.db')

Base.metadata.create_all(engine)