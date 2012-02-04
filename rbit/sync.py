# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
import email
from rbit import models
from rbit.decode import decode_unicode

def save_attachment(folder, mid, m, basedir='attachments'):
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
    dirname = path.join(basedir, 'message-%s-%s' % (folder, mid))
    filename = path.join(dirname, m.get_filename())
    try:
        mkdir(dirname)
    except:
        pass
    with open(filename, 'w') as output:
        if m.get_content_type() == 'message/rfc822':
            output.write(m.as_string())
        else:
            output.write(m.get_payload(decode=True))
    return filename

def message_to_model(message, folder, uid):
    '''
    message = retrieve_model(message, folder, uid)

    Retrieves message as models.Message

    Parameters
    ----------
    message : str
        RFC822 representation of message
    folder : str
    uid : int
        IMAP UID
    folderm : models.Folder, optional
    '''
    m = email.message_from_string(message)
    model = models.Message.from_email_message(m, uid)
    model.folder = folder
    for inner in m.walk():
        text = get_text(inner)
        if text is not None:
            model.body = text
        else:
            if inner.get_filename() is not None and inner.get_content_type() != 'application/pgp-signature':
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
    if isinstance(m, (str,unicode)):
        return m
    if m.get_content_type() in ('text/plain','text/html'):
        text = m.get_payload(decode=True)
        return decode_unicode(text, m.get_charsets())
    if m.get_content_type() in ('multipart/alternative', 'multipart/mixed', 'multipart/signed'):
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
    status = client.select_folder(folder)
    uidvalidity = status['UIDVALIDITY']

    folderm = session.query(models.Folder).filter_by(name=folder).first()
    if folderm is not None and folderm.uidvalidity != uidvalidity:
        # UIDs are INVALID
        # We need to clear the cache!
        session.delete(folderm)
        q = session.query(models.Message).filter_by(folder=folder).delete()
        session.commit()
        folderm = None

    if folderm is None:
        folderm = models.Folder(name=folder, uidvalidity=uidvalidity)
        session.add(folderm)

    messages = set(client.list_messages())
    current = set(uid for uid, in
                    session.query(models.Message.uid).filter_by(folder=folder).all())

    extra = current - messages
    for uid in extra:
        m = session.query(models.Message).filter_by(folder=folder, uid=uid).first()
        session.delete(m)
    session.commit()

    new = messages - current
    for uid in new:
        m = client.retrieve(folder, uid)
        m = message_to_model(m[uid]['RFC822'], folder, uid)
        session.add(m)
    session.commit()

    return len(extra)+len(new)