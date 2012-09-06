# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from os import path
from PySide import QtCore, QtGui, QtUiTools
from PySide.QtWebKit import QWebView
from PySidePlus import qopen

from rbit import models
from rbit import messages
from rbit import index
from rbit import signals
from rbit import backend

from tasks import GEventLoop, UpdateMessages, TrashMessage, MoveMessage
from messagelist import MessageList, MessageListItem


def search_messages(query):
    from rbglobals import index
    return [
        messages.load_message(f,u)
            for f,u in index.search(query)]


def _format_as_html(text):
    if '<html>' in text or \
        '<body>' in text: return text
    return '<html><head></head><body><pre>%s</pre></html>' % text

class RBitMain(QtCore.QObject):
    def __init__(self, parent=None):
        super(RBitMain, self).__init__(parent)
        loader = QtUiTools.QUiLoader()
        uifilepath = path.join(
            path.dirname(__file__),
            'rbitmain.ui')
        with qopen(uifilepath) as uifile:
            self.win = loader.load(uifile)

        self.active_message = None
        self.foldername = None
        self.in_check_mail = False
        self.win.messagelist.clicked.connect(self.set_message)
        self.win.action_Quit.triggered.connect(self.win.close)
        self.win.searchGo.clicked.connect(self.search)
        self.win.action_CheckMail.triggered.connect(self.check_mail)
        self.win.action_Trash.triggered.connect(self.trash)
        self.win.actionAuto_Move.triggered.connect(self.auto_move)
        self.win.actionNew_Message.triggered.connect(self.new_message)
        self.worker = GEventLoop(self)
        self.worker.start()

    def set_messagelist(self, messages):
        messages = MessageList(messages)
        self.win.messagelist.setModel(messages)
        self.win.messagelist.setItemDelegate(MessageListItem(messages.messages, self.win.messagelist))
        if messages.rowCount(None):
            self.set_message(messages.createIndex(0,0))

    def set_message(self, index):
        m = self.win.messagelist.model().messages[index.row()]
        self.win.from_.setText(m.from_)
        self.win.date.setText(str(m.date))
        self.win.subject.setText(m.subject)
        self.win.mbody.setHtml(_format_as_html(m.body))

        while self.win.attachments.count():
            self.win.attachments.takeItem(0)

        for at in m.attachments:
            self.win.attachments.addItem(at.filename)
        self.win.tabWidget.setTabText(
            self.win.tabWidget.indexOf(self.win.tab_attach),
            QtGui.QApplication.translate("RBitMain", "Attachments (%s)", None, QtGui.QApplication.UnicodeUTF8) % len(m.attachments)
            )
        self.active_message = m

    def search(self):
        q = self.win.searchBox.text()
        messages = search_messages(q)
        self.win.statusBar().showMessage(self.win.tr('Found %s messages') % len(messages))
        self.set_messagelist(messages)

    def check_mail(self):
        if self.in_check_mail:
            self.win.statusBar().showMessage(self.win.tr("Already checking mail"), 4000)
            return

        self.in_check_mail = True
        update = UpdateMessages(self)
        update.status.connect(self.win.statusBar().showMessage)
        @update.done.connect
        def _done():
            self.win.statusBar().showMessage(self.win.tr("Sync complete"), 4000)
            self.in_check_mail = False
        @update.error.connect
        def _err(err):
            self.win.statusBar().showMessage(self.win.tr("Error in sync: %s") % err, 4000)
            self.in_check_mail = False

        @signals.register_dec(signals.FOLDER_UPDATE)
        def updated(folder, n):
            if n != 0 and folder == self.foldername:
                self.metaObject().invokeMethod(self, 'update_folder', QtCore.Qt.QueuedConnection)
        self.worker.spawn(update.perform)

    def trash(self):
        self._trash_or_move('trash')

    def auto_move(self):
        self._trash_or_move('move')

    def update_active_message(self):
        idx = self.win.messagelist.currentIndex()
        self.set_message(idx)

    def _trash_or_move(self, action):
        if self.active_message is None:
            return
        tr = self.win.tr
        model = self.win.messagelist.model()
        model.messages.remove(self.active_message)
        if action == 'move':
            for pred in self.active_message.predictions:
                if pred.type == 'folder':
                    target = pred.value
                    break
            else:
                self.win.statusBar().showMessage(tr("Could not auto-move message"), 4000)
                return
            task = MoveMessage(self, self.active_message, target)
        else:
            task = TrashMessage(self, self.active_message)
        task.error.connect(lambda err: \
                            self.win.statusBar().showMessage(tr("Error in %s action: %s") % (tr(action),err), 4000))
        self.worker.spawn(task.perform)
        self.active_message = None
        self.update_active_message()

    def new_message(self):
        from Composer import Composer
        c = Composer(self)
        c.show()

    @QtCore.Slot(str)
    def open_folder(self, foldername):
        self.foldername = foldername
        self.update_folder()

    @QtCore.Slot()
    def update_folder(self):
        self.set_messagelist(messages.list_messages(self.foldername))


