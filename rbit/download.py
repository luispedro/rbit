# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
import email

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

def message_to_model(client, folder, mid):
    '''
    message = retrieve_model(client, folder, mid)

    Retrieves message as models.Message
    '''
    m = client.retrieve(folder, mid)
    m = email.message_from_string(m[mid]['RFC822'])
    m = models.Message.from_email_message(m)
    if isinstance(m.body, list):
        for inner in m.body:
            text = get_text(inner)
            if text is not None:
                m.body = text
            else:
                f = save_attachment(folder, mid, inner)
                att = models.Attachment(mid=m,filename=f)
    return m

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
        return m.get_payload()
    if m.get_content_type() == 'multipart/alternative':
        for inner in m.get_payload():
            t = get_text(inner)
            if t is not None:
                return t
    return None

