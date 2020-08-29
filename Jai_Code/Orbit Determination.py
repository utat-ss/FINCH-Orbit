#UTAT - Orbital Subsystem

#Jai Willems, 1006342165
#University of Toronto Faculty of Applied Science and Engineering
#Division of Engineeing Science
#Completed 18-08-2020

#The purpose of this script is to create a orbital simulation program.

#---------------------------------------------------------------------------------------------------------------------------------



import numpy as np



initialPosition = np.array([0, 0, 200000])      #m
mass = 2000                                     #g
initialVelocity = np.array([761.1111, 0, 0])    #m/s
endTime = 5                                     #s
deltaT = 0.5                                    #s



class satellite():
    def __init__(self, position, mass, velocity):
        self.position = position
        self.mass = mass
        self.velocity = velocity
        self.momentum = np.dot(self.mass, self.velocity)
    
    def __str__(self):
        return('Position: (%.4f, %.4f, %.4f)\tVelocity: (%.4f, %.4f, %.4f)\tMass: %0.4f' %(self.position[0], self.position[1], self.position[2], self.velocity[0], self.velocity[1], self.velocity[2], self.mass))

    def updatePosition(self, netForce, deltaT):
        self.position = self.position + np.dot(netForce, deltaT)



class forces():
    def __init__(self):
        self.forces = np.array([[0, 0, 0]])
    
    def addEarthGravity(self, satObject):
        G = 0.000000000066733
        mEarth = 5972000000000000000000000
        mSat = satObject.mass
        dist = np.linalg.norm(satObject.position)
        constant = - (G * mEarth * mSat) / dist**2
        gravityForce = np.dot(constant, satObject.position)
        self.forces = np.append(self.forces, [gravityForce], axis=0)

    def findNetForce(self):
        return np.sum(self.forces, axis=0)



satObject = satellite(initialPosition, mass, initialVelocity)
currentTime = 0
while currentTime < endTime:

    appliedForces = forces()
    appliedForces.addEarthGravity(satObject)
    Fnet = appliedForces.findNetForce()

    satObject.updatePosition(Fnet, deltaT)
    print(satObject)

    currentTime += deltaT