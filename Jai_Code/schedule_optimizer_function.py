#UTAT - Orbital Subsystem

#Jai Willems with assistance from Nishkrit Desai, 1006342165
#University of Toronto Faculty of Applied Science and Engineering
#Division of Engineeing Science
#Completed 07-09-2020

#The purpose of this script is to create an optimized encounter schedule for the FINCH satellite.

#---------------------------------------------------------------------------------------------------------------------------------



from orbital_data_converter_dependencies_V3 import findSatPositionData
import numpy as np
from time import perf_counter
from queue import PriorityQueue, Queue
from datetime import datetime, timedelta



windowDataFile = 'Satellite Encounter Windows.txt'  #file with satellite position data
orientationChangeTime = 5   #time required to change the satellites orientation



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
        window = np.array(['%s\t--\t%s\t--\tELAPSED SECONDS: %s' %(item1[0], item1[1], item1[2])])
        scheduleData = np.append(scheduleData, window, axis=0)
        timeLI, timeTTC, timeDL, timeNI = newStartTime(item1[0], timeLI, timeTTC, timeDL, timeNI)
        item1 = item2
    elif startTime1 < startTime2:
        window = np.array(['%s\t--\t%s\t--\tELAPSED SECONDS: %s' %(item1[0], item1[1], item1[2])])
        scheduleData = np.append(scheduleData, window, axis=0)
        timeLI, timeTTC, timeDL, timeNI = newStartTime(item1[0], timeLI, timeTTC, timeDL, timeNI)
        item1 = windowQueue.get()
    else:
        item1 = item2

window = np.array(['%s\t--\t%s\t--\tELAPSED SECONDS: %s' %(item1[0], item1[1], item1[2])])
scheduleData = np.append(scheduleData, window, axis=0)

np.savetxt('Satellite Encounter Schedule.txt', scheduleData, fmt='%s', header='Satellite Encounter Schedule')