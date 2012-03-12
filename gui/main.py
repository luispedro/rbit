# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from PySide.QtGui import QApplication, QMainWindow, QListView

from rbit import config
from rbit import backend
from rbit import imap

from RBitMain import RBitMain




def main(argv):
    app = QApplication(argv)
    main = RBitMain(app)
    main.open_folder('INBOX')
    main.win.action_CheckMail.trigger()
    main.win.show()
    app.exec_()

if __name__ == '__main__':
    from sys import argv
    main(argv)
