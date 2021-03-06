from datetime import datetime
from sqlalchemy import (Column,Integer,String,DateTime,ForeignKey)
from .db import Base,session
from sqlalchemy.sql import exists
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__='users'

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(50),unique=True,nullable=False)
    password = Column(String(50),nullable=False)
    last_login = Column(DateTime,default=datetime.now)
    created = Column(DateTime,default=datetime.now)

    def __repr__(self):
        return '<User #{}: {}>'.format(self.id,self.name)

    @classmethod
    def is_exists(cls,username):
        return session.query(exists().where(User.name == username)).scalar()

    @classmethod
    def add_user(cls,username,password):
        user=User(name=username,password=password)
        session.add(user)
        session.commit()

    @classmethod
    def get_pass(cls,username):
        user=session.query(cls).filter_by(name=username).scalar()
        if user:
            return user.password
        else:
            return ''

class Post(Base):
    __tablename__='posts'

    id= Column(Integer,primary_key=True,autoincrement=True)
    image_url=Column(String(100))
    thumb_url=Column(String(100))

    user_id=Column(Integer,ForeignKey('users.id'))
    user=relationship('User',backref='posts',uselist=False,cascade='all')

    def __repr__(self):
        return "<Post(#)>".format(self.id)


class Like(Base):
    __tablename__='likes'

    user_id=Column(Integer,ForeignKey('users.id'),nullable=False,primary_key=True)
    post_id=Column(Integer,ForeignKey('posts.id'),nullable=False,primary_key=True)

if __name__=='__main__':
    Base.metadata.create_all()