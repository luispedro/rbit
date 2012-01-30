# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
import email
from rbit import models

_basedir = 'attachments'
def save_attachment(folder, mid, m):
    '''
    save_attachment(folder, mid, m)

    If m represents an attachment from message `mid` in folder `folder`, save
    it.

    Parameters
    ----------
    folder : str or unicode
        Folder name
    mid : int
        Message ID
    m : email.Message
        The attachment
    '''
    from os import path, mkdir
    from cStringIO import StringIO
    from email.utils import base64
    dirname = path.join(_basedir, 'message-%s-%s' % (folder, mid))
    filename = path.join(dirname, m.get_filename())
    try:
        mkdir(dirname)
    except:
        pass
    with open(filename, 'w') as output:
        base64.decode(StringIO(m.get_payload()), output)
    return filename

def message_to_model(client, folder, uid):
    '''
    message = retrieve_model(client, folder, uid)

    Retrieves message as models.Message

    Parameters
    ----------
    client : imap.Client
    folder : str
    uid : int
        IMAP UID
    folderm : models.Folder, optional
    '''
    m = client.retrieve(folder, uid)
    m = email.message_from_string(m[uid]['RFC822'])
    model = models.Message.from_email_message(m, uid)
    model.folder = folder
    for inner in m.walk():
        text = get_text(inner)
        if text is not None:
            model.body = text
        else:
            if inner.get_filename() is not None:
                f = save_attachment(folder, uid, inner)
                att = models.Attachment(mid=model,filename=f)
    return model

def get_text(m):
    '''
    text = get_text(m)

    Parameters
    ----------
    m : email.Message

    Returns
    -------
    text : str or None
        If a text is found, returns it; else, returns None
    '''
    if m.get_content_type() in ('text/plain','text/html'):
        text = m.get_payload(decode=True)
        for charset in m.get_charsets():
            try:
                return unicode(text, charset)
            except:
                pass
        return unicode(text, 'utf-8')
    if m.get_content_type() == 'multipart/alternative':
        for inner in m.get_payload():
            t = get_text(inner)
            if t is not None:
                return t
    return None

def update_folder(client, folder, create_session):
    '''
    nr_changes = update_folder(client, folder, create_session)

    Parameters
    ----------
    client : rbit.Client
    folder : str or unicode
    create_session : callable

    Returns
    -------
    nr_changes : int
        Number of messages added or removed (from local store)
    '''
    session = create_session()
    messages = set(client.list_messages(folder))
    current = set(uid for uid, in
                    session.query(models.Message.uid).filter_by(folder=folder).all())

    extra = current - messages
    for uid in extra:
        m = session.query(models.Message).filter_by(folder=folder, uid=uid).first()
        session.delete(m)
    session.commit()

    new = messages - current
    for uid in new:
        m = message_to_model(client, folder, uid)
        session.add(m)
    session.commit()

    return len(extra)+len(new)
