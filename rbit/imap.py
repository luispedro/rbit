# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

import imapclient

class IMAPClient(object):
    def __init__(self, host, username, password):
        self.connection = imapclient.IMAPClient(host, ssl=True)
        self.connection.login(username, password)
        self.folder = None

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


