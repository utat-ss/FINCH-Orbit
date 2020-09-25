import numpy as np
from numpy import sin, cos, tan, pi, arctan, sqrt
from matplotlib import pyplot as plt

from matplotlib.widgets import Slider

def cartesiantopolar(x,y):
    theta = arctan(y/x)
    r = sqrt(x **2 + y ** 2)

    return (r, theta)

def polartocartesian(r,theta):
    x = r*cos(theta)
    y = r*sin(theta)

    return (x,y)

## Parameters
v = 50 # ms^-1
g = 9.81 # ms^-2
phi = 50 # degrees

planet_radius = 200 # m


## Trajectories
vx = v*cos(pi * phi/180)
vy = v*sin(pi * phi/180)
times = np.linspace(0,2*vy/g, 500) # impact time
x = vx * times # x positions
y = vy * times - 0.5 * g * times**2 # these will also be the radii
angularx = pi/2 - (x/planet_radius)


## Circle
theta = np.linspace(0, 2*pi)
circle = -planet_radius * np.ones(theta.shape[0])


## Plot Setup
fig = plt.figure("Parabolic Flight Demo")
ax = fig.add_subplot(111)
ax.set_title('Trajectory')

ax.set_aspect(1)
ax.grid()
plt.axis('off')


circ, = ax.plot(*polartocartesian(circle, theta))
traj, = ax.plot(*polartocartesian(y + planet_radius, angularx), lw=3)


## Sliders
axv = plt.axes([0.125, 0.03, 0.3, 0.03])
axphi = plt.axes([0.125, 0.08, 0.3, 0.03])

axg = plt.axes([0.62, 0.03, 0.3, 0.03])
axrad = plt.axes([0.62, 0.08, 0.3, 0.03])

sv = Slider(axv, 'Launch Speed (m/s)', 0, 200, valinit=20)
sphi = Slider(axphi, 'Launch Angle (degrees)', 0, 180, valinit=30)

sg = Slider(axg, 'Surface Gravity (m/s^2)', 1, 20, valinit=9.81)
srad = Slider(axrad, 'Planet Radius (m)', 1, 200, valinit=100)




def update(val):
    '''
    When a slider is updated.

    Reject the val variable, as it is only applicable for changing one slider.
    '''

    v = sv.val
    g = sg.val
    planet_radius = srad.val
    phi = sphi.val

    vx = v*cos(pi * phi/180)
    vy = v*sin(pi * phi/180)
    print(vy)
    times = np.linspace(0,2*vy/g, 500) # impact time
    x = vx * times # x positions
    y = vy * times - 0.5 * g * times**2 # these will also be the radii
    angularx = pi/2 - (x/planet_radius)

    traj.set_data(*polartocartesian(y + planet_radius, angularx))

    circle = -planet_radius * np.ones(theta.shape[0])

    circ.set_data(*polartocartesian(circle, theta))

    fig.canvas.draw_idle()

sv.on_changed(update)
sphi.on_changed(update)
sg.on_changed(update)
srad.on_changed(update)

plt.show()