# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from rbit import backend
from rbit.models import Message

def load_message(folder, uid, create_session=None):
    '''
    m = load_message(folder, uid, create_session={backend.create_session})

    Parameters
    ----------
    folder : str
    uid : int
    create_session : callable

    Returns
    -------
    m : Message or None
    '''
    session = backend.call_create_session(create_session)
    return session.query(Message) \
            .filter_by(folder=folder) \
            .filter_by(uid=uid) \
            .first()

def list_messages(folder, create_session=None):
    '''
    ms = list_messages(folder, create_session={backend.create_session})

    Parameters
    ----------
    folder : str
    create_session : callable

    Returns
    -------
    ms : list of Message
    '''
    session = backend.call_create_session(create_session)
    return session.query(Message) \
            .filter_by(folder=folder) \
            .order_by(Message.date.desc()) \
            .all()

