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

    def list_messages(self, folder=None):
        self._select_folder(folder)
        return self.connection.search()

    def retrieve(self, folder, message):
        self._select_folder(folder)
        return self.connection.fetch(message, ['RFC822'])

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


