#UTAT - Orbital Subsystem

#Jai Willems, 1006342165
#University of Toronto Faculty of Applied Science and Engineering
#Division of Engineeing Science
#Completed 18-08-2020

#The purpose of this script is to convert GMAT data into various representaions.

#---------------------------------------------------------------------------------------------------------------------------------



from FINCH_orbital_data_converter_dependencies_NUMPY_V2 import findHorizontalAndSatelliteNadirToLOSAngleNUMPY
import numpy as np
import matplotlib.pyplot as plt
from time import perf_counter



dataFile = 'data.txt'
satellite_height = 400
observer_coor = (43.662300, -79.394530)
surface_radius = 6371
maxLines = 10000



startTime = perf_counter()



#----------------------------------------------------------------------------------------------------
#   Convert Latitude/Longitude to Orbital Position Data                                             -
#----------------------------------------------------------------------------------------------------



data = np.loadtxt(dataFile, dtype='str', delimiter='\t', max_rows=maxLines)

satCoor = (np.copy(data[1:, 3]).astype(float), np.copy(data[1:, 4]).astype(float))
satHeight = np.copy(data[1:, 2].astype(float))
positionData = findHorizontalAndSatelliteNadirToLOSAngleNUMPY(satCoor, satHeight, observer_coor, surface_radius)
positionData = positionData.astype('U30')
positionData = np.append([['FINCHSat.Earth.altitude.angle', 'FINCHSat.Earth.azimuth', 'FINCHSat.Sat.Nadir/LOS.Angle']], positionData, axis=0)

data = np.append(data, positionData, axis=1)

fOut = '(horizontal)' + dataFile
np.savetxt(fOut, data, fmt='%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s') 




#----------------------------------------------------------------------------------------------------
#   Create Viewing Map                                                                              -
#----------------------------------------------------------------------------------------------------



x, y = np.meshgrid(np.array(np.linspace(-90, 90, 181)), np.array(np.linspace(-180, 180, 361)))
latitudeArray = np.reshape(x, -1)
longitudeArray = np.reshape(y, -1)
satelliteHeights = np.full((65341, ), satellite_height)

positionData = findHorizontalAndSatelliteNadirToLOSAngleNUMPY((latitudeArray, longitudeArray), satelliteHeights, observer_coor, surface_radius)

LIIndices = np.where((1 >= positionData[:, 0]) &(positionData[:, 0] > 0))
TTCIndices = np.where((30 >= positionData[:, 0]) & (positionData[:, 0]> 10))
DLIndices = np.where((positionData[:, 0] > 30) & (positionData[:, 2] > 30))
NIIndices = np.where((30 >= positionData[:, 2]) & (positionData[:, 2] >= 0))

LIx, LIy = longitudeArray[LIIndices], latitudeArray[LIIndices]
TTCx, TTCy = longitudeArray[TTCIndices], latitudeArray[TTCIndices]
DLx, DLy = longitudeArray[DLIndices], latitudeArray[DLIndices]
NIx, NIy = longitudeArray[NIIndices], latitudeArray[NIIndices]

plt.scatter(LIx, LIy, c='slategrey', marker=',', label='Limb Imaging')
plt.scatter(TTCx, TTCy, c='silver', marker=',', label='TTC')
plt.scatter(DLx, DLy, c='grey', marker=',', label='Data Link')
plt.scatter(NIx, NIy, c='black', marker=',', label='Nadir Imaging')

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

positionData = findHorizontalAndSatelliteNadirToLOSAngleNUMPY((data[1:, 3].astype(float), data[1:, 4].astype(float)), data[1:, 2].astype(float), observer_coor, surface_radius)

for index in range(0, maxLines - 1):

    altitude = positionData[index, 0]
    nadirLOSAngle = positionData[index, 2]

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