from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import path

from rbit.models import Base

def in_memory_sessionmaker():
    engine = create_engine('sqlite://')
    metadata = Base.metadata
    metadata.bind = engine
    metadata.create_all()
    return sessionmaker(engine)

def _open(fname):
    return open(path.join(
                path.dirname(path.abspath(__file__)),
                'data',
                fname))

