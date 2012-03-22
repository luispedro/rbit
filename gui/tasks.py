# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from PySide import QtCore
import Queue

from rbit import signals
from gevent import monkey
# thread needs to be left alone
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

class UpdateMessages(QtCore.QObject):
    status = QtCore.Signal(str)
    done = QtCore.Signal()

    def __init__(self, parent):
        super(UpdateMessages, self).__init__(parent)
        signals.register('status', self.get_status)

    def get_status(self, code, message):
        if code == 'imap-update':
            self.status.emit(message)

    def perform(self):
        from rbit.sync import update_all_folders
        from rbit import config
        from rbit import backend
        from rbit import imap
        cfg = config.Config('config', backend.create_session)
        client = imap.IMAPClient.from_config(cfg)
        update_all_folders(client)
        client.close()
        self.done.emit()
