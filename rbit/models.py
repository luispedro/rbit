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
    uid = Column(Integer, index=True)
    folder = Column(String, index=True)

    from_ = Column(String)
    to = Column(String)
    cc = Column(String)
    bcc = Column(String)
    date = Column(DateTime)
    subject = Column(String)
    body = Column(String)

    attachments = relation(Attachment)

    @staticmethod
    def from_email_message(m, uid):
        '''
        message = from_email_message(m, uid)

        Parameters
        ----------
        m : email.Message
            The message
        uid : int
            The IMAP UID

        Returns
        -------
        message : rbit.models.Message
        '''

        from email.utils import parsedate
        from time import mktime
        from datetime import datetime

        # I feel there should be an easier way, but I have not found it
        date = datetime.fromtimestamp(mktime(parsedate(m['Date'])))
        return Message(
                    from_=m['From'],
                    uid=uid,
                    subject=m['Subject'],
                    date=date,
                    to=m.get('To',''),
                    cc=m.get('CC', ''),
                    bcc=m.get('BCC', ''))

    def __unicode__(self):
        return u'Message(%s, %s -> %s)' % (self.uid, self.from_, self.to)

    def __str__(self):
        return str(unicode(self))

class Folder(Base):
    __tablename__ = 'folder'
    fid = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    uidvalidity = Column(Integer)


