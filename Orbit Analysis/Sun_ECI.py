import numpy as np
import datetime, math

def ecliptic_to_eci(lam, beta, R):
    '''
    converts a [lat, long, distance] spherical coordinate vector in 
    Earth Centered Ecliptic Coordinate System to cartesian position vector
    '''

    E = 0.4091 # axial tilt of the Earth

    rotation_matrix = np.matrix([[1, 0 ,0], [0, np.cos(E), -np.sin(E)], [0, np.sin(E), np.cos(E)]])

    return rotation_matrix * np.array([lam, beta, R]).reshape((3,1))

def sun_ecliptic(J2000: float):
    '''
    Returns a [lat, long, distance] spherical coordinate vector of the Sun's position
    in the Earth Centered Ecliptic Coordinate System
    '''
    # mean longitude
    L = 280.460 + 0.9856474 * J2000

    # mean anomaly of Sun
    g = 357.528 + 0.9856003 * J2000

    L = np.pi * L / 180
    g = np.pi * g / 180

    lam = L + 1.915 * np.sin(np.pi * g / 180) + 0.02 * np.sin(np.pi * g / 90)

    beta = 0 # latitude of sun in ecliptic frame is zero

    R = 1.0014 - 0.01671 * np.cos(np.pi * g / 180) - 0.00014 * np.cos(np.pi * g / 90)
    # distance to the Sun

    return lam, beta, R * 1.5e8


def to_jd(dt: datetime):
    # source: https://github.com/dannyzed/julian

    a = math.floor((14-dt.month)/12)
    y = dt.year + 4800 - a
    m = dt.month + 12*a - 3

    jdn = dt.day + math.floor((153*m + 2)/5) + 365*y + math.floor(y/4) - math.floor(y/100) + math.floor(y/400) - 32045

    return jdn + (dt.hour - 12) / 24 + dt.minute / 1440 + dt.second / 86400 + dt.microsecond / 86400000000

if __name__ == "__main__":
    print(f"Time is currently: {datetime.datetime.now().strftime('%A, %B %d, %Y -- %H:%M:%S')}")

    now = datetime.datetime.utcnow()

    MJ2000 = to_jd(now) - 2451545
    # translation of epochs

    print(f"MJ2000 Date: {MJ2000}")

    print(f"Sun's current position: {ecliptic_to_eci(*(sun_ecliptic(MJ2000)))}")