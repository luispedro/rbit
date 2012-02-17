# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from PySide.QtCore import QAbstractListModel, QAbstractItemModel, QModelIndex, Qt
from PySide.QtGui import QApplication, QMainWindow, QStandardItemModel, QListView
from PySide.QtDeclarative import QDeclarativeComponent, QDeclarativeItem, QDeclarativeEngine, QDeclarativeProperty


from rbit import config
from rbit import backend
from rbit import imap
from rbit import models

backend.init()
session = backend.create_session()

class RBitWindow(QMainWindow):
    def __init__(self, parent):
        super(RBitWindow, self).__init__(parent)

        from rbitmain import Ui_RBitMain
        self.builder = Ui_RBitMain()
        self.builder.setupUi(self)
        self.builder.messagelist.setViewMode(QListView.ListMode)



class MessageList(QAbstractListModel):
    def __init__(self, messages):
        super(MessageList, self).__init__()
        self.messages = messages

    def rowCount(self, parent):
        return len(self.messages)

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if role == Qt.DisplayRole:
            m = self.messages[index.row()]
            return '<qt><b>%s</b> <i>%s</i> <br/>%s</qt>' % (m.from_,m.subject, m.body[:64].replace('\n', ' '))


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
    win.show()
    app.exec_()

if __name__ == '__main__':
    from sys import argv
    main(argv)
