from numpy import sin, cos, tan, arctan
import numpy as np

import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.offsetbox import AnchoredText

from scipy.integrate import odeint
'''
Scipy integration demo

This is pretty bad example as this isn't a real DE, but nonetheless it shows what it needs to
'''

## User inputs

NUM_STEPS = 50 # number of computation steps in an orbit; lower is faster
EARTH_RADIUS = 6371 # km

J2 =  1.083e-3

# Orbital Elements

sma = 6920. # km -- make sure these are floats
ecc = 0.007
ii = 97.4 * np.pi/180 # degrees --> radians 
raa = 0. * np.pi/180  # degrees --> radians
aopo = 90 * np.pi/180 # degrees --> radians

muu = 3.98e5 # std. Gravitational parameter of the Earth

'''
Overall approach:
y is some vector containing the 5 orbtial elements

define a function dy/dt (t)

'''

def equation_system(y, t):

    sma, ecc, ii, raa, aopo = y
    # Unpack the incoming vector
    
    raa_dot = -3 * J2 * EARTH_RADIUS ** 2 / (2*(1-ecc**2)**2) * np.sqrt(muu/sma**7) * cos(ii)
    aopo_dot = 3 * J2 * EARTH_RADIUS ** 2 / (4*(1-ecc**2)**2) * np.sqrt(muu/sma**7) * (5*cos(ii)**2 - 1)

    return np.array([0, 0, 0, raa_dot, aopo_dot])
    # Return y'

t_initial = 0

t_final = 3e7 # around a year

times = np.linspace(t_initial, t_final, 200)

orbit_states = odeint(equation_system, np.array([sma, ecc, ii, raa, aopo]), times)
# Pass into ODE: dy/dy function, y0, timepoints

for i in range(1, orbit_states.shape[1]):

    names = ["SMA", "ECC", "INC", "RAAN", "AOP"]
    plt.plot(times, orbit_states[:,i], label = names[i])

plt.legend()
plt.show()