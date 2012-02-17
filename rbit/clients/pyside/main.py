# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from PySide.QtGui import QApplication, QMainWindow, QListView

from rbit import config
from rbit import backend
from rbit import imap
from rbit import models

from messagelist import MessageList, MessageListItem

backend.init()
session = backend.create_session()

class RBitWindow(QMainWindow):
    def __init__(self, parent):
        super(RBitWindow, self).__init__(parent)

        from rbitmain import Ui_RBitMain
        self.builder = Ui_RBitMain()
        self.builder.setupUi(self)
        self.builder.messagelist.setViewMode(QListView.ListMode)


def list_messages(folder):
    messages = session\
            .query(models.Message) \
            .filter_by(folder=folder) \
            .order_by(models.Message.date) \
            .all()
    return messages

def main(argv):
    app = QApplication(argv)
    win = RBitWindow(None)
    messages = list_messages('INBOX')
    messages = MessageList(messages)
    win.builder.messagelist.setModel(messages)
    win.builder.messagelist.setItemDelegate(MessageListItem(messages.messages,win.builder.messagelist))
    win.show()
    app.exec_()

if __name__ == '__main__':
    from sys import argv
    main(argv)
