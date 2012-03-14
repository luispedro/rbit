# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from os import path
from PySide import QtCore, QtGui, QtUiTools
from PySidePlus import qopen

from rbit import models
from rbit import messages
from rbit import index
from rbit import signals
from rbit import backend

from tasks import UpdateMessages
from messagelist import MessageList, MessageListItem


def search_messages(query):
    from rbglobals import session
    return [
        messages.load_message(f,u,lambda:session)
            for f,u in index.search(query)]



class RBitMain(QtCore.QObject):
    def __init__(self, parent=None):
        super(RBitMain, self).__init__(parent)
        loader = QtUiTools.QUiLoader()
        uifilepath = path.join(
            path.dirname(__file__),
            'rbitmain.ui')
        with qopen(uifilepath) as uifile:
            self.win = loader.load(uifile)

        self.win.messagelist.clicked.connect(self.set_message)
        self.win.action_Quit.triggered.connect(self.win.close)
        self.win.searchGo.clicked.connect(self.search)
        self.win.action_CheckMail.triggered.connect(self.check_mail)

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
        self.win.mbody.setText(m.body)

        while self.win.attachments.count():
            self.win.attachments.takeItem(0)

        for at in m.attachments:
            self.win.attachments.addItem(at.filename)
        self.win.tabWidget.setTabText(
            self.win.tabWidget.indexOf(self.win.tab_attach),
            QtGui.QApplication.translate("RBitMain", "Attachments (%s)", None, QtGui.QApplication.UnicodeUTF8) % len(m.attachments)
            )

    def search(self):
        q = self.win.searchBox.text()
        messages = search_messages(q)
        self.win.statusBar().showMessage(self.win.tr('Found %s messages') % len(messages))
        self.set_messagelist(messages)

    def check_mail(self):
        from rbglobals import client
        update = UpdateMessages(client)
        update.status.connect(self.win.statusBar().showMessage)
        update.done.connect(lambda: self.win.statusBar().showMessage(self.win.tr("Sync complete"), 4000))
        def updated(folder):
            if folder == self.foldername:
                self.metaObject().invokeMethod(self, 'update_folder', QtCore.Qt.QueuedConnection)
        signals.register('folder-update', updated)
        update.start()

    @QtCore.Slot(str)
    def open_folder(self, foldername):
        self.foldername = foldername
        self.update_folder()

    @QtCore.Slot()
    def update_folder(self):
        from rbglobals import session
        self.set_messagelist(messages.list_messages(self.foldername, lambda: session))

