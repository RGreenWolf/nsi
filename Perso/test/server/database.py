# database.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configurer la base de données
database = create_engine('sqlite:///storage/database.db')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    username = Column(String)
    password = Column(String)

Base.metadata.create_all(database)

def get_session():
    Session = sessionmaker(bind=database)
    return Session()
