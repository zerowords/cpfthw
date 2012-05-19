from sqlalchemy import *
from sqlalchemy.orm import mapper
from tgnotes.model import DeclarativeBase, metadata

from datetime import datetime

class Note(DeclarativeBase):
    __tablename__ = "notes"
    note_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    subject = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    date_taken = Column(Date, nullable=True)
