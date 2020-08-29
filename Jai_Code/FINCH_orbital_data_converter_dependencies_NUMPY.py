#UTAT - Orbital Subsystem

#Jai Willems, 1006342165
#University of Toronto Faculty of Applied Science and Engineering
#Division of Engineeing Science
#Completed 18-08-2020

#The purpose of this script is to yeild the appropriate functions required by conversion scripts.

#---------------------------------------------------------------------------------------------------------------------------------



from math import cos, sin, acos, atan, sqrt, degrees, radians
import numpy as np



#----------------------------------------------------------------------------------------------------
#   Vector Conversions                                                                              -
#----------------------------------------------------------------------------------------------------



def convertToSpherical(x_y_z_array):
    """
    (np.array) -> np.array

    This function takes an array in cartesian coordinates and converts it to spherical coordinates.
    """
    x = x_y_z_array[0]
    y = x_y_z_array[1]
    z = x_y_z_array[2]
    r = sqrt(x**2 + y**2 + z**2)
    if x == 0 and y > 0:
        theta = 90
    elif x == 0 and y < 0:
        theta = -90
    else:
        if x > 0:
            theta = degrees(atan(y / x))
        elif x < 0 and y > 0:
            theta = 180 + degrees(atan(y / x))
        else:
            theta = -180 + degrees(atan(y / x))
    phi = degrees(acos(z / r))
    sphArray = np.array([r, theta, phi])
    return sphArray



def convertToCartesian(r_theta_phi_array):
    """
    (np.array) -> np.array

    This function takes an array in spherical coordinates and converts it to cartesian coordinates.
    """
    r = r_theta_phi_array[0]
    theta = radians(r_theta_phi_array[1])
    phi = radians(r_theta_phi_array[2])
    x = r * sin(phi) * cos(theta)
    y = r * sin(theta) * sin(phi)
    z = r * cos(phi)
    cartArray = np.array([x, y, z])
    return cartArray



#----------------------------------------------------------------------------------------------------
#   Vector Operations                                                                               -
#----------------------------------------------------------------------------------------------------



def getAngle(x_y_z_array_one, x_y_z_array_two):
    """
    (np.array, np.array) -> float

    This function takes two arrays in cartesian coordinates and returns the degree angle between the two arrays.
    """
    argument = np.dot(x_y_z_array_one, x_y_z_array_two) / (np.linalg.norm(x_y_z_array_one) * np.linalg.norm(x_y_z_array_two))
    angle = degrees(acos(argument))
    return angle



#----------------------------------------------------------------------------------------------------
#   Orbital Specific Dependencies                                                                   -
#----------------------------------------------------------------------------------------------------



def changeVectorCoordinateAxes(x_axis_array, array_to_modify):
    """
    (np.array, np.array) -> np.array

    This function takes two array inputs as spherical coordinates. The fist is the array which
    defines the transformations to be made to the system such that the x_axis_array moves to the
    position of the x-axis. The same tranformations are applied to array_to_modify so that it
    remains in the new coordinate system.
    """
    zRotationAngle = -radians(x_axis_array[1])
    yRotationAngle = radians(90 - x_axis_array[2])

    zMatrix = np.array([[cos(zRotationAngle), -sin(zRotationAngle), 0], [sin(zRotationAngle), cos(zRotationAngle), 0], [0, 0, 1]])
    yMatrix = np.array([[cos(yRotationAngle), 0, sin(yRotationAngle)], [0, 1, 0], [-sin(yRotationAngle), 0, cos(yRotationAngle)]])

    productArray = np.dot(zMatrix, convertToCartesian(array_to_modify))
    productArray = np.dot(yMatrix, productArray)
    
    return productArray



def findAltitude(yz_array, array):
    """
    (np.array, np.array) -> float

    This function takes two arrays in cartesian coordinates, an array and its projection on the YZ 
    plane and returns the degree angle between the two arrays.
    """
    if array[0] > 0:
        return getAngle(yz_array, array)
    return -getAngle(yz_array, array)



def findAzimuth(yz_array):
    """
    (np.array) -> float

    This function takes an array in cartesian coordinates and returns the angle from the k_hat unit
    vector clockwise on the YZ plane to the given yz_array.
    """
    referenceArray = np.array([0, 0, 1])
    if yz_array[1] >= 0:
        return getAngle(referenceArray, yz_array)
    return 360 - getAngle(referenceArray, yz_array)



#----------------------------------------------------------------------------------------------------
#   Summation Functions                                                                             -
#----------------------------------------------------------------------------------------------------



def findHorizontalAndSatelliteNadirToLOSAngle(satellite_coor, satellite_height, observer_coor = (43.662300, -79.394530), surface_radius = 6371):
    """
    (np.array, float, np.array, float) -> tuple

    This function takes the coordinates and height of the observation station and satellite and returns
    the computed altitude and azimuth of the satellite.
    """
    rObserver = surface_radius
    thetaObserver = observer_coor[1]
    phiObserver = 90 - observer_coor[0]
    sphObserver = np.array([rObserver, thetaObserver, phiObserver])
    xyzObserver = convertToCartesian(sphObserver)

    rSatellite = surface_radius + satellite_height
    thetaSatellite = satellite_coor[1]
    phiSatellite = 90 - satellite_coor[0]
    sphSatellite = np.array([rSatellite, thetaSatellite, phiSatellite])
    xyzSatellite = convertToCartesian(sphSatellite)

    xyzLineOfSight = np.subtract(xyzSatellite, xyzObserver)
    sphLineOfSight = convertToSpherical(xyzLineOfSight)
    xyzLineOfSightPrime = changeVectorCoordinateAxes(sphObserver, sphLineOfSight)
    yzLineOfSight = np.array([0, xyzLineOfSightPrime[1], xyzLineOfSightPrime[2]])

    altitude = findAltitude(yzLineOfSight, xyzLineOfSightPrime)
    azimuth = findAzimuth(yzLineOfSight)
    if altitude >= 0:
        nadirLOSAngle = getAngle(xyzLineOfSight, xyzSatellite)
    else:
        nadirLOSAngle = -1

    return tuple([altitude, azimuth, nadirLOSAngle])