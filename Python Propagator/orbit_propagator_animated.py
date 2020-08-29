from numpy import sin, cos, tan, arctan
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


"""User inputs"""
with open("orbit.txt", "r") as f:
    sma, ecc, ii, raa, aopo, muu = [float(n) for n in f.readlines()]

t0 = 0

def orb_mechanics(a,e,i,ra,aop,m,mu):
    """Creates position & velocity vector of spacecraft using input orbital elements"""
    E = m + ((e*sin(m))/(1-sin(m + e) + sin(m)))
    theta = 2*arctan(np.sqrt((1+e)/(1-e))*tan(E/2))
    r = a*(1 - pow(e,2))/(1 + e*cos(theta))
    v = np.sqrt(mu/(a*(1 - pow(e,2))))
    rp = r*np.array([cos(theta),sin(theta),0])
    vp = v*np.array([-sin(theta),e + cos(theta),0])
    """Perifocal to ECI rotation matrix"""
    ci = cos(i)
    si = sin(i)
    co = cos(ra)
    so = sin(ra)
    cw = cos(aop)
    sw = sin(aop)

    Cgp = np.array([[co*cw - so*ci*sw , -co*sw - so*ci*cw , so*si],[so*cw + co*ci*sw , -so*sw + co*ci*sw , -co*si],[si*sw , si*cw , ci]])
    r_eci = np.matmul(Cgp, rp)
    v_eci = np.matmul(Cgp, vp)
    return r_eci

r_eci = []

times = np.arange(1, 7200) # Array of times

for t in times:
    ma = np.sqrt(muu/np.power(sma,3))*(t-t0)
    r_eci.append(orb_mechanics(sma,ecc,ii,raa,aopo,ma,muu))

r_eci = np.array(r_eci) # this step is to make it easier to index.

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

earth, = ax.plot3D([0],[0],[0],'bo')

orb_i, = ax.plot3D(r_eci[:,0], r_eci[:,1], r_eci[:,2], label = "$r_eci")

ax.set_xlim3d([-sma, sma])
ax.set_ylim3d([-sma, sma])
ax.set_zlim3d([-sma, sma])

plt.legend()

def animate(i):
    '''
    Animates the plot.
    '''

    orb_i.set_data(r_eci[:i,0], r_eci[:i,1])
    orb_i.set_3d_properties(r_eci[:i,2])

    return (earth,) + (orb_i,)

ani = animation.FuncAnimation(fig, animate,frames=7200, interval=1, blit=True)
plt.show()
