# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

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

def message_to_model(client, folder, mid):
    '''
    message = retrieve_model(client, folder, mid)

    Retrieves message as models.Message
    '''
    m = client.retrieve(folder, mid)
    m = email.message_from_string(m[mid]['RFC822'])
    m = models.Message.from_email_message(m)
    return m


