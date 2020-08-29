from numpy import sin, cos, tan, arctan
import numpy as np

from datetime import datetime

from matplotlib import pyplot as plt

from scipy.interpolate import interp1d

times = []
elapsedsecs = []
altitude = []

latitude = []
longitude = []

### Import File
with open("data.txt", "r") as f:
    for line in f.readlines()[1:50]:
        line = line.strip("\n").split("\t") 

        times.append(datetime.strptime(line[0], "%d %b %Y %H:%M:%S.%f"))

        elapsedsecs.append(float(line[1]))
        altitude.append(float(line[2]))
        latitude.append(float(line[3]))
        longitude.append(float(line[4]))

## Prepare Data
secs = np.array(elapsedsecs)
alts = np.array(altitude)

lats = np.array(latitude)
longs = np.array(longitude)


## Interpolation
interp_alt = interp1d(secs, alts, "cubic")
# Creates a function which uses a cubic interpolation of the data

t_end = secs[-1]

supertimes = np.linspace(0, t_end, 200)
# make finer timesteps

superalts = interp_alt(supertimes)
# make arrays using the interpolated function

plt.plot(supertimes, superalts, "x")
plt.plot(secs, alts, "o")
plt.show()