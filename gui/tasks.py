# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from PySide import QtCore

from rbit import signals
from rbit.sync import update_all_folders

class UpdateMessages(QtCore.QThread):
    status = QtCore.Signal(str)
    done = QtCore.Signal()

    def __init__(self, client):
        super(UpdateMessages, self).__init__()
        self.client = client
        signals.register('status', self.get_status)

    def get_status(self, code, message):
        if code == 'imap-update':
            self.status.emit(message)

    def run(self):
        update_all_folders(self.client) 
        self.done.emit()

