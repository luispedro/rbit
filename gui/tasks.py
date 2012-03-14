# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from PySide import QtCore

from rbit import signals
from rbit.sync import update_all_folders

class UpdateMessages(QtCore.QThread):
    status = QtCore.Signal(str)
    done = QtCore.Signal()

    def __init__(self, parent):
        super(UpdateMessages, self).__init__(parent)
        signals.register('status', self.get_status)

    def get_status(self, code, message):
        if code == 'imap-update':
            self.status.emit(message)

    def run(self):
        from rbit import config
        from rbit import backend
        from rbit import imap
        cfg = config.Config('config', backend.create_session)
        client = imap.IMAPClient.from_config(cfg)
        update_all_folders(client)
        client.close()
        self.done.emit()

