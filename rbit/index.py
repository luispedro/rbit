# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from __future__ import print_function
from rbit import models
from rbit import signals
from rbit.backend import create_session

from os import path

class index(object):
    def __init__(self, ix):
        self.ix = ix
        from whoosh.qparser import QueryParser
        self.parser = QueryParser('body', schema=ix.schema)


    def add(self, messages):
        '''
        index.add(messages)

        Parameters
        ----------
        ix : whoosh.index
        messages : sequence of models.Message
        '''
        for m in messages:
            writer = self.ix.writer()
            writer.add_document(body=unicode(m.body),
                                    subject=unicode(m.subject),
                                    from_=unicode(m.from_),
                                    recipient=unicode(m.to),
                                    date=m.date,
                                    path=(u'{0}/{1}/{2}'.format(m.account, m.folder, m.uid)))
            writer.commit()


    def remove(self, messages):
        '''
        index.remove(messages)

        Removes messages from the ``index``

        Parameters
        ----------
        ix : whoosh.index
        messages : sequence of models.Message
        '''
        for m in messages:
            writer = self.ix.writer()
            writer.delete_by_term('path', '{0}/{1}/{2}'.format(m.account, m.folder, m.uid))
            writer.commit()


    def register(self):
        '''
        index.register()

        Register signals for update of index
        '''
        signals.register(signals.NEW_MESSAGE, lambda m,_f,_u, **kwargs: self.add([m]))
        signals.register(signals.DELETE_MESSAGE, lambda m: self.remove([m]))

    def search(self, q, limit=10):
        '''
        for account,folder,uid in index.search(q, limit=10):
            ...
        '''
        with self.ix.searcher() as searcher:
            q = unicode(q)
            q = self.parser.parse(q)
            for r in searcher.search(q, limit=limit):
                account,folder,uid = r['path'].split('/')
                uid = int(uid)
                yield account,folder, uid


def get_index():
    '''
    index = get_index()

    Returns the index
    '''
    from whoosh.index import open_dir, create_in, exists_in
    indexdir = path.join(
                path.expanduser('~/.local/share/rbit'),
                'indexdir')
    if exists_in(indexdir):
        ix = open_dir(indexdir)
        return index(ix)
    try:
        from os import makedirs
        makedirs(indexdir)
    except OSError:
        pass
    from whoosh import fields as f
    schema = f.Schema(body=f.TEXT, subject=f.TEXT, from_=f.TEXT, recipient=f.TEXT, date=f.DATETIME, path=f.ID(stored=True, unique=True))
    ix = create_in(indexdir, schema)
    return index(ix)
