# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from PySide import QtCore, QtGui, QtUiTools
from PySide.QtGui import QApplication, QMainWindow, QListView
from PySidePlus import qopen

from rbit import config
from rbit import backend
from rbit import imap
from rbit import models

from messagelist import MessageList, MessageListItem

backend.init()
session = backend.create_session()



def list_messages(folder):
    messages = session\
            .query(models.Message) \
            .filter_by(folder=folder) \
            .order_by(models.Message.date.desc()) \
            .all()
    return messages

def build_mainwindow():
    loader = QtUiTools.QUiLoader()
    with qopen('rbitmain.ui') as uifile:
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
    win.messagelist.clicked.connect(set_message)
    win.action_Quit.triggered.connect(win.close)
    return win

def main(argv):
    app = QApplication(argv)
    win = build_mainwindow()
    win.set_messagelist(list_messages('INBOX'))

    win.show()
    app.exec_()

if __name__ == '__main__':
    from sys import argv
    main(argv)
