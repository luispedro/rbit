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

def list_folders(create_session=None):
    '''
    fs = list_folders(create_session=None)

    Parameters
    ----------
    create_session : callable

    Returns
    -------
    fs : list of str
        Folder names
    '''
    session = backend.call_create_session(create_session)
    fs = session.query(Message.folder) \
            .distinct() \
            .all()
    # fs is a list of 1-element tuples, so just flatten it:
    return [f for f, in fs]

def list_uids(folder=None, create_session=None):
    '''
    us = list_uids(folder={all folders}, create_session={backend.create_session})

    Parameters
    ----------
    folder : str, optional
    create_session : callable, optional

    Returns
    -------
    us : list of int
    '''
    session = backend.call_create_session(create_session)
    q = session.query(Message.uid)
    if folder is not None:
        q = q.filter_by(folder=folder)
    return q.all()
