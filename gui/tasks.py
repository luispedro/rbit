# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from PySide import QtCore
import Queue

from rbit import signals
from gevent import monkey
# thread needs to be left alone as Qt handles those
monkey.patch_all(thread=False)

def run_from_queue(group, q):
    for message in q:
        if message == 'quit':
            group.kill()
            return
        group.spawn(message)

def transfer_queue(q, gq):
    import gevent
    while True:
        try:
            message = q.get_nowait()
            gq.put(message)
            if message == 'quit':
                return
        except Queue.Empty:
            gevent.sleep(1.)

class GEventLoop(QtCore.QThread):
    def __init__(self, parent=None):
        super(GEventLoop, self).__init__(parent)
        self.q = Queue.Queue()

    def spawn(self, f, *args, **kwargs):
        self.q.put(lambda: f(*args, **kwargs))

    def run(self):
        import gevent.queue
        from gevent.pool import Group
        gq = gevent.queue.Queue()
        group = Group()
        group.spawn(transfer_queue, self.q, gq)
        run_from_queue(group, gq)

    @QtCore.Slot()
    def kill(self):
        self.q.put('quit')
        self.wait()

class RBitTask(QtCore.QObject):
    error = QtCore.Signal(str)
    status = QtCore.Signal(str)
    done = QtCore.Signal()

    def perform(self):
        try:
            self._perform()
            self.done.emit()
        except Exception, err:
            self.error.emit(str(err))

class UpdateMessages(RBitTask):
    def __init__(self, parent):
        super(UpdateMessages, self).__init__(parent)
        signals.register(signals.STATUS, self.get_status)

    def get_status(self, code, message):
        if code == 'imap-update':
            self.status.emit(message)

    def _perform(self):
        from rbit.sync import update_all_folders
        from rbit import config
        from rbit import backend
        from rbit import imap
        from rbit.ml import predict
        cfg = config.Config('config', backend.create_session)
        self.status.emit('Updating messages from %s' % cfg.get('account', 'host'))

        predict.init()
        signals.register(signals.NEW_MESSAGE, predict.predict_inbox, replace_all=True)

        client = imap.IMAPClient.from_config(cfg)
        update_all_folders(client)
        client.close()

class MoveMessage(RBitTask):
    def __init__(self, parent, message, target):
        super(MoveMessage, self).__init__(parent)
        self.folder = message.folder
        self.uid = message.uid
        self.target = target

    def _perform(self):
        from rbit import config
        from rbit import backend
        from rbit import imap
        cfg = config.Config('config', backend.create_session)
        client = imap.IMAPClient.from_config(cfg)
        client.select_folder(self.folder)
        client.move_messages([self.uid], self.target)
        client.expunge()
        client.close()

class TrashMessage(MoveMessage):
    def __init__(self, parent, message):
        MoveMessage.__init__(self, parent, message, 'INBOX.Trash')

