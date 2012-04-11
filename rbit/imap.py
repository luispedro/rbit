# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

import imapclient

class IMAPClient(object):
    def __init__(self, host, username, password):
        self.connection = imapclient.IMAPClient(host, ssl=True)
        self.connection.login(username, password)
        self.folder = None

    @staticmethod
    def from_config(cfg):
        return IMAPClient(
                    cfg.get('account', 'host'),
                    cfg.get('account', 'user'),
                    cfg.get('account', 'password'))


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

    def retrieve(self, folder, message):
        self._select_folder(folder)
        return self.connection.fetch(message, ['RFC822', 'FLAGS'])

    def trash_messages(self, uids, trash_folder='INBOX.Trash'):
        self.move_messages(uids, trash_folder)

    def move_messages(self, uids, destination_folder):
        self.connection.copy(uids, destination_folder)
        return self.connection.delete_messages(uids)

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


