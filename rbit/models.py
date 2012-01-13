# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Message(Base):
    __tablename__ = 'message'

    mid = Column(Integer, primary_key=True)
    body = Column(String)
    subject = Column(String)
    recipients = Column(String)

class Folder(Base):
    __tablename__ = 'folder'
    fid = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)

class FolderMessage(Base):
    __tablename__ = 'folder_message'
    fid = Column(Integer, ForeignKey('folder.fid'), primary_key=True, index=True)
    mid = Column(Integer, ForeignKey('message.mid'), primary_key=True, index=True)


