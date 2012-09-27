# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from os import path
from PySide import QtCore, QtGui, QtUiTools
from PySidePlus import qopen

def config_dialog():
    from rbglobals import cfg
    loader = QtUiTools.QUiLoader()
    uifilepath = path.join(
        path.dirname(__file__),
        'configdialog.ui')
    with qopen(uifilepath) as uifile:
        dialog = loader.load(uifile)

    dialog.hostname.setText(cfg.get_default('account', 'host', ''))
    dialog.username.setText(cfg.get_default('account', 'user', ''))
    dialog.password.setText(cfg.get_default('account', 'password', ''))

    def sync_back():
        cfg.set('account', 'host', dialog.hostname.text())
        cfg.set('account', 'port', dialog.port.text())
        cfg.set('account', 'user', dialog.username.text())
        cfg.set('account', 'password', dialog.password.text())
    dialog.accepted.connect(sync_back)
    return dialog
