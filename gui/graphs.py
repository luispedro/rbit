# Copyright (C) 2012 Luis Pedro Coelho <luis@luispedro.org>
# This file is part of rbit mail.
from os import path
from PySide import QtCore, QtGui, QtUiTools
from PySidePlus import qopen

def plot_hours(dialog, grid):
    import numpy as np
    from MatplotlibWidget import MatplotlibWidget
    hours = MatplotlibWidget(dialog)

    hours.axes.bar(np.arange(24), grid.sum(0)*100)
    hours.axes.set_ylabel('Fraction of messages (%)')
    hours.axes.set_xlabel('hour of the day')
    return hours

def plot_days(dialog, grid):
    import numpy as np
    from MatplotlibWidget import MatplotlibWidget
    days = MatplotlibWidget(dialog)

    days.axes.bar(np.arange(7), grid.sum(1)*100)
    days.axes.set_ylabel('Fraction of messages (%)')
    days.axes.set_xlabel('Day of the Week')
    return days



# We need to save a reference to the dialog object
# Otherwise, it gets garbage collected.
dialog = None
def show_graph_dialog():
    from rbglobals import cfg
    from rbit import stats
    global dialog
    loader = QtUiTools.QUiLoader()
    uifilepath = path.join(
        path.dirname(__file__),
        'graphs.ui')
    with qopen(uifilepath) as uifile:
        dialog = loader.load(uifile)

    dialog.tabWidget.clear()
    # This should be off-loaded to a background thread
    grid = stats.day_hour_grid()
    dialog.tabWidget.addTab(plot_hours(dialog, grid), u'Hours')
    dialog.tabWidget.addTab(plot_days(dialog, grid), u'Days')
    dialog.show()

