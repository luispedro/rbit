# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from sqlalchemy import Column, String, Integer, ForeignKey, Text, Float, PickleType, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from rbit.models import Base

class ContactInfo(Base):
    __tablename__ = 'contact_info'

    id = Column(Integer, primary_key=True)
    cid = Column(Integer, ForeignKey('contact.cid'), index=True)
    type = Column(String)
    value = Column(PickleType)
    
class Contact(Base):
    __tablename__ = 'contact'

    cid = Column(Integer, primary_key=True)
    info = relationship(ContactInfo, backref='contact')

    def __getitem__(self, key):
        return [info.value for info in self.info if info.type == key]

    def add_info(self, key, value):
        rel = ContactInfo(cid=self, type=key, value=value)
        self.info.append(rel)
        return rel

class Mentioned(Base):
    __tablename__ = 'mentioned'
    id = Column(Integer, primary_key=True)
    mid = Column(Integer, ForeignKey('message.mid'))
    cid = Column(Integer, ForeignKey('contact.cid'))
    mentioned_as = Column(Enum("FROM","TO","CC","BCC"))

def get_or_create(name, email, create_session=None):
    '''
    contact = get_or_create(name, email, create_session={backend.create_session})

    Retrieves or creates a new 
    '''
    from rbit.backend import call_create_session
    if name is None and email is None:
        raise ValueError('rbit.contact.get_or_create: both `name` and `email` are None')
    session = call_create_session(create_session)
    cids = [[]]
    def get(type, value):
        if value is not None:
            cids[0] += session. \
                    query(ContactInfo.cid). \
                    filter_by(type=type). \
                    filter_by(value=name). \
                    all()
    def check(key, value):
        if value is None:
            return None
        for c in cids[0]:
            c = session.query(Contact).get(c)
            if value in c[key]:
                return c
    get('name', name)
    get('email', email)

    c = check('email', email)
    if c is not None: return c

    c = check('name', name)
    if c is not None: return c
        
    c = Contact()
    if name is not None:
        c.add_info('name', name)
    if email is not None:
        c.add_info('email', email)
    return c
