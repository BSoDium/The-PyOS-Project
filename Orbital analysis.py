from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.gui.DirectGui import *
import sys
from math import *

### Orbital Analysis

## Physical approach :

''' What's an orbit ? 
    It's the gravitationally curved trajectory of an object 
    The major part of orbits are supposed circulars, but to fit with reality let's consider them elliptics.
    There is severals types of orbits : Suborbitals trajectories and Escape trajectories 
    To define our orbits we will need some parameters as : Eccentricity, Half-major axis, tilt, longitude of the ascending node, perry argument, periapsis and the position.

    About the position : 
    Let's consider the average anomaly, which allows us to know the angle between the periapsis and the actual position of the planet in the orbit.
    We note the average anomaly M, we have : 'G' the gravitationnal constant, 'a' the half major axis, 'Ms' the mass of the planet, 'm' the mass of the studied object.
    M = sqrt(G(Ms+m)/a³)*t
'''

def average_anomaly(Ms,m,t,a):
    M=sqrt(6.67408*10**-11*(Ms+m)/a**3)*t
    return M

