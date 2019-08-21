#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from  matplotlib.lines import Line2D
from netCDF4 import Dataset

dataset = Dataset(r"E:\ModelingWeek\data\2016021600-ART-chemtracer_grid_reg_DOM02_HL_0007.nc")
print("The dimentions of the dataset are:\n ", dataset.dimensions.keys(), "\n")
print("The variables of the dataset are:\n ",  dataset.variables.keys(),  "\n")

time = dataset.variables['time']
lon = dataset.variables['lon']
lat = dataset.variables['lat']
alt = dataset.variables['alt']
time = dataset.variables['time']
PV = dataset.variables['pv']
qv = dataset.variables['qv']

pv = (10 ** 6) * PV[:]

plt.figure()
plt.pcolormesh(lon[:], alt[:], pv[3,: , 100, :])
plt.colorbar()

axes = plt.subplots(2, 2, sharex = True, sharey = True)
for i in range(2):
    for j in range(2):
        plt.subplot(2, 2, i+j*2+1)
        CS = plt.contour(lat[:], alt[:], pv[i+j, :, :, 100], [0, 2, 4])
        plt.clabel(CS, inline = 1, fontsize = 10)

        
        
# =================== find the indices =========================================
lenTime = len(time)
lenAlt = len(alt)
lenLon = len(lon)
lenLat = len(lat)

matrix = [[2 for i in range(lenLon)] for j in range(lenLat)]

numSlide = 0
indexOfLargeRange = [];
indices = []
length = 0;

indexOfTime = 0;
tolerrence = 0.001

for t in pv:
    print(t.shape)
    indexOfAlt = 0;
    for altitude in t:
        diff = np.abs(altitude - matrix)        
        if diff.min() < tolerrence:
            numSlide += 1
            firstTwoIndex = [indexOfTime, indexOfAlt]
            lastTwoIndex = np.asarray(np.where((altitude > 2-tolerrence) & (altitude < 2+tolerrence))).T
            lastTwoIndex = np.array(lastTwoIndex)
            firstTwoIndex = np.matlib.repmat(firstTwoIndex, len(lastTwoIndex), 1)
            index = np.concatenate((firstTwoIndex, lastTwoIndex), axis=1)
            if len(indices):
                indices = np.concatenate((indices, index), axis = 0)
            else:
                indices = index
            length = length + index.shape[0]

print("The number of  different slides: %d" %numSlide)
print("The number of index pairs is : %d" % length)
indices = np.array(indices)
indices = np.asarray(indices)
#indices = np.reshape(indices, (2, length))
print(indices.shape)


# ========== plot the altitude ======================================================
time0 = []
time1 = []
time2 = []
time3 = []
def Connection(time, index):
    if len(time) == 0:
        time = index
    else:
        time = np.column_stack((time, index))
    return time

for i in range(indices.shape[0]):
    valueOfFirstIndex = indices[i, 0]
    if valueOfFirstIndex == 0:
        time0 = Connection(time0, indices[i, :])
    elif valueOfFirstIndex == 1:
        time1 = Connection(time1, indices[i, :])
    elif valueOfFirstIndex == 2:
        time2 = Connection(time2, indices[i, :])
    else:
        time3 = Connection(time3, indices[i, :])
time0 = time0.T
time1 = time1.T
time2 = time2.T
time3 = time3.T


indexOfAlti = indices[:, 1]
indexOfLati = indices[:, 2]
indexOfLong = indices[:, 3]

get_ipython().run_line_magic('matplotlib', 'qt')
fig = plt.subplots(2, 2, sharex = True, sharey = True)
plt.subplots_adjust(right = 0.7)
ax1 = plt.subplot(2,2,1)
scatter = ax1.scatter(lon[time0[:, 3]], lat[time0[:, 2]], c = alt[time0[:, 1]])
ax2 = plt.subplot(2,2,2)
ax2.scatter(lon[time1[:, 3]], lat[time1[:, 2]], c = alt[time1[:, 1]])
ax3 = plt.subplot(2, 2, 3)
ax3.scatter(lon[time2[:, 3]], lat[time2[:, 2]], c = alt[time2[:, 1]])
ax4 = plt.subplot(2, 2, 4)
ax4.scatter(lon[time3[:, 3]], lat[time3[:, 2]], c = alt[time3[:, 1]])
plt.legend(*scatter.legend_elements(),bbox_to_anchor=(1.7, 1),loc = 'center right', borderaxespad = 0.1)
plt.show()

