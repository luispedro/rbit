# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.

from PySide.QtGui import QApplication
from PySide.QtDeclarative import QDeclarativeComponent, QDeclarativeItem, QDeclarativeEngine

def main(argv):
    app = QApplication(argv)
    engine = QDeclarativeEngine()
    root = QDeclarativeItem()
    c = QDeclarativeComponent(engine, 'rbit.qml', app)
    win = c.create()
    win.show()
    app.exec_()

if __name__ == '__main__':
    from sys import argv
    main(argv)
