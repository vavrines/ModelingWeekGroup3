import sys
import time
import os
import numpy as np

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                             QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QSlider, QComboBox,
    QLabel, QLineEdit, QHBoxLayout)
from PyQt5 import QtWidgets



import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from glob import glob
from netCDF4 import Dataset
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import figure


def multidim_intersect(arr1, arr2):
    arr1_view = arr1.view([('',arr1.dtype)]*arr1.shape[1])
    arr2_view = arr2.view([('',arr2.dtype)]*arr2.shape[1])
    intersected = numpy.intersect1d(arr1_view, arr2_view)
    #return intersected.view(arr1.dtype).reshape(-1, arr1.shape[1])
    return intersected

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QWidget()
        self.setCentralWidget(self._main)
        self.setGeometry(10, 60, 1500, 800)
        layout = QVBoxLayout(self._main)
        self.var = QComboBox();
        layout.addWidget(self.var)
        self.times = {}
        self.get_times()
        limits = QHBoxLayout(self._main)
        limits.addStretch(0)
        descrip = QLabel()
        descrip.setText('Enter range of values for visualisation. First min then max. will be multiplied by 10^-6')
        self.limitmin = QLineEdit()
        self.limitmax = QLineEdit()
        self.limitmin.setText('0')
        self.limitmax.setText('1')
        limits.addWidget(descrip)
        limits.addWidget(self.limitmin)
        limits.addWidget(self.limitmax)
        layout.addLayout(limits)

        botLayout = QHBoxLayout(self._main)
        
        self.sl_time = QSlider(Qt.Horizontal)
        self.sl_time.setMinimum(0)
        self.sl_time.setMaximum(19)
        self.sl_time.setValue(0)
        self.sl_time.setTickPosition(QSlider.TicksBelow)
        self.sl_time.setTickInterval(1)
        botLayout.addWidget(self.sl_time)


        self.updateButton = QPushButton()
        self.updateButton.setText('Update')
        self.updateButton.clicked.connect(self.update_plot)
        botLayout.addWidget(self.updateButton)
        layout.addLayout(botLayout)


#         self.fig = Figure(figsize = (5,5), dpi = 100)
#         self.ax = self.fig.add_subplot(1,1,1)# projection='3d')
#         self.canvas = FigureCanvasTkAgg(self.fig)
#         self.canvas.draw()
        self.fig = figure()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        self.ax = self.fig.add_subplot(111, projection='3d')


        

        self.setLayout(layout)
        self.setWindowTitle("Visualisation demo")

    
    def getLimits(self):
        return (float(self.limitmin.text().replace(',', '.')), float(self.limitmax.text().replace(',', '.')))
    
    def fillVars(self):
        dataset = Dataset(glob("*")[0])
        vars = list(dataset.variables.keys())
        vars.remove('lat')
        vars.remove('alt')
        vars.remove('time')
        vars.remove('lon')
        self.var.addItems(vars)
        self.var.setCurrentText('pv')
        
    def variableChanged(self):
        if not self.blockChanges:
            self.blockChanges = True
            self.update_plot()
        
    
    def valuechange_time(self):
        pass
        #size = self.sl_time.value()
        #self.l1.setFont(QFont("Arial",size))
        
    def update_plot(self):
        dataset = Dataset(self.times[sorted(self.times.keys())[self.sl_time.value()]])
        minval, maxval = self.getLimits()
        curTime = list(dataset.variables['time']).index(sorted(self.times.keys())[self.sl_time.value()])
        pv = dataset.variables['pv'][curTime]
        a_alt, a_lat, a_lon = np.where(pv>1.99*10**-6)
        b_alt, b_lat, b_lon = np.where(pv<2.01*10**-6)
        
        a_complete = np.hstack((a_alt.reshape(a_alt.size, 1), a_lat.reshape(a_alt.size, 1), a_lon.reshape(a_alt.size, 1)))
        b_complete = np.hstack((b_alt.reshape(b_alt.size, 1), b_lat.reshape(b_alt.size, 1), b_lon.reshape(b_alt.size, 1)))
        
        points = multidim_intersect(a_complete, b_complete)
        
        dataset.close()

    def _update_canvas(self):
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._dynamic_ax.figure.canvas.draw()
        
    def get_axes_and_alt(self):
        dataset = Dataset(glob('*')[0])
        x = np.array(dataset.variables['lon'])
        y = np.array(dataset.variables['lat'])
        alt = list(np.array(dataset.variables['alt']))
        alt.sort()
        dataset.close()
        return x, y, alt
    def get_times(self):
        for path in glob('*'):
            dataset = Dataset(path)
            for t in np.array(dataset.variables['time']):
                if t not in self.times.keys():
                    self.times[t] = path
            dataset.close()

    

os.chdir('D:\\My Docs\\ModelingWeek\\data')
#os.chdir('F://data/0216')

qapp = QtWidgets.QApplication(sys.argv)
app = ApplicationWindow()
app.show()
qapp.exec_()