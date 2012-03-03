# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from rbit import models
from rbit.backend import create_session

_indexdir = 'indexdir'
def get_index():
    '''
    ix = get_index()

    Returns the index
    '''
    from whoosh.index import open_dir, create_in, exists_in
    if exists_in(_indexdir):
        return open_dir(_indexdir)
    try:
        mkdir(_indexdir)
    except OSError:
        pass
    from whoosh import fields as f
    schema = f.Schema(body=f.TEXT, subject=f.TEXT, from_=f.TEXT, recipient=f.TEXT, date=f.DATETIME, path=f.ID(stored=True, unique=True))
    return create_in(_indexdir, schema)

def index_add(ix, messages):
    '''
    index_add(ix, messages)

    Parameters
    ----------
    ix : whoosh.index
    messages : sequence of models.Message
    '''
    for m in messages:
        writer = ix.writer()
        writer.add_document(body=m.body, subject=m.subject, from_=m.from_, recipient=m.to, date=m.date, path=('%s/%s' % (m.folder,m.uid)))
        writer.commit()

