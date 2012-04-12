# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from os import path
from PySide import QtCore, QtGui, QtUiTools
from PySidePlus import qopen

class Composer(QtCore.QObject):
    def __init__(self, parent=None):
        super(Composer, self).__init__(parent)
        loader = QtUiTools.QUiLoader()
        uifilepath = path.join(
            path.dirname(__file__),
            'composer.ui')
        with qopen(uifilepath) as uifile:
            self.composer = loader.load(uifile)
        self.show = self.composer.show

