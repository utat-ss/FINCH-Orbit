import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d

from matplotlib.widgets import Slider

from astropy.coordinates import SkyCoord, EarthLocation, GCRS, ITRS, AltAz
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

mjd_values = data[:,0] + 29999.5 # Standard MJD Epoch: 17 Nov 1858 00:00:00.000
mpl_jd_values = mjd_values - 40587 # Matplotlib Epoch: 01 Jan 1970 00:00:00.000

times = Time(mjd_values, format="mjd")
# Times from GMAT imported into astropy

finch_track = SkyCoord(x=data[:,1], y=data[:,2], z=data[:,3], unit="km",frame=GCRS(obstime=times), representation_type="cartesian")

toronto = EarthLocation.from_geodetic(-79.3832*u.deg,43.651070*u.deg, 76*u.m)
# Toronto is at 79.3832 W, 43.651070 N, 76m height

aa_frame = AltAz(obstime=times, location=toronto) # Coordinate system: Az/Alt from a given location on Earth
itrs_frame = ITRS(obstime=times) # ITRS: Centered around the Earth, rotating with the Earth

aa_finch_track = finch_track.transform_to(aa_frame)
itrs_finch_track = finch_track.transform_to(itrs_frame)

itrs_finch_track.earth_location.geodetic

plt.plot_date(mpl_jd_values, aa_finch_track.alt.deg, "-")
plt.title("Altitude of Spacecraft Above 79.3832 W, 43.651070 N (Toronto)")
plt.xlabel("Time [mm-dd hh]")
plt.ylabel("Altitude (degrees)")
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('Ground Track')

lon = itrs_finch_track.earth_location.geodetic.lon.degree
lat = itrs_finch_track.earth_location.geodetic.lat.degree

plot, = ax.plot(lon, lat, ".")
plt.xlim((-180, 180))
plt.ylim((-90, 90))
plt.xlabel("Longitude (degrees)")
plt.ylabel("Latitude (degrees)")

ax1 = plt.axes([0.125, 0.03, 0.3, 0.03])
slide = Slider(ax1, 'Time', 0, len(lon)-1, valinit=int(len(lon)/2))

def update(val):

    plot.set_data(lon[:int(slide.val)], lat[:int(slide.val)])

    fig.canvas.draw_idle()


slide.on_changed(update)


plt.show()
