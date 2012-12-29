# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from rbit import backend
from rbit.models import Message, Folder

def load_message(account, folder, uid, create_session=None):
    '''
    m = load_message(account, folder, uid, create_session={backend.create_session})

    Parameters
    ----------
    account : str
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
            .filter_by(account=account) \
            .filter_by(uid=uid) \
            .first()

def list_messages(account, folder, create_session=None):
    '''
    ms = list_messages(account, folder, create_session={backend.create_session})

    Parameters
    ----------
    folder : str
    account : str
    create_session : callable, optional

    Returns
    -------
    ms : list of Message
    '''
    session = backend.call_create_session(create_session)
    return session.query(Message) \
            .filter_by(folder=folder) \
            .filter_by(account=account) \
            .order_by(Message.date.desc()) \
            .all()

def list_folders(account, create_session=None):
    '''
    fs = list_folders(account, create_session=None)

    Parameters
    ----------
    create_session : callable

    Returns
    -------
    fs : list of str
        Folder names
    '''
    session = backend.call_create_session(create_session)
    fs = session.query(Folder.name) \
            .filter_by(account=account) \
            .distinct() \
            .all()
    # fs is a list of 1-element tuples, so just flatten it:
    return [f for f, in fs]

def list_uids(account, folder=None, create_session=None):
    '''
    us = list_uids(account, folder={all folders}, create_session={backend.create_session})

    Parameters
    ----------
    account : str
    folder : str, optional
    create_session : callable, optional

    Returns
    -------
    us : list of int
    '''
    session = backend.call_create_session(create_session)
    q = session.query(Message.uid) \
            .filter_by(account=account)
    if folder is not None:
        q = q.filter_by(folder=folder)
    return q.all()

def folder_prediction(message):
    '''
    folder = folder_prediction(message)

    Returns auto move target. Returns ``None`` if there is no prediction.
    '''
    for pred in message.predictions:
        if pred.type == 'folder':
            return pred.value
