#UTAT - Orbital Subsystem

#Jai Willems with assistance from Nishkrit Desai and Mingde Yin, 1006342165
#University of Toronto Faculty of Applied Science and Engineering
#Division of Engineeing Science
#Completed 07-09-2020

#The purpose of this script is to convert GMAT Orbital data into various representaions.

#---------------------------------------------------------------------------------------------------------------------------------



from orbital_data_converter_dependencies_V3 import findSatPositionData
import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter
from queue import PriorityQueue, Queue
from datetime import datetime, timedelta



dataFile = 'data.txt'                       #file with satellite position data
satellite_height = 400                      #height viewing map is taken at
observer_coor = (43.662300, -79.394530)     #coordinates of observation station
imaging_coor = (30, -100)                   #ground coordinates to image
surface_radius = 6371                       #distance from the earths core to observer
maxLines = 10000                            #number of dataFile lines to investigate



min_LI_time = 30    #min time required to complete a limb imaging encounter
min_TTC_time = 30   #min time required to complete a ttc encounter
min_DL_time = 30    #min time required to complete a data link encounter
min_NI_time = 30    #min time required to complete a nadir imaging encounter



orientationChangeTime = 5   #time required to change the satellites orientation



startTime = perf_counter()



#----------------------------------------------------------------------------------------------------
#   Convert Latitude/Longitude to Orbital Position Data                                             -
#----------------------------------------------------------------------------------------------------



data = np.loadtxt(dataFile, dtype='str', delimiter='\t', max_rows=maxLines)

satCoor = (np.copy(data[1:, 3]).astype(float), np.copy(data[1:, 4]).astype(float))
satHeight = np.copy(data[1:, 2].astype(float))
positionData = findSatPositionData(satCoor, satHeight, imaging_coor, observer_coor, surface_radius)
positionData = positionData.astype('U30')
positionData = np.append([['FINCHSat.Earth.altitude.angle', 'FINCHSat.Earth.azimuth', 'FINCHSat.imaging.altitude.angle', 'FINCHSat.imaging.Nadir/LOS.Angle']], positionData, axis=0)

data = np.append(data, positionData, axis=1)

fOut = '(horizontal)' + dataFile
np.savetxt(fOut, data, fmt='%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s') 



#----------------------------------------------------------------------------------------------------
#   Create Viewing Map                                                                              -
#----------------------------------------------------------------------------------------------------



x, y = np.meshgrid(np.array(np.linspace(-90, 90, 181)), np.array(np.linspace(-180, 180, 361)))
latitudeArray = np.reshape(x, -1)
longitudeArray = np.reshape(y, -1)
satelliteHeights = np.full((65341, ), satellite_height)

positionData = findSatPositionData((latitudeArray, longitudeArray), satelliteHeights, imaging_coor, observer_coor, surface_radius)

LIIndices = np.where((1 >= positionData[:, 0]) &(positionData[:, 0] > 0)) if (imaging_coor == observer_coor) else np.where((1 >= positionData[:, 2]) &(positionData[:, 2] > 0))
TTCIndices = np.where(positionData[:, 0] > 10)
DLIndices = np.where(positionData[:, 0] > 30)
NIIndices = np.where((30 >= positionData[:, 3]) & (positionData[:, 3] >= 0))

LIx, LIy = longitudeArray[LIIndices], latitudeArray[LIIndices]
TTCx, TTCy = longitudeArray[TTCIndices], latitudeArray[TTCIndices]
DLx, DLy = longitudeArray[DLIndices], latitudeArray[DLIndices]
NIx, NIy = longitudeArray[NIIndices], latitudeArray[NIIndices]

plt.scatter(TTCx, TTCy, c='silver', marker=',', label='TTC')
plt.scatter(DLx, DLy, c='grey', marker=',', label='Data Link')
plt.scatter(NIx, NIy, c='black', marker=',', label='Nadir Imaging')
plt.scatter(LIx, LIy, c='slategrey', marker=',', label='Limb Imaging')

plt.title('Viewing Map')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend(loc='upper right')

plt.savefig('vewingMap')



#----------------------------------------------------------------------------------------------------
#   Generate Viewing Windows                                                                        -
#----------------------------------------------------------------------------------------------------



LIPass = []
TTCPass = []
DLPass = []
NIPass = []

outDataQueue = PriorityQueue()
data = np.loadtxt(dataFile, dtype='str', delimiter='\t', max_rows=maxLines)

satCoor = (np.copy(data[1:, 3]).astype(float), np.copy(data[1:, 4]).astype(float))
satHeight = np.copy(data[1:, 2].astype(float))
positionData = findSatPositionData(satCoor, satHeight, imaging_coor, observer_coor, surface_radius)

for index in range(0, maxLines - 1):
    data[index + 1][0] = datetime.strptime(data[index + 1][0], '%d %b %Y %H:%M:%S.%f')

    observerAltitude = positionData[index, 0]
    imagingAltitude = positionData[index, 2]
    nadirLOSAngle = positionData[index, 3]

    if 1 >= imagingAltitude >= 0 and len(LIPass) == 0:
        LIPass.extend([data[index][0], data[index][1]])
    if (imagingAltitude > 1 or 0 > imagingAltitude) and len(LIPass) > 0:
        elapsedTime = float(data[index][1]) - float(LIPass[1])
        if elapsedTime > min_LI_time:
            window = 'LIMB IMAGING WINDOW\t%s\tELAPSED SECONDS:\t%s' %(LIPass[0], str(elapsedTime))
            outDataQueue.put((float(LIPass[1]), window))
        LIPass = []

    if observerAltitude >= 20 and len(TTCPass) == 0:
        TTCPass.extend([data[index][0], data[index][1]])
    if 20 > observerAltitude and len(TTCPass) > 0:
        elapsedTime = float(data[index][1]) - float(TTCPass[1])
        if elapsedTime > min_TTC_time:
            window = 'TTC TRANSMISSION WINDOW\t%s\tELAPSED SECONDS:\t%s' %(TTCPass[0], str(elapsedTime))
            outDataQueue.put((float(TTCPass[1]), window))
        TTCPass = []

    if observerAltitude >= 30 and len(DLPass) == 0:
        DLPass.extend([data[index][0], data[index][1]])
    if 30 > observerAltitude and len(DLPass) > 0:
        elapsedTime = float(data[index][1]) - float(DLPass[1])
        if elapsedTime > min_DL_time:
            window = 'DATA LINK TRANSMISSION WINDOW\t%s\tELAPSED SECONDS:\t%s' %(DLPass[0], str(elapsedTime))
            outDataQueue.put((float(DLPass[1]), window))
        DLPass = []

    if 30 >= nadirLOSAngle >= 0 and len(NIPass) == 0:
        NIPass.extend([data[index][0], data[index][1]])
    if (nadirLOSAngle > 30 or 0 > nadirLOSAngle) and len(NIPass) > 0:
        elapsedTime = float(data[index][1]) - float(NIPass[1])
        if elapsedTime > min_NI_time:
            window = 'NADIR IMAGING WINDOW\t%s\tELAPSED SECONDS:\t%s' %(NIPass[0], str(elapsedTime))
            outDataQueue.put((float(NIPass[1]), window))
        NIPass = []

outData = np.array([])
while not outDataQueue.empty():
    outData = np.append(outData, outDataQueue.get()[1])

np.savetxt('Satellite Encounter Windows.txt', outData, fmt='%s', header='Satellite Encounter Windows')



#----------------------------------------------------------------------------------------------------
#   Generate Encounter Schedule                                                                     -
#----------------------------------------------------------------------------------------------------



windows = np.loadtxt('Satellite Encounter windows.txt', dtype=str, delimiter='\t', skiprows=0)

scheduleData = np.array([])
scheduleQueue = Queue()
windowQueue = Queue()

for i in range(np.shape(windows)[0]):
    windowQueue.put((windows[i][0], windows[i][1], windows[i][3]))
timeLI, timeTTC, timeDL, timeNI = perf_counter(), perf_counter(), perf_counter(), perf_counter()

def getStartTime(passIdentifier, timeLI, timeTTC, timeDL, timeNI):
    if passIdentifier == 'LIMB IMAGING WINDOW':
        return timeLI
    elif passIdentifier == 'TTC TRANSMISSION WINDOW':
        return timeTTC
    elif passIdentifier == 'DATA LINK TRANSMISSION WINDOW':
        return timeDL
    else:
        return timeNI

def newStartTime(passIdentifier, timeLI, timeTTC, timeDL, timeNI):
    if passIdentifier == 'LIMB IMAGING WINDOW':
        timeLI = perf_counter()
    elif passIdentifier == 'TTC TRANSMISSION WINDOW':
        timeTTC = perf_counter()
    elif passIdentifier == 'DATA LINK TRANSMISSION WINDOW':
        timeDL = perf_counter()
    else:
        timeNI = perf_counter()
    return timeLI, timeTTC, timeDL, timeNI

item1 = windowQueue.get()
while not windowQueue.empty():
    time1 = datetime.strptime(item1[1], '%Y-%m-%d %H:%M:%S.%f')
    item2 = windowQueue.get()
    time2 = datetime.strptime(item2[1], '%Y-%m-%d %H:%M:%S.%f')
    timeDifference = time2 - time1

    startTime1 = round(getStartTime(item1[0], timeLI, timeTTC, timeDL, timeNI), 4)
    startTime2 = round(getStartTime(item2[0], timeLI, timeTTC, timeDL, timeNI), 4)
    
    if timeDifference.seconds - orientationChangeTime > float(item1[2]):
        window = np.array(['%s\t%s\t%s' %(item1[0], item1[1], item1[2])])
        scheduleData = np.append(scheduleData, window, axis=0)
        timeLI, timeTTC, timeDL, timeNI = newStartTime(item1[0], timeLI, timeTTC, timeDL, timeNI)
        item1 = item2
    elif startTime1 < startTime2:
        window = np.array(['%s\t%s\t%s' %(item1[0], item1[1], item1[2])])
        scheduleData = np.append(scheduleData, window, axis=0)
        timeLI, timeTTC, timeDL, timeNI = newStartTime(item1[0], timeLI, timeTTC, timeDL, timeNI)
        item1 = windowQueue.get()
    else:
        item1 = item2

window = np.array(['%s\t%s\t%s' %(item1[0], item1[1], item1[2])])
scheduleData = np.append(scheduleData, window, axis=0)

np.savetxt('Satellite Encounter Schedule.txt', scheduleData, fmt='%s', header='Satellite Encounter Schedule')



endTime = perf_counter()
print('Elapsed Time: ', endTime - startTime)