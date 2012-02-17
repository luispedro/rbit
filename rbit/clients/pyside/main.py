# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from PySide import QtCore, QtGui, QtUiTools
from PySide.QtGui import QApplication, QMainWindow, QListView

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
            .order_by(models.Message.date) \
            .all()
    return messages

def main(argv):
    app = QApplication(argv)
    loader = QtUiTools.QUiLoader()
    uifile = QtCore.QFile("rbitmain.ui")
    win = loader.load(uifile)
    uifile.close()
    messages = list_messages('INBOX.Sent')
    messages = MessageList(messages)
    win.messagelist.setModel(messages)
    win.messagelist.setItemDelegate(MessageListItem(messages.messages,win.messagelist))
    def set_message(index):
        m = messages.messages[index.row()]
        win.subject.setText(m.subject)
        win.mbody.setText(m.body)
    win.messagelist.clicked.connect(set_message)
    set_message(messages.createIndex(0,0))
    win.show()
    app.exec_()

if __name__ == '__main__':
    from sys import argv
    main(argv)
