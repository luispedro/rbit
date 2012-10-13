import matplotlib
import numpy as np


matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'


from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class MatplotlibWidget(FigureCanvas):

    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(Figure())

        self.setParent(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.gca()


