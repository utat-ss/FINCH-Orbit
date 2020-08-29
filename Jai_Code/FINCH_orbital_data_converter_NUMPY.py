#UTAT - Orbital Subsystem

#Jai Willems, 1006342165
#University of Toronto Faculty of Applied Science and Engineering
#Division of Engineeing Science
#Completed 18-08-2020

#The purpose of this script is to convert GMAT data into various representaions.

#---------------------------------------------------------------------------------------------------------------------------------



from FINCH_orbital_data_converter_dependencies_NUMPY import findHorizontalAndSatelliteNadirToLOSAngle
import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter



dataFile = 'data.txt'
satellite_height = 400 # km
observer_coor = (43.662300, -79.394530)
surface_radius = 6371
maxLines = 100



startTime = perf_counter()


# HEADERS
# FINCHSat.ElapsedSecs	FINCHSat.Earth.Altitude	FINCHSat.Earth.Latitude	FINCHSat.Earth.Longitude	FINCHSat.EarthMJ2000Eq.RA	FINCHSat.EarthMJ2000Eq.DEC	FINCHSat.EarthMJ2000Eq.X	FINCHSat.EarthMJ2000Eq.Y	FINCHSat.EarthMJ2000Eq.Z	FINCHSat.Earth.SMA	FINCHSat.Earth.MA	FINCHSat.Earth.EA	FINCHSat.Earth.TA	FINCHSat.EarthMJ2000Eq.AOP	FINCHSat.EarthMJ2000Eq.RAAN	FINCHSat.EarthMJ2000Eq.INC	FINCHSat.Earth.ECC
# 0                     1                       2                       3                           4                           5                           6                           7                           8                           9                   10                  11                  12                  13                          14                          15                          16          

#----------------------------------------------------------------------------------------------------
#   Convert Latitude/Longitude to Orbital Position Data                                             -
#----------------------------------------------------------------------------------------------------


data = np.loadtxt(dataFile, dtype=float, delimiter='\t', skiprows=1, usecols=np.arange(1, 18), max_rows=maxLines)

positionData = np.array([['FINCHSat.Earth.altitude.angle', 'FINCHSat.Earth.azimuth', 'FINCHSat.Sat.Nadir/LOS.Angle']])
for index in range(1, maxLines):
    positionTuple = findHorizontalAndSatelliteNadirToLOSAngle((data[index][2], data[index][3]), data[index][1], observer_coor, surface_radius)
    tempPositionData = np.array([positionTuple])
    positionData = np.append(positionData, tempPositionData.astype(str), axis=0)
data = np.append(data, positionData, axis=1)

fOut = '(horizontal)' + dataFile
np.savetxt(fOut, data, fmt='%s' + '\t%s'*(data.shape[1]-1)) 




#----------------------------------------------------------------------------------------------------
#   Create Viewing Map                                                                              -
#----------------------------------------------------------------------------------------------------



LIx, LIy = np.array([]), np.array([])
TTCx, TTCy = np.array([]), np.array([])
DLx, DLy = np.array([]), np.array([])
NIx, NIy = np.array([]), np.array([])

for latitude in range(90, -90, -1):
    for longitude in range(-180, 180):

        positionTuple = findHorizontalAndSatelliteNadirToLOSAngle((latitude, longitude), satellite_height, observer_coor, surface_radius)
        altitude = positionTuple[0]
        nadirLOSAngle = positionTuple[2]
        if 1 >= altitude > 0:
            LIx, LIy = np.append(LIx, longitude), np.append(LIy, latitude)
        elif 30 >= altitude > 10:
            TTCx, TTCy = np.append(TTCx, longitude), np.append(TTCy, latitude)
        elif altitude > 30 and nadirLOSAngle > 30:
            DLx, DLy = np.append(DLx, longitude), np.append(DLy, latitude)
        elif 30 >= nadirLOSAngle >= 0:
            NIx, NIy = np.append(NIx, longitude), np.append(NIy, latitude)

plot1 = plt.scatter(LIx, LIy, c='slategrey', marker=',', label='Limb Imaging')
plot2 = plt.scatter(TTCx, TTCy, c='silver', marker=',', label='TTC')
plot3 = plt.scatter(DLx, DLy, c='grey', marker=',', label='Data Link')
plot4 = plt.scatter(NIx, NIy, c='black', marker=',', label='Nadir Imaging')

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

outData = np.array([])

data = np.loadtxt(dataFile, dtype='str', delimiter='\t', max_rows=maxLines)

for index in range(1, maxLines):

    satLat = float(data[index][3])
    satLong = float(data[index][4])
    satAlt = float(data[index][2])
    positionTuple = findHorizontalAndSatelliteNadirToLOSAngle((satLat, satLong), satAlt, observer_coor, surface_radius)
    altitude = positionTuple[0]
    nadirLOSAngle = positionTuple[2]

    if 1 >= altitude >= 0 and len(LIPass) == 0:
        LIPass.extend([data[index][0], data[index][1]])
    if (altitude > 1 or 0 > altitude) and len(LIPass) > 0:
        window = np.array(['LIMB IMAGING WINDOW\t\t--\t%s\t--\tELAPSED SECONDS: %s' %(LIPass[0], str(float(data[index][1]) - float(LIPass[1])))])
        outData = np.append(outData, window, axis=0)
        LIPass = []

    if altitude >= 20 and len(TTCPass) == 0:
        TTCPass.extend([data[index][0], data[index][1]])
    if 20 > altitude and len(TTCPass) > 0:
        window = np.array(['TTC TRANSMISSION WINDOW\t\t--\t%s\t--\tELAPSED SECONDS: %s' %(TTCPass[0], str(float(data[index][1]) - float(TTCPass[1])))])
        outData = np.append(outData, window, axis=0)
        TTCPass = []

    if altitude >= 30 and len(DLPass) == 0:
        DLPass.extend([data[index][0], data[index][1]])
    if 30 > altitude and len(DLPass) > 0:
        window = np.array(['DATA LINK TRANSMISSION WINDOW\t--\t%s\t--\tELAPSED SECONDS: %s' %(DLPass[0], str(float(data[index][1]) - float(DLPass[1])))])
        outData = np.append(outData, window, axis=0)
        DLPass = []

    if 30 >= nadirLOSAngle >= 0 and len(NIPass) == 0:
        NIPass.extend([data[index][0], data[index][1]])
    if (nadirLOSAngle > 30 or 0 > nadirLOSAngle) and len(NIPass) > 0:
        window = np.array(['NADIR IMAGING WINDOW\t\t--\t%s\t--\tELAPSED SECONDS: %s' %(NIPass[0], str(float(data[index][1]) - float(NIPass[1])))])
        outData = np.append(outData, window, axis=0)
        NIPass = []

np.savetxt('Satellite Encounter Windows.txt', outData, fmt='%s', header='Satellite Encounter Windows')



endTime = perf_counter()
print('Elapsed Time: ', endTime - startTime)