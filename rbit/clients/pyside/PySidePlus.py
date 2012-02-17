from PySide import QtCore
from contextlib import contextmanager

@contextmanager
def qopen(filename, parent=None):
    '''
    with qopen as f:
        use f

    Parameters
    ----------
    filename : str
        filename to open

    Returns
    -------
    f : QtCore.QFile
    '''
    f = QtCore.QFile(filename, parent)
    yield f
    f.close()
