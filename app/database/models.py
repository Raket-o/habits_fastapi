"""the module for creating tables"""
import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import backref, relationship
from sqlalchemy.types import DateTime, Integer, String

from app.database.connect import Base


class Book(Base):
    """Class Book. It is a table model books"""
    __tablename__ = "books"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(Base):
    """Class User. It is a table model users"""
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, nullable=False, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    token = Column(String(100), nullable=True)
    tasks = relationship('Task', backref='user', cascade='all, delete')


class Task(Base):
    """Class User. It is a table model tasks"""
    __tablename__ = "tasks"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(20), nullable=False)
    created_datetime = Column(DateTime, default=datetime.datetime.now())
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
