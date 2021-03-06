# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from __future__ import print_function
from PySide import QtGui, QtCore
from rbit.html2text import html2text
import re

PIXMAP_CACHE_MAX_SIZE = 512

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

    def remove_message(self, m):
        pos = self.messages.index(m)
        p = QtCore.QModelIndex()
        self.rowsAboutToBeRemoved.emit(p, pos, pos)
        del self.messages[pos]
        self.rowsRemoved.emit(p, pos, pos)

class MessageListItem(QtGui.QItemDelegate):
    def __init__(self, mlist, parent=None):
        super(MessageListItem, self).__init__(parent)
        self.mlist = mlist
        self.cache = {}


    def paint(self, painter, option, index):
        row = index.row()
        m = self.mlist.messages[row]
        state = int(option.state)
        key = (m.mid,state)
        pix = self.cache.get(key)
        if pix is None:
            if len(self.cache) > PIXMAP_CACHE_MAX_SIZE:
                self.cache.clear()
            pix = self.do_paint(option, m)
            self.cache[key] = pix
        p = option.rect.topLeft()
        painter.drawPixmap(p, pix)


    def do_paint(self, option, m):
        w, h = option.rect.width(), option.rect.height()
        pix = QtGui.QPixmap(w,h)
        pix.fill()
        painter = QtGui.QPainter(pix)

        r,g,b = 0,0,0
        rect = QtCore.QRect(0,0,w,h)

        flagstr = ''
        flags = set(f.flag for f in m.flags)
        if r'\Answered' in flags or \
           r'$Replied' in flags or \
           r'$REPLIED' in flags:
            flagstr += "R"
        if r'$ATTACHMENT' in flags:
            flagstr += "A"

        predictions = ""
        for p in m.predictions:
            if p.type == 'folder':
                predictions = '     -> {0.value}'.format(p)
                break

        if option.state & QtGui.QStyle.State_MouseOver:
            painter.fillRect(rect, option.palette.color(QtGui.QPalette.Highlight).lighter())
        if option.state & QtGui.QStyle.State_Selected:
            painter.fillRect(rect, option.palette.color(QtGui.QPalette.Highlight))

        painter.save()
        font = painter.font()
        font.setWeight(QtGui.QFont.Bold)
        painter.setFont(font)
        painter.setPen(QtGui.QColor(int(255*r), int(255*g), int(255*b)))
        painter.drawText(rect, QtCore.Qt.TextSingleLine, u'{0:<8} {1} ::: {2} {3}'.format(flagstr, m.from_, m.subject, predictions))
        painter.restore()
        rect.setTop(rect.top() + 12)
        text = html2text(m.body)
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        try:
            painter.drawText(rect, QtCore.Qt.TextSingleLine, text)
        except UnicodeEncodeError: # I am not sure why this happens, but it sometimes does
            text = text.encode('utf-8')
            painter.drawText(rect, QtCore.Qt.TextSingleLine, text)
        rect.setTop(rect.top() + 12 + 4)
        return pix
    
    def sizeHint(self, options, index):
        return QtCore.QSize(0, 12 + 12 + 4 + 4)

    def createEditor(self):
        return None
