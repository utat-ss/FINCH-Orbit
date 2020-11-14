import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d

from astropy.coordinates import SkyCoord, EarthLocation, GCRS, ITRS
from astropy import coordinates as coord
from astropy.time import Time
from astropy import units as u

# USING GMAT https://documentation.help/GMAT

## Demo analysis code
data = np.genfromtxt("report.txt", dtype=float, delimiter=",", skip_header=1)
# Opens a report file, and turns it into a numpy-compatible array.
# As with our example, our file would take the form
'''
HEADER1,HEADER2....
VALUE1,VALUE2....
'''
# for a set of n values.
# skip_header = 1 means we skip the line of headers to get right into the data.

mjd_values = data[:,0] + 29999.5
times = Time(mjd_values, format="mjd")
# Times from GMAT imported into astropy

finch_track = SkyCoord(x=data[:,1], y=data[:,2], z=data[:,3], unit="km",frame=GCRS(obstime=times), representation_type="cartesian")

toronto = EarthLocation.from_geodetic(-79.3832*u.deg,43.651070*u.deg, 76*u.m)
# Toronto is at 79.3832 W, 43.651070 N, 76m height

aa_frame = coord.AltAz(obstime=times, location=toronto)

aa_finch_track = finch_track.transform_to(aa_frame)

print(aa_finch_track)
