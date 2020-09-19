#UTAT - Orbital Subsystem

#Jai Willems with assistance from Mingde Yin, 1006342165
#University of Toronto Faculty of Applied Science and Engineering
#Division of Engineeing Science
#Completed 27-08-2020

#The purpose of this script is to yeild the appropriate functions required by conversion scripts.

#---------------------------------------------------------------------------------------------------------------------------------



from math import cos, sin
import numpy as np



#----------------------------------------------------------------------------------------------------
#   Vector Conversions                                                                              -
#----------------------------------------------------------------------------------------------------



def convertToSpherical(x_y_z_array):
    """
    (np.array) -> np.array

    This function takes a multidimensional array of cartesian coordinates and converts it to 
    spherical element-wise.
    """
    rows = x_y_z_array.shape[0]
    sphEquivilent = np.zeros((rows, 3))

    sphEquivilent[:, 0] = np.sqrt(np.add(np.add(np.square(x_y_z_array[:, 0]), np.square(x_y_z_array[:, 1])), np.square(x_y_z_array[:, 2])))

    indicesOne = np.where((x_y_z_array[:, 0] == 0) & (x_y_z_array[:, 1] > 0))
    sphEquivilent[indicesOne[0], 1] = 90
    indicesTwo = np.where((x_y_z_array[:, 0] == 0) & (x_y_z_array[:, 1] < 0))
    sphEquivilent[indicesTwo[0], 1] = -90
    indicesThree = np.where(x_y_z_array[:, 0] > 0)
    sphEquivilent[indicesThree[0], 1] = np.degrees(np.arctan(np.divide(x_y_z_array[indicesThree[0], 1], x_y_z_array[indicesThree[0], 0])))
    indicesFour = np.where((x_y_z_array[:, 0] < 0) & (x_y_z_array[:, 1] > 0))
    sphEquivilent[indicesFour[0], 1] = 180 + np.degrees(np.arctan(np.divide(x_y_z_array[indicesFour[0], 1], x_y_z_array[indicesFour[0], 0])))
    indicesFive = np.where((x_y_z_array[:, 0] < 0) & (x_y_z_array[:, 1] <= 0))
    sphEquivilent[indicesFive[0], 1] = np.degrees(np.arctan(np.divide(x_y_z_array[indicesFive[0], 1], x_y_z_array[indicesFive[0], 0]))) - 180
    
    sphEquivilent[:, 2] = np.degrees(np.arccos(np.divide(x_y_z_array[:, 2], sphEquivilent[:, 0])))

    return sphEquivilent



def convertToCartesian(r_theta_phi_array):
    """
    (np.array) -> np.array

    This function takes a multidimensional array of spherical coordinates and converts it to 
    cartesian element-wise.
    """
    rows = r_theta_phi_array.shape[0]
    cartEquivilent = np.zeros((rows, 3))

    r = r_theta_phi_array[:, 0]
    theta = np.radians(r_theta_phi_array[:, 1])
    phi = np.radians(r_theta_phi_array[:, 2])

    cartEquivilent[:, 0] = np.multiply(r, np.multiply(np.sin(phi), np.cos(theta)))
    cartEquivilent[:, 1] = np.multiply(r, np.multiply(np.sin(theta), np.sin(phi)))
    cartEquivilent[:, 2] = np.multiply(r, np.cos(phi))

    return cartEquivilent



#----------------------------------------------------------------------------------------------------
#   Vector Operations                                                                               -
#----------------------------------------------------------------------------------------------------



def getAngle(x_y_z_array_one, x_y_z_array_two):
    """
    (np.array, np.array) -> float

    This function takes two multidimensional arrays in cartesian coordinates and returns the degree 
    angle between the two arrays element-wise.
    """
    length = np.shape(x_y_z_array_one)[0]
    dividend = np.zeros((length, ))
    divisor = np.zeros((length, ))
    for i in range(length):
        dividend[i] = np.dot(x_y_z_array_one[i], x_y_z_array_two[i])
        divisor[i] = np.multiply(np.linalg.norm(x_y_z_array_one[i]), np.linalg.norm(x_y_z_array_two[i]))
    argument = np.divide(dividend, divisor)
    angle = np.degrees(np.arccos(argument))
    return angle



#----------------------------------------------------------------------------------------------------
#   Orbital Specific Dependencies                                                                   -
#----------------------------------------------------------------------------------------------------



def changeVectorCoordinateAxes(x_axis_array, array_to_modify):
    """
    (np.array, np.array) -> np.array

    This function takes two multidimensional arrays of spherical coordinates as inputs. x_axis_array 
    defines the transformations to be made to the system such that the x_axis_array moves to the
    position of the x-axis in an element-wise fashion. The same tranformation is applied element-wise
    to array_to_modify so that it transisions to the coordinate permutation.
    """
    rows = x_axis_array.shape[0]
    rotationAnglesZY = np.zeros((rows, 2))

    rotationAnglesZY[:, 0] = -np.radians(x_axis_array[:, 1])
    rotationAnglesZY[:, 1] = np.radians(90 - x_axis_array[:, 2])

    def zMatrix(zRotationAngle):
        return np.array([[cos(zRotationAngle), -sin(zRotationAngle), 0], [sin(zRotationAngle), cos(zRotationAngle), 0], [0, 0, 1]])

    def yMatrix(yRotationAngle):
        return np.array([[cos(yRotationAngle), 0, sin(yRotationAngle)], [0, 1, 0], [-sin(yRotationAngle), 0, cos(yRotationAngle)]])

    oldCoordinates = convertToCartesian(array_to_modify)
    newCoordinates = np.zeros((rows, 3))
    for i in range(rows):
        temp = np.dot(zMatrix(rotationAnglesZY[i, 0]), oldCoordinates[i])
        newCoordinates[i] = np.dot(yMatrix(rotationAnglesZY[i, 1]), temp)
    
    return newCoordinates



#----------------------------------------------------------------------------------------------------
#   Summation Functions                                                                             -
#----------------------------------------------------------------------------------------------------



def findSatPositionData(satellite_coor, satellite_height, imaging_coor = (43.662300, -79.394530), observer_coor = (43.662300, -79.394530), surface_radius = 6371):
    """
    ((np.array, np.array), np.array, tuple, tuple, float) -> np.array

    This function takes the coordinates and heights of the satellite as multidimensional arrays, the 
    imaging and observation coordinates as tuples, and the surface radius as a float. It returns the 
    element-wise computed altitude, azimuth, and nadir/LOS angle as a multidimensional array.
    """
    rows = np.shape(satellite_coor[0])[0]
    shape = (rows, 3)

    sphSatellite = np.zeros(shape)
    sphSatellite[:, 0] = surface_radius + satellite_height
    sphSatellite[:, 1] = satellite_coor[1]
    sphSatellite[:, 2] = 90 - satellite_coor[0]
    xyzSatellite = convertToCartesian(sphSatellite)

    sphObserver = np.array([[surface_radius, observer_coor[1], 90 - observer_coor[0]]])
    xyzObserver = np.zeros(shape)
    xyzObserver[:, :] = convertToCartesian(sphObserver)
    sphObserver = convertToSpherical(xyzObserver)

    xyzLineOfSight = np.subtract(xyzSatellite, xyzObserver)
    sphLineOfSight = convertToSpherical(xyzLineOfSight)
    xyzLineOfSightPrime = changeVectorCoordinateAxes(sphObserver, sphLineOfSight)
    yzLineOfSight = np.copy(xyzLineOfSightPrime)
    yzLineOfSight[:, 0] = 0

    position = np.zeros((rows, 4))

    #Determine Altitude
    negativeIndices = np.where(xyzLineOfSightPrime[:, 0] < 0)
    positiveIndices = np.where(xyzLineOfSightPrime[:, 0] >= 0)
    position[negativeIndices[0], 0] = -getAngle(yzLineOfSight[negativeIndices[0], :], xyzLineOfSightPrime[negativeIndices[0], :])
    position[positiveIndices[0], 0] = getAngle(yzLineOfSight[positiveIndices[0], :], xyzLineOfSightPrime[positiveIndices[0], :])

    #Determine Azimuth
    negativeIndices = np.where(yzLineOfSight[:, 1] < 0)
    positiveIndices = np.where(yzLineOfSight[:, 1] >= 0)
    referenceArray = np.zeros((rows, 3))
    referenceArray[:] = [0, 0, 1]
    position[negativeIndices[0], 1] = 360 - getAngle(referenceArray[negativeIndices[0]], yzLineOfSight[negativeIndices[0], :])
    position[positiveIndices[0], 1] = getAngle(referenceArray[positiveIndices[0]], yzLineOfSight[positiveIndices[0], :])
    
    if imaging_coor != observer_coor:

        sphImaging = np.array([[surface_radius, imaging_coor[1], 90 - imaging_coor[0]]])
        xyzImaging = np.zeros(shape)
        xyzImaging[:, :] = convertToCartesian(sphImaging)
        sphImaging = convertToSpherical(xyzImaging)

        xyzLineOfSight = np.subtract(xyzSatellite, xyzImaging)
        sphLineOfSight = convertToSpherical(xyzLineOfSight)
        xyzLineOfSightPrime = changeVectorCoordinateAxes(sphImaging, sphLineOfSight)
        yzLineOfSight = np.copy(xyzLineOfSightPrime)
        yzLineOfSight[:, 0] = 0

        negativeIndices = np.where(xyzLineOfSightPrime[:, 0] < 0)
        positiveIndices = np.where(xyzLineOfSightPrime[:, 0] >= 0)
        position[negativeIndices[0], 2] = -getAngle(yzLineOfSight[negativeIndices[0], :], xyzLineOfSightPrime[negativeIndices[0], :])
        position[positiveIndices[0], 2] = getAngle(yzLineOfSight[positiveIndices[0], :], xyzLineOfSightPrime[positiveIndices[0], :])

        negativeIndices = np.where(position[:, 2] < 0)
        positiveIndices = np.where(position[:, 2] >= 0)
        position[negativeIndices[0], 3] = -1
        position[positiveIndices[0], 3] = getAngle(xyzLineOfSight[positiveIndices[0], :], xyzSatellite[positiveIndices[0], :])

    else:
        position[:, 2] = position[:, 0]
        negativeIndices = np.where(position[:, 0] < 0)
        positiveIndices = np.where(position[:, 0] >= 0)
        position[negativeIndices[0], 3] = -1
        position[positiveIndices[0], 3] = getAngle(xyzLineOfSight[positiveIndices[0], :], xyzSatellite[positiveIndices[0], :])

    return position