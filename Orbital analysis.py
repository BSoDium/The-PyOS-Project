from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.gui.DirectGui import *
import sys
from math import *
import numpy as np

### Orbital Analysis

## Physical approach :

''' What's an orbit ? 
    It's the gravitationally curved trajectory of an object 
    The major part of orbits are supposed circulars, but to fit with reality let's consider them elliptics. (After we will add functions to make them parabolic and hyperbolic)
    There is severals types of orbits : Suborbitals trajectories and Escape trajectories 
    To define our orbits we will need some parameters as : Eccentricity, Half-major axis, tilt, longitude of the ascending node, perry argument, periapsis and the position.

    About the position : 
    Let's consider the average anomaly, which allows us to know the fraction of the orbital period that has elapsed since the last pass to the periapsis, expressed as an angle.
    We note the average anomaly 'M', we have : 'G' the gravitationnal constant, 'a' the half major axis, 'Ms' the mass of the planet, 'm' the mass of the studied object.
    M = sqrt(G(Ms+m)/a³)*t
'''

def average_anomaly(Ms,m,t,a):
    M=sqrt(6.67408*10**-11*(Ms+m)/a**3)*t
    return M

''' The average eccentric is the angle between the periapsis and the actual position projected in the cercle excircled perpendicularly to the half major axis. 
Let's note the average eccentric 'E'. Then with 'e' the exxentricity , we have :
The iteration : E[i+1]=(M-e*(E[i]cos(E[i]-sin(E[i]))/1-e*cos(E[i])) , by doing 4 iterations, we obtain a precise value of E for a t time'''

def average_eccentric(M,a):
    E=np.pi
    for i in range(1,5):
        E=(M-e*(E*cos(E)-sin(E)))/1-e*cos(E)
    return E

''' Finally the real anomaly is the angle between the periapsis and the actual position of the studied object (that's what we want). We note the real anomaly 'v', then :
tan(v/2) : sqrt(1+e/1-e)*tan(E/2)
'''

def real_anomaly(E,e):
    v=2*np.arctan(sqrt(1+e/1-e))*tant(E/2)
    return v


''' If we want to know what is the eccentricity of an orbit thanks to apoapsis radius(Ra) and periapsis radius(Rp), with :
e = (Ra-Rp)/(Ra+Rp)
or 
e = sqrt(1-(b²/a²))   with b the half minor axis and a the half major axis
'''

def e(Ra,Rp):
    e = (Ra-Rp)/(Ra+Rp)
    return e

def e_V2(a,b):
    e=sqrt(1-(b**2/a**2))
    return e

