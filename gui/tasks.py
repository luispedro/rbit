# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from __future__ import print_function
from PySide import QtCore
import Queue

from rbit import signals

def run_from_queue(group, q):
    from gevent import monkey
    # thread needs to be left alone as Qt handles those
    monkey.patch_all(thread=False)

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
    progress = QtCore.Signal(int, int)
    done = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(RBitTask, self).__init__(*args, **kwargs)
        self.dead = False

    def schedule_death(self):
        '''
        task.schedule_death()

        This method should cause the task to complete at its earliest
        convenience. There are no garantees on how long this should take,
        however.
        '''
        self.dead = True

    def perform(self):
        try:
            self._perform()
            self.done.emit()
        except Exception as err:
            from sys import stderr
            import traceback
            self.error.emit(str(err))
            traceback.print_exc(file=stderr)

class RetrainFolderModel(RBitTask):
    def _perform(self):
        from rbit.ml import train, predict
        self.status.emit('Retraining folder model...')
        train.retrain_folder_model()
        predict.init()

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
        from rbglobals import index
        cfg = config.Config('config', backend.create_session)
        self.status.emit('Updating messages from %s' % cfg.get('account', 'host'))

        signals.register(signals.NEW_MESSAGE, predict.predict_inbox, replace_all=True)
        index.register()

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

class PredictMessages(RBitTask):
    def __init__(self, parent, account, uids):
        super(PredictMessages, self).__init__(parent)
        self.account = account
        self.uids = uids

    def _perform(self):
        from rbit.ml import predict
        from rbit.backend import create_session
        from rbit.models import Message
        session = create_session()
        for uid in self.uids:
            message = session.\
                        query(Message).\
                        filter_by(account=self.account).\
                        filter_by(uid=uid).\
                        filter_by(folder=u'INBOX').\
                        one()
            if message is not None:
                predict.predict_inbox(message, u'INBOX', uid, session=session)
        session.commit()

def paginate(xs, n):
    s = 0
    while s < len(xs):
        yield xs[s:s+n]
        s += n

class ReindexMessages(RBitTask):
    def _perform(self):
        import rbglobals
        from rbit import index as rbit_index
        from rbit.backend import create_session
        from rbit.models import Message
        from rbit.imap import breakup
        rbglobals.index.close()
        rbit_index.remove_index()
        rbglobals.index = rbit_index.get_index()
        session = create_session()
        mids = session.query(Message.mid).all()
        STEP = 256
        for done,ms in enumerate(paginate(mids, STEP)):
            self.progress.emit(done*STEP, len(mids))
            messages = [Message.load_by_mid(m, create_session=(lambda:session)) for m in ms]
            rbglobals.index.add(messages)
            session.expunge_all()
            if self.dead:
                break
        self.status.emit('Message reindexing complete')

