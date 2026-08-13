from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="list")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

    list_id = Column(Integer, ForeignKey("lists.id"))

    list = relationship("List", back_populates="tasks")
    list = relationship("Reminder", back_populates="tasks")


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    remind_at = Column(DateTime, nullable=False)
    sent = Column(Boolean, default=False)

    task_id = Column(Integer, ForeignKey("tasks.id"))

    task = relationship("Task", back_populates="reminders")