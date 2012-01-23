# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import path

from models import Base

_engine = None
_create_session = None
_paths = [
    path.join(path.abspath(path.dirname(__file__)), '..'),
    '.',
    ]

def init(database_file=None):
    global _engine, _create_session
    basename = 'rbit.sqlite3'
    if database_file is None:
        for basep in _paths:
            fullp = path.join(basep, basename)
            if path.exists(fullp):
                database_file = fullp
                break
        else:
            database_file = path.join(_paths[0], basename)
    _engine = create_engine('sqlite:///' + database_file, echo=False)
    _create_session = sessionmaker(bind=_engine)

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
