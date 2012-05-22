#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, Integer, Text, String, Date

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session, sessionmaker

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = \
    scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Note(Base):

    __tablename__ = 'note'
    note_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False, unique=True)
    author = Column(String(100), nullable=False, unique=True)
    subject = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    date_created = Column(Date, default=datetime.now().date())

    def __init__(
        self,
        title,
        author,
        subject,
        description,
        ):
        self.title = title
        self.author = author
        self.subject = subject
        self.description = description


