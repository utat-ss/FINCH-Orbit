from numpy import sin, cos, tan, arctan
import numpy as np

import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.offsetbox import AnchoredText

'''
FINCH ORBIT VISUALIZER DEV 0.2

Mingde Yin
'''

## User inputs

NUM_STEPS = 50 # number of computation steps in an orbit; lower is faster
EARTH_RADIUS = 6371 # km

# Orbital Elements

sma = 6920. # km -- make sure these are floats
ecc = 0.007
ii = 97.4 * np.pi/180 # degrees --> radians 
raa = 0. * np.pi/180  # degrees --> radians
aopo = 90 * np.pi/180 # degrees --> radians

muu = 3.98e5 # std. Gravitational parameter of the Earth

t0 = 0

## Global orbit data
r_eci, v_eci, times, period = None, None, None, None # required for animation to work.

def findNodes(a,e,i,ra,aop,mu):
    '''
    Calculates AN position
    '''
    theta =  2*np.pi - aop # true anomaly
    r = a*(1 - e**2)/(1 + e*cos(theta))

    ## Perifocal Orbital Elements
    rAN = r*np.array((cos(theta),sin(theta),0))

    theta =  np.pi - aop # true anomaly
    r = a*(1 - e**2)/(1 + e*cos(theta))

    ## Perifocal Orbital Elements
    rDN = r*np.array((cos(theta),sin(theta),0))
    
    ## Perifocal to ECI (Earth Centred Inertial) rotation matrix
    C3w = np.matrix([[cos(aop), sin(aop), 0], [-sin(aop), cos(aop), 0], [0, 0, 1]])
    C1i = np.matrix([[1, 0, 0],[0, cos(i), sin(i)],[0, -sin(i), cos(i)]])
    C3O = np.matrix([[cos(ra), sin(ra), 0], [-sin(ra), cos(ra), 0], [0, 0, 1]])
    
    Cgp = np.array((C3w*C1i*C3O).I)
    
    ## Transform Perifocal to ECI
    pos_AN = np.matmul(Cgp, rAN)
    pos_DN = np.matmul(Cgp, rDN)

    return pos_AN, pos_DN

def apsides(a,e,i,ra,aop,m,mu):
    ## Creates position & velocity vector of spacecraft using input orbital elements

    E = m + ((e*sin(m))/(1-sin(m + e) + sin(m))) # Eccentric anomaly

    theta = 2*arctan(np.sqrt((1+e)/(1-e))*tan(E/2)) # true anomaly

    r = a*(1 - e**2)/(1 + e*cos(theta)) # distance of the orbit at a point (magnitude of position)
    
    return max(r) - EARTH_RADIUS, min(r) - EARTH_RADIUS

def orb_mechanics(a,e,i,ra,aop,m,mu):
    ## Creates position & velocity vector of spacecraft using input orbital elements

    E = m + ((e*sin(m))/(1-sin(m + e) + sin(m))) # Eccentric anomaly

    theta = 2*arctan(np.sqrt((1+e)/(1-e))*tan(E/2)) # true anomaly

    r = a*(1 - e**2)/(1 + e*cos(theta)) # distance of the orbit at a point (magnitude of position)

    v = np.sqrt(mu/(a*(1 - e**2))) # magnitude of velocity

    ## Perifocal Orbital Elements
    rp = r*np.vstack((cos(theta),sin(theta),np.zeros(theta.shape[0])))
    vp = v*np.vstack((-sin(theta),e + cos(theta),np.zeros(theta.shape[0])))
    
    ## Perifocal to ECI (Earth Centred Inertial) rotation matrix
    C3w = np.matrix([[cos(aop), sin(aop), 0], [-sin(aop), cos(aop), 0], [0, 0, 1]])
    C1i = np.matrix([[1, 0, 0],[0, cos(i), sin(i)],[0, -sin(i), cos(i)]])
    C3O = np.matrix([[cos(ra), sin(ra), 0], [-sin(ra), cos(ra), 0], [0, 0, 1]])
    
    
    Cgp = np.array((C3w*C1i*C3O).I)

    print(Cgp)
    
    ## Transform Perifocal to ECI
    r_eci = (np.matmul(Cgp, rp)).T
    v_eci = (np.matmul(Cgp, vp)).T

    return r_eci, v_eci


## Initializing Plot

fig = plt.figure("FINCH Orbit Visualizer Dev 0.2")
ax = fig.add_subplot(111, projection='3d')
ax.set_title('Visualized Orbit')

# sphere
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = EARTH_RADIUS*np.cos(u)*np.sin(v)
y = EARTH_RADIUS*np.sin(u)*np.sin(v)
z = EARTH_RADIUS*np.cos(v)

ax.plot_wireframe(x, y, z, color="#5892D0", alpha=0.25)

orb_i, = ax.plot3D([0],[0],[0],color="#22FF1F", lw=3)

AP, = ax.plot3D([0],[0],[0], color="#0099ff", marker="o", linestyle="None", label = "AP/PE")
PE, = ax.plot3D([0],[0],[0], color="#0099ff", marker="o", linestyle="None")

AN, = ax.plot3D([0],[0],[0], color="#ff3d5a", marker="o", linestyle="None", label = "AN/DN")
DN, = ax.plot3D([0],[0],[0], color="#ff3d5a", marker="o", linestyle="None")
nodal_line, = ax.plot3D([0],[0],[0], color = "#ff3d5a")

Marker, = ax.plot3D([0],[0],[0], "ko", label = "Satellite")

v_vector, = ax.plot3D([0],[0],[0], color = "k")

at = AnchoredText("", frameon=True, bbox_to_anchor=(0, 0.7),
                       bbox_transform=ax.transAxes,loc='upper right')
at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
ax.add_artist(at)

at2 = AnchoredText("", frameon=True, bbox_to_anchor=(0.15, 0.4),
                       bbox_transform=ax.transAxes,loc='upper right')
at2.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
ax.add_artist(at2)

plt.axis('off')

plt.legend(bbox_to_anchor=(0, 1), loc='upper right', ncol=1)
plt.subplots_adjust(bottom=0, left=0.25, right=1, top=0.9)

'''
Sliders
'''
axsma = plt.axes([0.125, 0.03, 0.3, 0.03])
axecc = plt.axes([0.125, 0.08, 0.3, 0.03])

axran = plt.axes([0.62, 0.03, 0.3, 0.03])
axinc = plt.axes([0.62, 0.08, 0.3, 0.03])

axaop = plt.axes([0.125, 0.13, 0.3, 0.03])

ssma = Slider(axsma, 'SMA (km)', EARTH_RADIUS, 25000, valinit=sma )
secc = Slider(axecc, 'ECC [0-1]', 0, 1, valinit=ecc)

sran = Slider(axran, 'RAAN (°)', 0, 360, valinit=raa * 180/np.pi)
sinc = Slider(axinc, 'INC (°)', 0, 360, valinit=ii * 180/np.pi)

saop = Slider(axaop, "AOP (°)", 0, 360, valinit=aopo * 180/np.pi)

def update(val):
    '''
    When a slider is updated.

    Reject the val variable, as it is only applicable for changing one slider.
    '''
    global sma, r_eci, v_eci, times, period

    ecc = secc.val
    ii = sinc.val * (np.pi/180)
    raa = sran.val * (np.pi/180)
    aopo = saop.val * (np.pi/180)
    # Compute new orbital parameters
  
    if ssma.val != sma:
        sma = ssma.val
        ax.set_xlim3d([-sma, sma])
        ax.set_ylim3d([-sma, sma])
        ax.set_zlim3d([-sma, sma])
    
    period = 2*np.pi*np.sqrt(sma**3/muu) # period of orbit in seconds 

    times = np.linspace(0, period, NUM_STEPS) # array of times

    ma = np.sqrt(muu/np.power(sma,3))*(times-t0) # mean anomaly

    ap, pe = apsides(sma,ecc,ii,raa,aopo,ma,muu)

    r_eci, v_eci = orb_mechanics(sma,ecc,ii,raa,aopo,ma,muu) # Earth Centered Inertial Coordinate System

    v = np.sqrt(v_eci[:,0]**2 + v_eci[:,1]**2 + v_eci[:,2]**2) # magnitude of velocity

    formatted_p = time.strftime('%Hh %Mm %Ss', time.gmtime(period))

    at.txt.set_text(f"Orbit Information:\nPeriod: {formatted_p}\nAP: {round(ap,2)}km\nPE: {round(pe,2)}km\nMax. Spd: {round(max(v),3)}km/s\nMin. Spd: {round(min(v),3)}km/s")

    # AP and PE
    AP.set_data(r_eci[int(NUM_STEPS/2),0], r_eci[int(NUM_STEPS/2),1])
    AP.set_3d_properties(r_eci[int(NUM_STEPS/2),2])

    PE.set_data(r_eci[0,0], r_eci[0,1])
    PE.set_3d_properties(r_eci[0,2])

    # AN and DN
    an, dn = findNodes(sma,ecc,ii,raa,aopo,muu)
    AN.set_data(an[0], an[1])
    AN.set_3d_properties(an[2])

    DN.set_data(dn[0], dn[1])
    DN.set_3d_properties(dn[2])

    nodes = np.vstack((an,dn))
    nodal_line.set_data(*nodes.T[:2])
    nodal_line.set_3d_properties(nodes.T[2])

    # Orbit Path
    orb_i.set_data(r_eci[:,0], r_eci[:,1])
    orb_i.set_3d_properties(r_eci[:,2])

    Marker.set_data(r_eci[0,0], r_eci[0,1])
    Marker.set_3d_properties(r_eci[0,2])

    fig.canvas.draw_idle()

# Set sliders to update
ssma.on_changed(update)
secc.on_changed(update)
sran.on_changed(update)
sinc.on_changed(update)
saop.on_changed(update)

update(0)

def animate(i):
    '''
    Animates the plot.
    '''
    speed = np.linalg.norm(v_eci[i])

    formatted_p = time.strftime('%Hh %Mm %Ss', time.gmtime(period-times[i]))
    # formatted time to display

    alt = np.sqrt(r_eci[i,0]**2 + r_eci[i,1]**2 + r_eci[i,2]**2) - EARTH_RADIUS # altitude

    at2.txt.set_text(f"Spacecraft Information:\nSpeed: {round(speed,3)}km/s\nAltitude: {round(alt,3)}km\nTime to Periapsis: {formatted_p}")

    v_v = np.vstack((r_eci[i], r_eci[i]+v_eci[i]/speed * sma/6))
    # making the vector to plot as the velocity vector

    v_vector.set_data(v_v[:,0], v_v[:,1])
    v_vector.set_3d_properties(v_v[:,2])

    Marker.set_data(r_eci[i,0], r_eci[i,1])
    Marker.set_3d_properties(r_eci[i,2])
    # moving the spacecraft position

    return (Marker, v_vector)

ani = animation.FuncAnimation(fig, animate, frames=NUM_STEPS, blit=False)

plt.show()

