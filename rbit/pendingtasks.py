# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from sqlalchemy import Column, String, Integer, ForeignKey, Text, DateTime, Float, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from rbit.models import Base
from rbit.backend import call_create_session

# This is coded such that, as long as the Database is working, no task ever
# gets lost, but it may be repeated multiple times if the system crashes at the
# wrong moment.

class PendingTask(Base):
    __tablename__ = 'pending_task'

    id = Column(Integer, primary_key=True)
    order = Column(Integer)
    task_object = Column(PickleType)

_next_order = None

def queue_task(t, create_session=None):
    session = call_create_session(create_session)
    if _next_order is None:
        _next_order = session. \
                            query(PendingTask.order). \
                            order_by(PendingTask.order). \
                            descending(). \
                            limit(1). \
                            one()
        if _next_order is None:
            _next_order = 0
        else:
            _next_order = 1+_next_order.order
    session.add(
        PendingTask(order=_next_order, task_object=t)
        )
    _next_order += 1
    session.commit()

def run_one(create_session=None):
    '''
    did_run = run_one(create_session={backend.create_session})
    '''
    session = call_create_session(create_session)
    task = session. \
            query(PendingTask). \
            order_by(PendingTask.order). \
            limit(1). \
            one()
    if task is None:
        return False
    task.execute()
    session.delete(task)
    session.commit()
    return True
