# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

import imapclient

def breakup(seq, n):
    if not (n > 0):
        raise ValueError("breakup: n must be greater than zero (got {0}).".format(n))
    cur = []
    for s in seq:
        if len(cur) == n:
            yield cur
            cur = []
        cur.append(s)
    if len(cur):
        yield cur

class IMAPClient(object):
    def __init__(self, host, port, username, password, ssl=True):
        port = int(port)
        self.connection = imapclient.IMAPClient(host, port=port, ssl=ssl)
        self.connection.login(username, password)
        self.folder = None
        self.account = '{0}@{1}'.format(username, host)

    @staticmethod
    def from_config(cfg):
        return IMAPClient(
                    cfg.get('account', 'host'),
                    cfg.get('account', 'port'),
                    cfg.get('account', 'user'),
                    cfg.get('account', 'password'),
                    cfg.get_default('account', 'ssl', True))

    def close(self):
        pass

    def _select_folder(self, folder):
        if folder is None:
            return
        if self.folder != folder:
            return self.connection.select_folder(folder)

    def select_folder(self, folder):
        return self.connection.select_folder(folder)

    def flags(self, folder, uids):
        self._select_folder(folder)
        res = self.connection.fetch(uids, ['FLAGS'])
        return {u:r['FLAGS'] for u,r in res.iteritems()}

    def fetch_flags_since(self, modseq):
        return self.connection.fetch('1:*', ['FLAGS'], ['CHANGEDSINCE %s' % modseq])

    def list_messages(self, folder=None):
        self._select_folder(folder)
        return self.connection.search()

    def retrieve_many(self, folder, messages):
        import gevent
        import gevent.queue
        if not messages: return
        self._select_folder(folder)
        q = gevent.queue.Queue(32)
        def perform_retrieve():
            for block in breakup(messages, 8):
                ms = self.connection.fetch(block, ['RFC822', 'FLAGS'])
                for k in ms:
                    q.put(( k, {k:ms[k]} ))
            q.put(StopIteration)
        gevent.spawn(perform_retrieve)
        for r in q:
            yield r
            gevent.sleep()

    def retrieve(self, folder, message):
        [m] = self.retrieve_many(folder, [message])
        return m

    def trash_messages(self, uids, trash_folder='INBOX.Trash'):
        self.move_messages(uids, trash_folder)

    def move_messages(self, uids, destination_folder):
        self.connection.copy(uids, destination_folder)
        return self.connection.delete_messages(uids)

    def expunge(self):
        self.connection.expunge()

    def list_all_folders(self):
        '''
        for f in client.list_all_folders():
            ...

        Generate all folders on the server
        '''
        self._select_folder('INBOX')
        yield 'INBOX'
        for _,_,f in self.connection.list_sub_folders():
            yield f


