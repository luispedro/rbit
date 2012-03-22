# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

import sqlalchemy
from sqlalchemy import Column, String, Integer, Text, PickleType
from sqlalchemy.ext.declarative import declarative_base

from models import Base
__all__ = [
    'Config',
    ]

class ConfigEntry(Base):
    __tablename__ = 'config_entry'

    id = Column(Integer, primary_key=True)
    supergroup = Column(String)
    group = Column(String)
    name = Column(String)
    value = Column(PickleType)

config_index = sqlalchemy.Index('config_index',
        ConfigEntry.supergroup,
        ConfigEntry.group,
        ConfigEntry.name,
        )

def _config(supergroup, group, name, session):
    return session.query(ConfigEntry).filter_by(supergroup=supergroup,group=group,name=name).first()

def _config_set(supergroup, group, name, value, session):
    q = _config(supergroup, group, name, session)
    if q is None:
        q = ConfigEntry(supergroup=supergroup, group=group, name=name, value=value)
    else:
        q.value = value
    session.add(q)
    session.commit()

class Config(object):
    def __init__(self, supergroup, create_session=None):
        self.supergroup = supergroup
        self.session = create_session()

    def get(self, group, name):
        e = _config(self.supergroup, group, name, self.session)
        if e is None:
            raise KeyError('rbit.Config.get: Unknown key (%s,%s,%s)' % (self.supergroup, group, name))
        return e.value

    def has_entry(self, group, name):
        try:
            self.get(group, name)
            return True
        except KeyError:
            return False

    def get_default(self, group, name, default):
        try:
            return self.get(group, name)
        except KeyError:
            return default

    def set(self, group, name, value):
        _config_set(self.supergroup, group, name, value, self.session)

