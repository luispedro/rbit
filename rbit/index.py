# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from rbit import models
from rbit import signals
from rbit.backend import create_session

_indexdir = 'indexdir'


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
            writer.add_document(body=m.body, subject=m.subject, from_=m.from_, recipient=m.to, date=m.date, path=('%s/%s' % (m.folder,m.uid)))
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
            writer.delete_by_term('path', '%s/%s' % (m.folder,m.uid))
            writer.commit()


    def register(self):
        '''
        index.register()

        Register signals for update of index
        '''
        signals.register('new-message', lambda m: self.add([m]))
        signals.register('delete-message', lambda m: self.add([m]))

    def search(self, q):
        '''
        for folder,uid in index.search(q):
            ...
        '''
        searcher = self.ix.searcher()
        q = unicode(q)
        q = self.parser.parse(q)
        for r in searcher.search(q):
            folder,uid = r['path'].split('/')
            uid = int(uid)
            yield folder, uid


def get_index():
    '''
    index = get_index()

    Returns the index
    '''
    from whoosh.index import open_dir, create_in, exists_in
    if exists_in(_indexdir):
        ix = open_dir(_indexdir)
        return index(ix)
    try:
        from os import mkdir
        mkdir(_indexdir)
    except OSError:
        pass
    from whoosh import fields as f
    schema = f.Schema(body=f.TEXT, subject=f.TEXT, from_=f.TEXT, recipient=f.TEXT, date=f.DATETIME, path=f.ID(stored=True, unique=True))
    ix = create_in(_indexdir, schema)
    return index(ix)
