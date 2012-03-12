# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from os import path

from PySide import QtCore, QtGui, QtUiTools
from PySide.QtGui import QApplication, QMainWindow, QListView
from PySidePlus import qopen

from rbit import config
from rbit import backend
from rbit import imap
from rbit import models
from rbit import index

from messagelist import MessageList, MessageListItem
from tasks import UpdateMessages


backend.init()
index = index.get_index()
cfg = config.Config('config', backend.create_session)
client = imap.IMAPClient.from_config(cfg)
session = backend.create_session()

def search_messages(query):
    return [
        models.load_message(f,u,lambda:session)
            for f,u in index.search(query)]


def list_messages(folder):
    messages = session\
            .query(models.Message) \
            .filter_by(folder=folder) \
            .order_by(models.Message.date.desc()) \
            .all()
    return messages

def build_mainwindow():
    loader = QtUiTools.QUiLoader()
    uifilepath = path.join(
        path.dirname(__file__),
        'rbitmain.ui')
    with qopen(uifilepath) as uifile:
        win = loader.load(uifile)

    def set_messagelist(messages):
        messages = MessageList(messages)
        win.messagelist.setModel(messages)
        win.messagelist.setItemDelegate(MessageListItem(messages.messages,win.messagelist))
        if messages.rowCount(None):
            set_message(messages.createIndex(0,0))

    win.set_messagelist = set_messagelist
    def set_message(index):
        m = win.messagelist.model().messages[index.row()]
        win.from_.setText(m.from_)
        win.date.setText(str(m.date))
        win.subject.setText(m.subject)
        win.mbody.setText(m.body)

        while win.attachments.count():
            win.attachments.takeItem(0)

        for at in m.attachments:
            win.attachments.addItem(at.filename)
        win.tabWidget.setTabText(
            win.tabWidget.indexOf(win.tab_attach),
            QtGui.QApplication.translate("RBitMain", "Attachments (%s)", None, QtGui.QApplication.UnicodeUTF8) % len(m.attachments)
            )
    def search():
        q = win.searchBox.text()
        messages = search_messages(q)
        print 'found', len(messages)
        win.set_messagelist(messages)
    win.messagelist.clicked.connect(set_message)
    win.action_Quit.triggered.connect(win.close)
    win.searchGo.clicked.connect(search)

    return win

def open_folder(win, foldername):
    win.set_messagelist(list_messages(foldername))

def main(argv):
    app = QApplication(argv)
    win = build_mainwindow()
    open_folder(win, 'INBOX')

    win.show()
    update = UpdateMessages(client)
    update.status.connect(win.statusBar().showMessage)
    update.done.connect(lambda: win.statusBar().showMessage(win.tr("Sync complete"), 4000))
    update.done.connect(lambda: open_folder(win, 'INBOX'))
    update.start()
    app.exec_()

if __name__ == '__main__':
    from sys import argv
    main(argv)
