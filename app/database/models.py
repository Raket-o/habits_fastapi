"""the module for creating tables"""
import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Time
from sqlalchemy.orm import backref, relationship
from sqlalchemy.types import DateTime, Integer, String

from app.database.connect import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False)
    password = Column(String(200), nullable=False)
    telegram_id = Column(Integer, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)

    habit = relationship(
        "Habit",
        cascade="all, delete",
        backref="users",
        passive_deletes=True,
        lazy=True,
    )

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Habit(Base):
    __tablename__ = "habits"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name_habit = Column(String(20), nullable=False)
    description = Column(String(200), nullable=True)

    tracking_habit = relationship('TrackingHabit', backref='habits', cascade='all, delete')


class TrackingHabit(Base):
    __tablename__ = "tracking_habits"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    habit_id = Column(Integer, ForeignKey('habits.id', ondelete='CASCADE'), nullable=False)
    alert_time = Column(Time, nullable=True)
    count = Column(Integer, nullable=False, default=0)


# class Book(Base):
#     """Class Book. It is a table model books"""
#     __tablename__ = "books"
#     __table_args__ = {'extend_existing': True}
#
#     id = Column(Integer, nullable=False, primary_key=True)
#     name = Column(String(20), nullable=False, unique=True)
#
#     def to_json(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}
#
#
# class User(Base):
#     """Class User. It is a table model users"""
#     __tablename__ = "users"
#     __table_args__ = {'extend_existing': True}
#
#     id = Column(Integer, nullable=False, primary_key=True)
#     username = Column(String(20), unique=True, nullable=False)
#     password = Column(String(100), nullable=False)
#     token = Column(String(100), nullable=True)
#     tasks = relationship('Task', backref='user', cascade='all, delete')
#
#
# class Task(Base):
#     """Class User. It is a table model tasks"""
#     __tablename__ = "tasks"
#     __table_args__ = {'extend_existing': True}
#
#     id = Column(Integer, nullable=False, primary_key=True)
#     name = Column(String(20), nullable=False)
#     created_datetime = Column(DateTime, default=datetime.datetime.now())
#     user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
