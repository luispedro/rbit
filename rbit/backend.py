# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import path

from .models import Base

_engine = None
_create_session = None

def init(database_file=None):
    global _engine, _create_session
    basename = 'rbit.sqlite3'
    if database_file is None:
        database_file = path.join(
                path.expanduser('~/.local/share/rbit'),
                'rbit.sqlite3')
    _engine = create_engine('sqlite:///' + database_file, echo=False)
    _create_session = sessionmaker(bind=_engine)
    create_tables()

def create_session():
    if _create_session is None:
        init()
    return _create_session()

def create_tables():
    '''
    create_tables()

    Creates all tables in database.
    '''
    if _engine is None:
        init()
    metadata = Base.metadata
    metadata.bind = _engine
    metadata.create_all()


def call_create_session(create_session_):
    '''
    session = call_create_session(create_session_)

    Implements a simple protocol that is common in rbit::

        if create_session_ is None: return backend.create_session()
        else: return create_session_()
    '''
    if create_session_ is None:
        create_session_ = create_session
    return create_session_()
