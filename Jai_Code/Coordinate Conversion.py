#UTAT - Orbital Subsystem

#Jai Willems with assistance from Pascal Saint-Hilaire, 1006342165
#University of Toronto Faculty of Applied Science and Engineering
#Division of Engineeing Science
#Completed 07-09-2020

#The purpose of this script is to convert ECI Coordinates to ECEF geographical coordinates.

#---------------------------------------------------------------------------------------------------------------------------------



import numpy as np
from math import pi, cos, sin
from datetime import datetime
from orbital_data_converter_dependencies_V3.py import getAngle



dataFile = 'data.txt'
surface_radius = 6371
maxLines = 1000



#----------------------------------------------------------------------------------------------------
#   getGMST                                                                                         -
#----------------------------------------------------------------------------------------------------



def getGMST(timeData):
    """
    (np.array, np.array) -> np.array

    This function takes a Gregorian date array and returns the Greenwich Mean Sidereal Time.
    """
    utcTime = np.zeros((np.shape(timeData)[1], 5))
    utcTime[:, 0] = timeData[:].month#    timeData[0:2].astype(float)
    utcTime[:, 1] = timeDate[:].day#    timeData[2:4].astype(float)
    utcTime[:, 2] = timeDate[:].year#    timeData[4:6].astype(float) + 2000
    utcTime[:, 3] = timeDate[:].hour + timeDate[:].minutes / 60#    timeData[7:9].astype(float) + timeData[9:11].astype(float) / 60   #Fractional Hours
    
    termOne = 367 * utcTime[:, 2]
    termTwo = ((7 * ((utcTime[:, 0] + 9) / 12).astype(int)) / 4).astype(int)
    termThree = ((275 * utcTime[:, 0]) / 9).astype(int)
    termSix =utcTime[:, 3] / 24
    timeJD = np.add(np.add(np.add(np.add(np.subtract(termOne, termTwo), termThree), utcTime[:, 1]), 1721013.5), termSix)

    GMST = (18.697374558 + 24.06570982441908 * (timeJD - 2451545)) % 24

    return GMST



#----------------------------------------------------------------------------------------------------
#   getLST                                                                                          -
#----------------------------------------------------------------------------------------------------



def getLST(longitude, timeData): #UTC input as "MMDDYY HHMM"
    """
    (np.array, np.array) -> np.array

    This function takes in a point longitude and gregorian date and returns the Local Sidereal Time.
    """
    longitude = longitude.astype(float)
    positionData = np.zeros((np.shape(longitude)[1], 3))

    positionData[:, 0] = longitude.astype(int)
    positionData[:, 1] = np.subtract(longitude - positionData[:, 0]) * 60
    positionData[:, 2] = np.subtract(positionData[:, 1] - positionData[:, 1].astype(int)) * 60
    positionData[:, 1] = positionData.astype(int)
    positionData[:, 2] = positionData.astype(int)

    GMST = getGMST(timeData)

    longitude = longitude / 15
    LST = GMST + longitude
    negativeIndices = np.where(LST < 0)[0]
    LST[negativeIndices] += 24

    return LST



#----------------------------------------------------------------------------------------------------
#   Geographical2ECI                                                                                -
#----------------------------------------------------------------------------------------------------



def Geographical2ECI(dataFile):
    """
    (file) -> tuple

    This function takes a data file of satellite position in geographical coordinates and returns the ECI coordinates.
    This function was heavily influenced by the following code https://idlastro.gsfc.nasa.gov/ftp/pro/astro/geo2eci.pro
    """
    data = np.loadtxt(dataFile, dtype='str', delimiter='\t', max_rows=maxLines, skiprows=0).astype(float)

    latitude = np.radians(data[:, 3])
    longitude = np.radians(data[:, 4])
    altitude = np.radians(data[:, 2])

    for i in range(maxLines - 1):
        data[i][0] = datetime.strptime(data[i][0], '%d %b %Y %H:%M:%S.%f')
    utcTime = data[:, 0]

    siderealAngles = np.radians(timeConverter(data[:, 4], utcTime) * 15)
        
    theta = np.add(longitude, siderealAngles)
    r = np.multiply(altitude + surface_radius, np.cos(latitude))
    x = np.multiply(r, np.cos(theta))
    y = np.multiply(r, np.sin(theta))
    z = np.multiply(altitude + surface_radius, np.sin(latitude))

    return (x, y, z)



#----------------------------------------------------------------------------------------------------
#   ECI2Geographical                                                                                -
#----------------------------------------------------------------------------------------------------



def ECI2Geographical(dataFile):
    """
    (file) -> np.array

    This function takes a data file of satellite position in ECI coordinates and returns the Geographical coordinates.
    This is a simplified model that does not account for precession or nutation.
    """
    data = np.loadtxt(dataFile, dtype='str', delimiter='\t', max_rows=maxLines, skiprows=0).astype(float)
    data[i][0] = datetime.strptime(data[i][0], '%d %b %Y %H:%M:%S.%f') for i in range(maxLines - 1)

    siderealRotationRate = 7292115167 * 10**(-14) * 3600 #rad/h
    GMST = getGMST(data[:, 0])
    theta = siderealRotationRate * GMST

    def rotationMatrix(theta):
        return np.array([cos(theta), sin(theta), 0], [-sin(theta), cos(theta), 0], [0, 0, 1])

    #Convert ECI to ECEF
    xyzECEF = np.zeros((maxLines - 1, 3))
    for j in tange(maxLines - 1):
        xyzECEF[j] = np.multiply(rotationMatrix(theta), np.array([data[j, 7], data[j, 8], data[j, 9]]))

    #Determine Altitude
    geographicalCoordinates = np.zeros((maxLines - 1, 3))
    geographicalCoordinates[:, 2] = np.linalg.norm(xyzECEF, axis=0) - surface_radius

    #Determine Lattitude
    negativeIndices = np.where(xyzECEF[:, 2] < 0)[0]
    positiveIndices = np.where(xyzECEF[:, 2] >= 0)[0]
    xyECEF = np.zeros((maxLines - 1, 3))
    xyECEF[:, 0], xyECEF[:, 1] = xyzECEF[:, 0], xyzECEF[:, 1]
    geographicalCoordinates[negativeIndices, 0] = -getAngle(xyECEF[negativeIndices, :], xyzECEF[negativeIndices, :])
    geographicalCoordinates[positiveIndices, 0] = getAngle(xyECEF[negativeIndices, :], xyzECEF[negativeIndices, :])

    #Determine Azimuth
    negativeIndices = np.where(xyzECEF[:, 1] < 0)[0]
    positiveIndices = np.where(xyzECEF[:, 1] >= 0)[0]
    referenceArray = np.full((rows, 3), np.array([1, 0, 0]))
    geographicalCoordinates[negativeIndices, 1] = 360 - getAngle(referenceArray[negativeIndices], xyECEF[negativeIndices, :])
    geographicalCoordinates[positiveIndices, 1] = getAngle(referenceArray[positiveIndices], xyECEF[positiveIndices, :])

    return geographicalCoordinates