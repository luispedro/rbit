# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
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

class MessageListItem(QtGui.QItemDelegate):
    def __init__(self, messages, parent=None):
        super(MessageListItem, self).__init__(parent)
        self.messages = messages
        self.cache = {}


    def paint(self, painter, option, index):
        row = index.row()
        m = self.messages[row]
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
                predictions += '%s (%.2f)' % (p.value, p.strength)

        if option.state & QtGui.QStyle.State_MouseOver:
            painter.fillRect(rect, option.palette.color(QtGui.QPalette.Highlight).lighter())
        if option.state & QtGui.QStyle.State_Selected:
            painter.fillRect(rect, option.palette.color(QtGui.QPalette.Highlight))

        painter.save()
        font = painter.font()
        font.setWeight(QtGui.QFont.Bold)
        painter.setFont(font)
        painter.drawText(rect, QtCore.Qt.TextSingleLine, u'{0:<8} {1} ::: {2}    -> {3}'.format(flagstr, m.from_, m.subject, predictions))
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
        painter.drawLine(rect.left(), rect.top(), (rect.left()+rect.right())//2, rect.top())
        return pix
    
    def sizeHint(self, options, index):
        return QtCore.QSize(0, 12 + 12 + 4 + 4)

    def createEditor(self):
        return None
