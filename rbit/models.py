# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, backref

Base = declarative_base()

class Attachment(Base):
    __tablename__ = 'message_attachment'
    id = Column(Integer, primary_key=True)
    mid = Column(Integer, ForeignKey('message.mid'), index=True)
    filename = Column(String)

class Message(Base):
    __tablename__ = 'message'

    mid = Column(Integer, primary_key=True)
    from_ = Column(String)
    to = Column(String)
    cc = Column(String)
    bcc = Column(String)
    date = Column(DateTime)
    subject = Column(String)
    body = Column(String)

    attachments = relation(Attachment)

    @staticmethod
    def from_email_message(m):
        from email.utils import parsedate
        from time import mktime
        from datetime import datetime

        # I feel there should be an easier way, but I have not found it
        date = datetime.fromtimestamp(mktime(parsedate(m['Date'])))
        return Message(
                    from_=m['From'],
                    subject=m['Subject'],
                    body=m.get_payload(),
                    date=date,
                    to=m.get('To',''),
                    cc=m.get('CC', ''),
                    bcc=m.get('BCC', ''))

class Folder(Base):
    __tablename__ = 'folder'
    fid = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)

class FolderMessage(Base):
    __tablename__ = 'folder_message'
    fid = Column(Integer, ForeignKey('folder.fid'), primary_key=True, index=True)
    mid = Column(Integer, ForeignKey('message.mid'), primary_key=True, index=True)


