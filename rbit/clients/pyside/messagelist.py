# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from PySide import QtGui, QtCore

class MessageList(QtCore.QAbstractListModel):
    def __init__(self, messages):
        super(MessageList, self).__init__()
        self.messages = messages

    def rowCount(self, parent):
        return len(self.messages)

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        return None

class MessageListItem(QtGui.QItemDelegate):
    def __init__(self, messages, parent=None):
        super(MessageListItem, self).__init__(parent)
        self.messages = messages

    def paint(self, painter, option, index):
        m = self.messages[index.row()]
        rect = option.rect
        painter.save()
        font = painter.font()
        font.setWeight(QtGui.QFont.Bold)
        painter.setFont(font)
        painter.drawText(rect, '%s ::: %s' % (m.from_, m.subject))
        painter.restore()
        rect.setTop(rect.top() + 12)
        painter.drawText(rect, QtCore.Qt.TextSingleLine, m.body)
        rect.setTop(rect.top() + 12 + 4)
        painter.drawLine(rect.left(), rect.top(), (rect.left()+rect.right())//2, rect.top())
    
    def sizeHint(self, options, index):
        return QtCore.QSize(0, 12 + 12 + 4 + 4)

    def createEditor(self):
        return None
