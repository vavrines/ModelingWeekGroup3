import sys
import time
import os
import numpy as np

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
                             QMenu, QPushButton, QRadioButton, QVBoxLayout, QWidget, QSlider, QComboBox,
    QLabel)
from PyQt5 import QtWidgets

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from glob import glob
from netCDF4 import Dataset


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QWidget()
        self.setCentralWidget(self._main)
        self.setGeometry(10, 60, 1500, 800)
        layout = QVBoxLayout(self._main)
        self.var = QComboBox();
        layout.addWidget(self.var)
        self.fillVars();
        self.var.currentTextChanged.connect(self.variableChanged)
        
        self.altVal = QLabel()
        self.timeVal = QLabel()
        
        layout.addWidget(self.altVal)
        layout.addWidget(self.timeVal)
        
        self.x, self.y, self.altitudes = self.get_axes_and_alt()
        self.times = {}
        self.get_times()
        static_canvas = FigureCanvas(Figure(figsize=(5, 8)))
        layout.addWidget(static_canvas)

        self._static_ax = static_canvas.figure.subplots()
        
#         self._dynamic_ax = dynamic_canvas.figure.subplots()
#         self._timer = dynamic_canvas.new_timer(
#             100, [(self._update_canvas, (), {})])
#         self._timer.start()
        self.sl_time = QSlider(Qt.Horizontal)
        self.sl_time.setMinimum(0)
        self.sl_time.setMaximum(len(self.times.keys()) - 1)
        self.sl_time.setValue(0)
        self.sl_time.setTickPosition(QSlider.TicksBelow)
        self.sl_time.setTickInterval(1)
          
        layout.addWidget(self.sl_time)
        self.sl_time.valueChanged.connect(self.valuechange_time)
        self.blockChanges = False
        
        self.sl_alt = QSlider(Qt.Horizontal)
        self.sl_alt.setMinimum(0)
        self.sl_alt.setMaximum(len(self.altitudes) - 1)
        self.sl_alt.setValue(0)
        self.sl_alt.setTickPosition(QSlider.TicksBelow)
        self.sl_alt.setTickInterval(1)
        layout.addWidget(self.sl_alt)
        self.sl_alt.valueChanged.connect(self.valuechange_alt)
        
        self.fig, self.ax = plt.subplots()
        
        self.update_plot()
        self.setLayout(layout)
        self.setWindowTitle("Visualisation demo")
    
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
        if not self.blockChanges:
            self.blockChanges = True
            self.update_plot()
        #size = self.sl_time.value()
        #self.l1.setFont(QFont("Arial",size))
        
    def valuechange_alt(self):
        if not self.blockChanges:
            self.blockChanges = True
            self.update_plot()

    def update_plot(self):
        self.altVal.setText("Altitude: %f"%(sorted(self.altitudes)[self.sl_alt.value()]))
        self.timeVal.setText("Time: %f"%(sorted(self.times.keys())[self.sl_time.value()]))
        dataset = Dataset(self.times[sorted(self.times.keys())[self.sl_time.value()]])
        values = np.array(dataset.variables[self.var.currentText()][list(dataset.variables['time']).index(sorted(self.times.keys())[self.sl_time.value()])]
                          [list(dataset.variables['alt']).index(sorted(self.altitudes)[self.sl_alt.value()])])
        self._static_ax.clear()
          
        #self.clb.remove()
        self.im = self._static_ax.imshow(values)
        try:
            self.clb.remove()
            del self.clb
        except:
            pass
        self.clb = self._static_ax.figure.colorbar(self.im)
        self._static_ax.set_xlabel('lon')
        xticks = [i for i in range(0, len(self.x), int(len(self.x) / 10))]
        xtickslabels = [self.x[i] for i in range(0, len(self.x), int(len(self.x) / 10))]
        yticks = [i for i in range(0, len(self.y), int(len(self.y) / 10))]
        ytickslabels = [self.y[i] for i in range(0, len(self.y), int(len(self.y) / 10))]
        self._static_ax.set_ylabel('lat')
        self._static_ax.set_xticks(xticks)
        self._static_ax.set_xticklabels(xtickslabels)
        self._static_ax.set_yticks(yticks)
        self._static_ax.set_yticklabels(ytickslabels)
        self._static_ax.figure.canvas.draw()
        self.blockChanges = False
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