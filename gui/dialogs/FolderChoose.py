# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from os import path
from PySide import QtCore, QtGui, QtUiTools
from PySidePlus import qopen


def folderchoose_dialog():
    from rbglobals import cfg
    loader = QtUiTools.QUiLoader()
    uifilepath = path.join(
        path.dirname(__file__),
        'folderchoose.ui')
    with qopen(uifilepath) as uifile:
        dialog = loader.load(uifile)
    return dialog
