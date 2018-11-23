from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

HOST = '192.168.2.250'
PORT = '3306'
DATABASE = 'tudo28'
USERNAME = 'admin'
PASSWORD = 'Root110qwe'

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME,PASSWORD,HOST,PORT,DATABASE

)

engine = create_engine(DB_URI)
DBSession = sessionmaker(bind=engine)
Base = declarative_base(engine)
