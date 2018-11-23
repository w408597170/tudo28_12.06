from datetime import datetime

from sqlalchemy import (Column, Integer, String, DateTime)
from sqlalchemy.sql import exists

from .db import Base, DBSession
session = DBSession()

class User(Base):
    """
    用户表,记录用户相关信息
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    created = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return '<User(#{}: {})>'.format(self.id, self.name)

    @classmethod
    def is_exists(cls,username):
        return  session.query(exists().where(User.name == username)).scalar()


    @classmethod
    def add_user(cls, username, password):
        """
        增加一个用户记录
        :param username:
        :param password:
        :return:
        """
        user = User(name=username, password=password)

        session.add(user)
        session.commit()




# if __name__ == '__main__':
#     Base.metadata.create_all()