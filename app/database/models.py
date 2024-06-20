"""the module for creating tables"""
from sqlalchemy import Boolean, Column, ForeignKey, Time
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer, String

from app.database.connect import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False)
    hashed_password = Column(String(200), nullable=False)
    # telegram_id = Column(Integer, nullable=False, unique=True)
    telegram_id = Column(Integer, nullable=False)
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
    alert_time = Column(Time, nullable=True)
    count = Column(Integer, nullable=False, default=0)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
