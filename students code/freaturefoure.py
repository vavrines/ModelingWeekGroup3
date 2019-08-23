import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from netCDF4 import Dataset



dataset = Dataset(r"F:\\MathSEE\ModelingWeekGroup3\dataset\2016021600-ART-chemtracer_grid_reg_DOM02_HL_0007.nc")
#change data path here
time = dataset.variables['time']
lon = dataset.variables['lon']
lat = dataset.variables['lat']
alt = dataset.variables['alt']
time = dataset.variables['time']
pv = dataset.variables['pv']
qv = dataset.variables['qv']
np.ma.is_masked(qv[:])
np.ma.is_masked(pv[:])
#mask = np.where(pv ==0,True,False)
#pv.mask = mask
#mask = np.where(qv ==0,True,False)
#qv.mask = mask


# print(lon.shape);
# print(lat.shape);
# print(alt.shape);
# print(time.shape);
# print(pv.shape);
# print(qv.shape)

pv = (10 ** 6) * pv[:]
# print(pv.shape)
# plt.figure()
# plt.pcolormesh(lon[:], alt[:], pv[3, :, 100, :])
# plt.colorbar()
#
# axes = plt.subplots(2, 2, sharex=True, sharey=True)
# for i in range(2):
#     for j in range(2):
#         plt.subplot(2, 2, i + j * 2 + 1)
#         CS = plt.contour(lat[:], alt[:], pv[i + j, :, :, 100], [0, 2, 4])
#         plt.clabel(CS, inline=1, fontsize=10)

lenTime = len(time)
lenAlt = len(alt)
lenLon = len(lon)
lenLat = len(lat)

matrix = [[2 for i in range(lenLon)] for j in range(lenLat)]

numSlide = 0
indexOfLargeRange = [];
# indices = []
length = 0;

# lowerBound = 0
# upperBound = 3


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
tolerrence = 1e-3

for t in pv:
    print(t.shape)
    indexOfAlt = 0;
    for altitude in t:
        diff = np.abs(altitude - matrix)
        if diff.min() < tolerrence:
            numSlide += 1
            firstTwoIndex = [indexOfTime, indexOfAlt]
            lastTwoIndex = np.asarray(np.where((altitude > 2 - tolerrence) & (altitude < 2 + tolerrence))).T
            lastTwoIndex = np.array(lastTwoIndex)
            if lastTwoIndex.size != 0:  ## ???It should not be 0 if the condition is fulfilled
                firstTwoIndex = np.matlib.repmat(firstTwoIndex, len(lastTwoIndex), 1)
                index = np.concatenate((firstTwoIndex, lastTwoIndex), axis=1)
                #                print(index)
                #                indices.append(index)
                if len(indices):
                    indices = np.concatenate((indices, index), axis=0)
                else:
                    indices = index
                length = length + index.shape[0]
        indexOfAlt += 1
    indexOfTime += 1


print("The number of value of different slides: %d" % numSlide)
print("The number of index pairs is : %d" % length)
indices = np.array(indices)
indices = np.asarray(indices)
print(indices.shape)
qv_temp = []
for e in indices:
    # print(qv[i[0],i[1],i[2],i[3]])
    qv_temp.append(qv[e[0],e[1],e[2],e[3]])


qv_temp = np.array(qv_temp)
mask = np.where(qv_temp ==0,True,False)
qv_temp.mask = mask

print(qv_temp.shape)
qv_mean = np.mean(qv_temp)

print(qv_mean)

numSlide1 = 0
indexOfLargeRange1 = [];
indices1 = []
length1 = 0;

indexOfTime1 = 0;
tolerrence1 = qv_mean*0.25
matrix1 = [[qv_mean for i in range(lenLon)] for j in range(lenLat)]
for t1 in qv:
    # print(t.shape)
    indexOfAlt1 = 0;
    for altitude1 in t1:
        diff = np.abs(altitude1 - matrix1)
        if diff.min() < tolerrence1:
            numSlide1 += 1
            firstTwoIndex = [indexOfTime1, indexOfAlt1]
            lastTwoIndex = np.asarray(np.where((altitude1 > qv_mean - tolerrence1) & (altitude1 < qv_mean + tolerrence1))).T
            lastTwoIndex = np.array(lastTwoIndex)
            if lastTwoIndex.size != 0:  ## ???It should not be 0 if the condition is fulfilled
                firstTwoIndex = np.matlib.repmat(firstTwoIndex, len(lastTwoIndex), 1)
                index = np.concatenate((firstTwoIndex, lastTwoIndex), axis=1)
                #                print(index)
                #                indices.append(index)
                if len(indices1):
                    indices1 = np.concatenate((indices1, index), axis=0)
                else:
                    indices1 = index
                length1 = length1 + index.shape[0]
        indexOfAlt1 += 1
    indexOfTime1 += 1


print("The number of value of different slides: %d" % numSlide1)
print("The number of index pairs is : %d" % length1)
indices1 = np.array(indices1)
indices1 = np.asarray(indices1)
indices1 = indices1[:][1:length1:100]
print(indices1.shape)
qv_temp0 = []
qv_temp1 = []
qv_temp2 = []
qv_temp3 = []

for m in indices1:
    if m[0] == 0:
    # print(qv[i[0],i[1],i[2],i[3]])
        qv_temp0.append(qv[m[0],m[1],m[2],m[3]])
    if m[0] == 1:
    # print(qv[i[0],i[1],i[2],i[3]])
        qv_temp1.append(qv[m[0],m[1],m[2],m[3]])
    if m[0] == 2:
    # print(qv[i[0],i[1],i[2],i[3]])
        qv_temp2.append(qv[m[0],m[1],m[2],m[3]])
    if m[0] == 3:
    # print(qv[i[0],i[1],i[2],i[3]])
        qv_temp3.append(qv[m[0],m[1],m[2],m[3]])

qv_temp0 = np.array(qv_temp0)
qv_temp1 = np.array(qv_temp1)
qv_temp2 = np.array(qv_temp2)
qv_temp3 = np.array(qv_temp3)

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

for k in range(indices1.shape[0]):
    valueOfFirstIndex = indices1[k, 0]
    if valueOfFirstIndex == 0:
        time0 = Connection(time0, indices1[k, :])
    elif valueOfFirstIndex == 1:
        time1 = Connection(time1, indices1[k, :])
    elif valueOfFirstIndex == 2:
        time2 = Connection(time2, indices1[k, :])
    else:
        time3 = Connection(time3, indices1[k, :])


time0 = time0.T
time1 = time1.T
time2 = time2.T
time3 = time3.T

# get_ipython().run_line_magic('matplotlib', 'qt')
fig = plt.subplots(2, 2, sharex = True, sharey = True)
plt.subplots_adjust(right = 0.7)
ax1 = plt.subplot(2,2,1)
scatter = ax1.scatter(lon[time0[:, 3]], lat[time0[:, 2]],s=5, c = qv_temp0)
ax2 = plt.subplot(2,2,2)
ax2.scatter(lon[time1[:, 3]], lat[time1[:, 2]],s=5, c = qv_temp1)
ax3 = plt.subplot(2, 2, 3)
ax3.scatter(lon[time2[:, 3]], lat[time2[:, 2]],s=5, c = qv_temp2)
ax4 = plt.subplot(2, 2, 4)
ax4.scatter(lon[time3[:, 3]], lat[time3[:, 2]],s=5, c = qv_temp3)
plt.legend(*scatter.legend_elements(),bbox_to_anchor=(1.7, 1),loc = 'center right', borderaxespad = 0.1)
# plt.show()


fig1 = plt.subplots(2, 2, sharex = True, sharey = True)
plt.subplots_adjust(right = 0.7)
ax5 = plt.subplot(2,2,1)
plt.tricontour(lon[time0[:, 3]], lat[time0[:, 2]], qv_temp0, 15, linewidths=0.01, colors='k')
plt.tricontourf(lon[time0[:, 3]], lat[time0[:, 2]], qv_temp0, 15)
ax6 = plt.subplot(2,2,2)
plt.tricontour(lon[time1[:, 3]], lat[time1[:, 2]], qv_temp1, 15, linewidths=0.01, colors='k')
plt.tricontourf(lon[time1[:, 3]], lat[time1[:, 2]], qv_temp1, 15)
ax7 = plt.subplot(2, 2, 3)
plt.tricontour(lon[time2[:, 3]], lat[time2[:, 2]], qv_temp2, 15, linewidths=0.01, colors='k')
plt.tricontourf(lon[time2[:, 3]], lat[time2[:, 2]], qv_temp2, 15)
ax8 = plt.subplot(2, 2, 4)
plt.tricontour(lon[time3[:, 3]], lat[time3[:, 2]], qv_temp3, 15, linewidths=0.01, colors='k')
plt.tricontourf(lon[time3[:, 3]], lat[time3[:, 2]], qv_temp3, 15)
plt.show()









dataset.close()