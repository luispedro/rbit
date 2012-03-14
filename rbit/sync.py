# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
import email
from rbit import backend
from rbit import models
from rbit import signals
from rbit.decode import decode_unicode

def _attachments_dir(folder, mid, basedir=None):
    from os import path
    if basedir is None:
        basedir = path.join(
                path.expanduser('~/.local/share/rbit'),
                'attachments')
    return path.join(basedir, 'message-%s-%s' % (folder, mid))

def save_attachment(folder, mid, m, basedir=None):
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
    from os import path, makedirs
    dirname = _attachments_dir(folder, mid, basedir)
    filename = decode_unicode(m.get_filename(), m.get_charsets())
    if not filename:
        filename = 'attachment'
    filename = path.join(dirname, filename)
    try:
        makedirs(dirname)
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
    created = [model]
    for inner in m.walk():
        text = get_text(inner)
        if text is not None:
            model.body = text
        else:
            if inner.get_filename() is not None and inner.get_content_type() != 'application/pgp-signature':
                f = save_attachment(folder, uid, inner)
                att = models.Attachment(filename=f)
                model.attachments.append(att)
                created.append(att)
    return created


def get_text(m):
    '''
    text = get_text(m)

    Parameters
    ----------
    m : email.Message

    Returns
    -------
    text : unicode or None
        If a text is found, returns it; else, returns None
    '''
    if isinstance(m, (str,unicode)):
        return m
    if m.get_content_type() in ('text/plain','text/html'):
        text = m.get_payload(decode=True)
        return decode_unicode(text, m.get_charsets())

    def _first_of(m, content_type):
        for inner in m.get_payload():
            if isinstance(inner, (str,unicode)):
                return inner
            if inner.get_content_type() == content_type:
                return decode_unicode(inner.get_payload(decode=True), inner.get_charsets() + m.get_charsets())
    if m.get_content_type() in ('multipart/signed', 'multipart/alternative', 'multipart/mixed'):
        return _first_of(m, 'text/plain') or _first_of(m, 'text/html')
    return None

def update_folder(client, folder, create_session=None):
    '''
    nr_changes = update_folder(client, folder, create_session={backend.create_session})

    Parameters
    ----------
    client : rbit.Client
    folder : str or unicode
    create_session : callable, optional

    Returns
    -------
    nr_changes : int
        Number of messages added or removed (from local store)
    '''
    from os import unlink, rmdir
    session = backend.call_create_session(create_session)
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
        signals.emit('delete-message', [m])
        for at in m.attachments:
            try:
                unlink(at.filename)
            except OSError:
                pass
            session.delete(at)
        try:
            rmdir(_attachments_dir(m.folder, m.uid))
        except OSError:
            pass

        session.delete(m)
    session.commit()

    new = messages - current
    for uid in new:
        m = client.retrieve(folder, uid)
        m = m[uid]['RFC822']
        created = message_to_model(m, folder, uid)
        signals.emit('new-message', [m, folder, uid])
        session.add_all(created)
        session.commit()

    return len(extra)+len(new)

def update_all_folders(client, create_session=None):
    '''
    update_all_folders(client)

    Parameters
    ----------
    client : imap.Client
    '''
    for folder in client.list_all_folders():
        n = update_folder(client, folder, create_session)
        signals.emit('folder-update', (folder,))
        signals.emit('status', ('imap-update', '%s updates in %s' % (n,folder)))

