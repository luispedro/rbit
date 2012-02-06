# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from PySide.QtCore import QAbstractListModel, QAbstractItemModel, Qt
from PySide.QtGui import QApplication
from PySide.QtDeclarative import QDeclarativeComponent, QDeclarativeItem, QDeclarativeEngine


from rbit import config
from rbit import backend
from rbit import imap
from rbit import models

backend.init()
session = backend.create_session()

class MessageList(QAbstractListModel):
    _roles = xrange(Qt.UserRole, Qt.UserRole + 3)
    def __init__(self, messages):
        super(MessageList, self).__init__()
        self.messages = messages

        self.setRoleNames({
            Qt.UserRole: "from",
            Qt.UserRole+1: "subject",
            Qt.UserRole+2: "first",
            Qt.UserRole+3: "index",
            })

    def rowCount(self, parent):
        return len(self.messages)

    def data(self, index, role):
        m = self.messages[index.row()]
        if role == Qt.UserRole: return m.from_
        if role == Qt.UserRole+1: return m.subject
        if role == Qt.UserRole+2: return m.body[:64].replace('\n',' ')
        if role == Qt.UserRole+3: return index.row()
        return '<unknown>'


def load_qml(root, folder):
    messages = list_messages(folder)
    messages = MessageList(messages)
    engine = QDeclarativeEngine()
    root = engine.rootContext()
    root.setContextProperty('iMessages', messages)
    root.setContextProperty('iFolder', folder)
    c = QDeclarativeComponent(engine, 'rbit.qml', root)
    return c.create()

def list_messages(folder):
    messages = session\
            .query(models.Message) \
            .filter_by(folder=folder) \
            .order_by(models.Message.date) \
            .all()
    return messages

def main(argv):
    app = QApplication(argv)
    win = load_qml(app, 'INBOX')

    app.exec_()

if __name__ == '__main__':
    from sys import argv
    main(argv)
