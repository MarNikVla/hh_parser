
from sqlalchemy import Column, Integer, String, Text

from sqlalchemy.ext.declarative import declarative_base

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

