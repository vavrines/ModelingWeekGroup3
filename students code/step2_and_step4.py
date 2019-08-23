#!/usr/bin/env python
# coding: utf-8

# In[36]:


import sys
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from  matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import Axes3D
from netCDF4 import Dataset


# In[2]:


dataset = Dataset(r"E:\ModelingWeek\data\2016021600-ART-chemtracer_grid_reg_DOM02_HL_0007.nc")
print("The dimentions of the dataset are:\n ", dataset.dimensions.keys(), "\n")
print("The variables of the dataset are:\n ",  dataset.variables.keys(),  "\n")


# In[135]:


time = dataset.variables['time']
lon = dataset.variables['lon']
lat = dataset.variables['lat']
alt = dataset.variables['alt']
time = dataset.variables['time']
PV = dataset.variables['pv']
qv = dataset.variables['qv']
qv = qv[:]

pv = (10 ** 6) * PV[:]
print(lon.units)
print(lat.units)
print(alt.units)
print(time.units)


# In[134]:


get_ipython().run_line_magic('matplotlib', 'qt')
latitudeIndex = 100
fig = plt.figure()
plt.pcolormesh(lon[:], alt[:], pv[3,: , latitudeIndex, :])
plt.colorbar()
plt.xlabel("lon/$^\circ$E")
plt.ylabel("alt/m")
plt.title("value of PV at latitude = %i $^\circ$N" % lat[latitudeIndex])

altitudeIndex = 30
fig = plt.figure()
plt.pcolormesh(lon[:], lat[:], pv[3, altitudeIndex, :, :])
plt.colorbar()
plt.xlabel("lon/$^\circ$E")
plt.ylabel("lat/$^\circ$N")
plt.title("value of PV at altitude = %i $m$" %  alt[altitudeIndex])


axes = plt.subplots(2, 2, sharex = True, sharey = True)
for i in range(2):
    for j in range(2):
        plt.subplot(2, 2, i+j*2+1)
        CS = plt.contour(lat[:], alt[:], pv[i+j, :, :, 100], [0, 2, 4])
        plt.clabel(CS, inline = 1, fontsize = 10)


# In[ ]:


print(alt[:])


# In[ ]:





# In[ ]:





# In[141]:


lenTime = len(time)
lenAlt = len(alt)
lenLon = len(lon)
lenLat = len(lat)

matrix = [[2 for i in range(lenLon)] for j in range(lenLat)]

numSlide = 0
indexOfLargeRange = [];
indices = []
length = 0;

#lowerBound = 0
#upperBound = 3

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
            
#             if lastTwoIndex.size != 0: ## ???It should not be 0 if the condition is fulfilled
#                 firstTwoIndex = np.matlib.repmat(firstTwoIndex, len(lastTwoIndex), 1)
#                 index = np.concatenate((firstTwoIndex, lastTwoIndex), axis=1)
# #                print(index)
# #                indices.append(index)
#                 if len(indices):
#                     indices = np.concatenate((indices, index), axis = 0)
#                 else:
#                     indices = index
#                 length = length + index.shape[0]

        indexOfAlt += 1
    indexOfTime += 1


# count = 0
# for s in range(lenTime):
#     for i in range(lenAlt):
#         for j in range(lenLat):
#             for k in range(lenLon):
#                 if (pv[s, i, j, k] > (2 - tolerrence)) and (pv[s, i, j, k] < (2 + tolerrence)):
#                     count += 1
# #             print(i, j, k, l, "\n") 
# print(count)
            

            
            
                

print("The number of  different slides: %d" %numSlide)
print("The number of index pairs is : %d" % length)
indices = np.array(indices)
indices = np.asarray(indices)
#indices = np.reshape(indices, (2, length))
print(indices.shape)


# In[94]:


numpy.set_printoptions(threshold = 300)
print(indices)


# In[142]:


def Connection(time, index):
    if len(time) == 0:
        time = index
    else:
        time = np.column_stack((time, index))
    return time

def Splite(indices, timeRange):
    time0 = []
    time1 = []
    time2 = []
    time3 = []
    time = [time0, time1, time2, time3]
    print("proceeding...\n")

#     for i in range(indices.shape[0]):
#         valueOfFirstIndex = indices[i, 0]
#         if valueOfFirstIndex == 0:
#             time0 = Connection(time0, indices[i, :])
#         elif valueOfFirstIndex == 1:
#             time1 = Connection(time1, indices[i, :])
#         elif valueOfFirstIndex == 2:
#             time2 = Connection(time2, indices[i, :])
#         else:
#             time3 = Connection(time3, indices[i, :])
        
#         if i == 0.3 * len(indices):
#             print("proceeded 30%!\n")
#         elif i == 0.6 * len(indices):
#             print("proceeded 60%!\n")
#         elif i == 0.9 * len(indices):
#             print("proceeded 90%!\n")
    for i in range(timeRange):
        print("i = ", i)
        location = np.where(indices[:, 0] == i)
        location = np.array(location)
        print(location.shape)
        time[i] = indices[location,:]
    
    return time


# In[154]:


time0 = []
time1 = []
time2 = []
time3 = []

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

indexOfTime = indices[:, 0]
indexOfAlti = indices[:, 1]
indexOfLati = indices[:, 2]
indexOfLong = indices[:, 3]

get_ipython().run_line_magic('matplotlib', 'qt')
fig = plt.subplot()
plt.subplots_adjust(right=0.9)
scatter = fig.scatter(lon[time0[:, 3]], lat[time0[:, 2]], c = alt[time0[:, 1]])
fig.set_xlabel("lon/$^\circ$E")
fig.set_ylabel("lat/$^\circ$N")
# plt.legend(*scatter.legend_elements(),bbox_to_anchor=(1.1, 0.5),loc = 'center right',title="alt/m", borderaxespad = 0.1)

fig = plt.subplots(2, 2, sharex = True, sharey = True)
plt.subplots_adjust(bottom = 0.2)
ax1 = plt.subplot(2,2,1)
scatter = ax1.scatter(lon[time0[:, 3]], lat[time0[:, 2]], c = alt[time0[:, 1]])
ax1.set_xlabel("lon/$^\circ$E")
ax1.set_ylabel("lat/$^\circ$N")
ax2 = plt.subplot(2,2,2)
ax2.scatter(lon[time1[:, 3]], lat[time1[:, 2]], c = alt[time1[:, 1]])
ax2.set_xlabel("lon/$^\circ$E")
ax2.set_ylabel("lat/$^\circ$N")
ax3 = plt.subplot(2, 2, 3)
ax3.scatter(lon[time2[:, 3]], lat[time2[:, 2]], c = alt[time2[:, 1]])
ax3.set_xlabel("lon/$^\circ$E")
ax3.set_ylabel("lat/$^\circ$N")
ax4 = plt.subplot(2, 2, 4)
ax4.scatter(lon[time3[:, 3]], lat[time3[:, 2]], c = alt[time3[:, 1]])
ax4.set_xlabel("lon/$^\circ$E")
ax4.set_ylabel("lat/$^\circ$N")
plt.legend(*scatter.legend_elements(),bbox_to_anchor=(0, -0.2),loc = 'upper center',title="alt/m", borderaxespad = 0.1,ncol = 10)
plt.show()


# In[ ]:





# In[78]:


index = indices[0, :]
# index = index.tolist()

print(index)
print(qv.shape)
print(type(qv))
print(qv[0,13,62,340])
print(qv[index[0],index[1], index[2], index[3]])


# In[79]:


mask = np.where(qv==0, True, False)
qv.mask = mask

print(qv)
print(qv.mask)


# In[80]:


sumOfQV = 0;
for i in range(len(indices)):
    index = indices[i, :]
    qvValue = qv[index[0], index[1], index[2], index[3]]
    sumOfQV += qvValue

averOfQV = sumOfQV / (len(indices) * 1.0)
print(averOfQV)
exceedRatio = 0.25
upperBound = averOfQV * (1 + exceedRatio)
lowerBound = averOfQV * (1 - exceedRatio)

print(upperBound)
print(lowerBound)


# In[81]:


indicesOfQV = []
indexOfTime = 0
lengthOfQVInRange = 0

tolerrence = exceedRatio * averOfQV
compareMatrix = averOfQV * np.ones((lenLat, lenLon))

for t in qv:
    print(t.shape)
    indexOfAlt = 0
    for altitude in t:
        firstTwoIndex = [indexOfTime, indexOfAlt]
        diff = np.abs(altitude - compareMatrix)
        if diff.min() <= tolerrence:
            lastTwoIndex = np.asarray(np.where((altitude >= lowerBound) & (altitude <= upperBound))).T
            lastTwoIndex = np.array(lastTwoIndex)
            firstTwoIndex = np.matlib.repmat(firstTwoIndex, len(lastTwoIndex), 1)
            index = np.concatenate((firstTwoIndex, lastTwoIndex), axis = 1)
            if len(indicesOfQV):
                indicesOfQV = np.concatenate((indicesOfQV, index), axis = 0)
            else:
                indicesOfQV = index
            lengthOfQVInRange = lengthOfQVInRange + index.shape[0]
        indexOfAlt += 1
    indexOfTime += 1
print("The number of the points: ", lengthOfQVInRange)
print(indicesOfQV.shape)


# In[82]:





# In[88]:


indicesOfLon = indicesOfQV[:, 3]
indicesOfLat = indicesOfQV[:, 2]
indicesOfAlt = indicesOfQV[:, 1]
indicesOfTime = indicesOfQV[:, 0]

[time0, time1, time2, time3] = Splite(indicesOfQV, 4)
time0 = time0[0,:,:]
time1 = time1[0,:,:]
time2 = time2[0,:,:]
time3 = time3[0,:,:]


# In[89]:


print(time0.shape)
print(time0)


# In[92]:


fig = plt.figure()
ax0 = fig.add_subplot(2, 2, 1, projection='3d')
ax0.scatter(lon[time0[:,3]], lat[time0[:, 2]], alt[time0[:, 1]])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(lon[time0[:,3]], lat[time0[:, 2]], alt[time0[:, 1]])


# In[ ]:




