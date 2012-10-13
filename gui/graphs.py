# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from os import path
from PySide import QtCore, QtGui, QtUiTools
from PySidePlus import qopen


# We need to save a reference to the dialog object
# Otherwise, it gets garbage collected.
dialog = None
def show_graph_dialog():
    from rbglobals import cfg
    global dialog
    loader = QtUiTools.QUiLoader()
    uifilepath = path.join(
        path.dirname(__file__),
        'graphs.ui')
    with qopen(uifilepath) as uifile:
        dialog = loader.load(uifile)

    dialog.show()
