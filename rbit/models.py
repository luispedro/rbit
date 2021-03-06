# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from sqlalchemy import Column, String, Unicode, Integer, ForeignKey, Text, DateTime, Float, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

import six
from rbit.decode import decode_unicode

Base = declarative_base()

class Attachment(Base):
    __tablename__ = 'message_attachment'
    id = Column(Integer, primary_key=True)
    mid = Column(Integer, ForeignKey('message.mid'), index=True)
    filename = Column(String)

    def __unicode__(self):
        return six.u('Attachment({0} of mid {1})').format(self.filename, self.mid)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return 'Attachment({0}, {1}, {2})'.format(self.id, self.mid, self.filename)

class MessageRelation(Base):
    __tablename__ = 'message_relationship'
    source = Column(Integer, ForeignKey('message.mid'), primary_key=True, index=True)
    target = Column(Integer, ForeignKey('message.mid'), primary_key=True, index=True)
    reltype = Column(String)

    def __unicode__(self):
        return six.u('MessageRelation({0} -{1}-> {2})').format(self.source, self.reltype, self.target)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return 'MessageRelation({0}, {1}, {2}, {3})'.format(self.id, self.source, self.target, self.reltype)

class Flag(Base):
    __tablename__ = 'message_flag'
    id = Column(Integer, primary_key=True)
    mid = Column(Integer, ForeignKey('message.mid'), index=True)
    flag = Column(String, index=True)

    def __unicode__(self):
        return six.u('Flag({0})').format(self.flag)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return 'Flag({0}, {1}, {2})'.format(self.id, self.mid, self.flag)


class Prediction(Base):
    __tablename__ = 'message_prediction'

    id = Column(Integer, primary_key=True)
    mid = Column(Integer, ForeignKey('message.mid'), index=True)
    type = Column(String)
    strength = Column(Float)
    value = Column(PickleType)


class Message(Base):
    __tablename__ = 'message'

    mid = Column(Integer, primary_key=True)
    uid = Column(Integer, index=True)
    account = Column(String)
    folder = Column(String, index=True)

    from_ = Column(Unicode)
    to = Column(Unicode)
    cc = Column(Unicode)
    bcc = Column(Unicode)
    date = Column(DateTime)
    subject = Column(Unicode)
    body = Column(Unicode)
    message_id = Column(String, index=True)
    headers = Column(PickleType)

    attachments = relationship(Attachment, backref='message')
    flags = relationship(Flag, backref='message')
    predictions = relationship(Prediction, backref='message')
    related = relationship('MessageRelation', uselist=True, primaryjoin = (mid == MessageRelation.source))


    @property
    def recipients(self):
        r = ''
        if self.to:
            r += self.to
        if self.cc:
            r += (' ' if r else '')
            r += self.cc
        if self.bcc:
            r += (' ' if r else '')
            r += self.bcc
        return r


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
        from email.header import decode_header
        from time import mktime
        from datetime import datetime

        def u(h):
            s = six.u('')
            for text,charset in decode_header(h):
                if charset is None:
                    s += decode_unicode(text, [])
                else:
                    s += decode_unicode(text, [charset])
            return s

        from collections import defaultdict
        headers = defaultdict(list)
        for k,v in m.items():
            headers[k].append(v)
        headers = dict(headers.items())
        try:
            # I feel there should be an easier way, but I have not found it
            date = datetime.fromtimestamp(mktime(parsedate(m['Date'])))
        except TypeError:
            # This is probably as good as anything else
            date = datetime.now()
        return Message(
                    from_=u(m['From']),
                    uid=uid,
                    subject=u(m['Subject']),
                    date=date,
                    message_id=m['Message-Id'],
                    headers=headers,
                    to=u(m.get('To','')),
                    cc=u(m.get('CC', '')),
                    bcc=u(m.get('BCC', '')))

    @staticmethod
    def load_by_mid(mid, create_session=None):
        from rbit.backend import call_create_session
        return call_create_session(create_session). \
                    query(Message). \
                    get(mid)

    def __unicode__(self):
        return six.u('Message({0}, {1} -> {2})'.format(self.uid, self.from_, self.to))

    def __str__(self):
        return str(unicode(self))


class Folder(Base):
    __tablename__ = 'folder'
    fid = Column(Integer, primary_key=True)
    name = Column(String(128), index=True)
    account = Column(String, index=True)
    uidvalidity = Column(Integer)
    highestmodseq = Column(Integer)


