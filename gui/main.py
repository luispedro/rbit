# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from PySide.QtGui import QApplication, QMainWindow, QListView

from rbit import config
from rbit import backend
from rbit import imap

from RBitMain import RBitMain
from ConfigDialog import config_dialog

def main(argv):
    from rbglobals import cfg
    app = QApplication(argv)
    main = RBitMain(app)
    app.aboutToQuit.connect(main.aboutToQuit)
    app.aboutToQuit.connect(main.worker.kill)
    main.win.show()
    if cfg.has_entry('account', 'user'):
        foldername = 'INBOX'
        account = '{0}@{1}'.format(cfg.get('account', 'user'), cfg.get('account', 'host'))
        main.open_folder(account, foldername)
    else:
        dialog = config_dialog()
        dialog.accepted.connect(main.win.action_CheckMail.trigger)
        dialog.show()
    app.exec_()

if __name__ == '__main__':
    from sys import argv
    main(argv)
