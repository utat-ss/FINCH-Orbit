#UTAT - Orbital Subsystem

#Jai Willems with assistance from Nishkrit Desai and Mingde Yin, 1006342165
#University of Toronto Faculty of Applied Science and Engineering
#Division of Engineeing Science
#Completed 07-09-2020

#The purpose of this script is to create various visual representaions of the satellite encounter data.

#---------------------------------------------------------------------------------------------------------------------------------



import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt



schedule_file = 'Satellite Encounter Schedule.txt'



#----------------------------------------------------------------------------------------------------
#   Satellite Encounter Distribution                                                                -
#----------------------------------------------------------------------------------------------------



schedule = np.loadtxt(schedule_file, dtype=str, delimiter='\t', skiprows=0)

indicesLI = np.where(schedule[:, 0] == 'LIMB IMAGING WINDOW')
indicesDL = np.where(schedule[:, 0] == 'DATA LINK TRANSMISSION WINDOW')
indicesTTC = np.where(schedule[:, 0] == 'TTC TRANSMISSION WINDOW')
indicesNI = np.where(schedule[:, 0] == 'NADIR IMAGING WINDOW')

labels = 'Limb Imaging', 'Data Link', 'Tracking, Telimetry, & Control', 'Nadir Imaging'
sizes = [np.shape(indicesLI[0])[0], np.shape(indicesDL[0])[0], np.shape(indicesTTC[0])[0], np.shape(indicesNI[0])[0]]

fig1, ax = plt.subplots()

ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False)
ax.set_title('Satellite Encounter distribution')

fig1.set_size_inches(11, 8)
fig1.savefig('satEncounterDistribution')



#----------------------------------------------------------------------------------------------------
#   Satellite Time Distribution                                                                     -
#----------------------------------------------------------------------------------------------------



schedule = np.loadtxt(schedule_file, dtype=str, delimiter='\t', skiprows=0)

indicesLI = np.where(schedule[:, 0] == 'LIMB IMAGING WINDOW')[0]
indicesDL = np.where(schedule[:, 0] == 'DATA LINK TRANSMISSION WINDOW')[0]
indicesTTC = np.where(schedule[:, 0] == 'TTC TRANSMISSION WINDOW')[0]
indicesNI = np.where(schedule[:, 0] == 'NADIR IMAGING WINDOW')[0]

startDateTime = datetime.strptime(schedule[0][1], '%Y-%m-%d %H:%M:%S.%f')
endDateTime = datetime.strptime(schedule[np.shape(schedule)[0] - 1][1], '%Y-%m-%d %H:%M:%S.%f')
timeLI = np.sum(schedule[indicesLI, 2].astype(float))
timeDL = np.sum(schedule[indicesDL, 2].astype(float))
timeTTC = np.sum(schedule[indicesTTC, 2].astype(float))
timeNI = np.sum(schedule[indicesNI, 2].astype(float))
downTime = ((endDateTime - startDateTime) - timedelta(seconds=np.sum(schedule[:, 2].astype(float))))#.seconds

labels = 'Limb Imaging', 'Data Link', 'Tracking, Telimetry, & Control', 'Nadir Imaging', 'Down Time'
sizes = [timeLI, timeDL, timeTTC, timeNI, downTime.seconds]

fig2, ax = plt.subplots()

ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False)
ax.set_title('Satellite Time distribution')

fig2.set_size_inches(11, 8)
fig2.savefig('satTimeDistribution')



#----------------------------------------------------------------------------------------------------
#   Geomap of Imaging Frequency by Location                                                         -
#----------------------------------------------------------------------------------------------------

#geomap of imaging areas (color gradient based on how many times it could be imaged)

#calendar of passes