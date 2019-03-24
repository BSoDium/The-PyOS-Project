'''                                                         
                                                                     
 ██████╗ ██████╗ ██████╗ ██╗████████╗ █████╗ ██╗          █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗███████╗██╗███████╗
██╔═══██╗██╔══██╗██╔══██╗██║╚══██╔══╝██╔══██╗██║         ██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝██╔════╝██║██╔════╝
██║   ██║██████╔╝██████╔╝██║   ██║   ███████║██║         ███████║██╔██╗ ██║███████║██║   ╚████╔╝ ███████╗██║███████╗
██║   ██║██╔══██╗██╔══██╗██║   ██║   ██╔══██║██║         ██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝  ╚════██║██║╚════██║
╚██████╔╝██║  ██║██████╔╝██║   ██║   ██║  ██║███████╗    ██║  ██║██║ ╚████║██║  ██║███████╗██║   ███████║██║███████║
 ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝   ╚══════╝╚═╝╚══════╝

'''

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.gui.DirectGui import *
import sys
from math import *
import numpy as np


#       ___  _  _ _   _ ____ _ ____ ____ _       ____ ___  ___  ____ ____ ____ ____ _  _ 
#       |__] |__|  \_/  [__  | |    |__| |       |__| |__] |__] |__/ |  | |__| |    |__| 
#       |    |  |   |   ___] | |___ |  | |___    |  | |    |    |  \ |__| |  | |___ |  | 
                                                                                 


''' What's an orbit ? 
    It's the gravitationally curved trajectory of an object 
    The major part of orbits are supposed circulars, but to fit with reality let's consider them elliptics. (After we will add functions to make them parabolic or hyperbolic).
    We take the ecuador of the created object as the plane reference.
    There is severals types of orbits : Suborbitals trajectories and Escape trajectories.
    To define our orbits we will need some parameters as : Eccentricity, Half-major axis, tilt, longitude of the ascending node, perry argument, periapsis and the position.
'''

#    About the position : 

''' Let's consider the average anomaly, which allows us to know the fraction of the orbital period that has elapsed since the last pass to the periapsis, expressed as an angle.
    We note the average anomaly 'M', we have : 'G' the gravitationnal constant, 'a' the half major axis, 'Ms' the mass of the planet, 'm' the mass of the studied object.
    M = sqrt(G(Ms+m)/a³)*t
'''

def average_anomaly(M,m,t,a):
    M=sqrt(6.67408*10**-11*(Ms+m)/a**3)*t
    return M

''' The average eccentric is the angle between the periapsis and the actual position projected in the cercle excircled perpendicularly to the half major axis. 
Let's note the average eccentric 'E'. Then with 'e' the eccentricity , we have :
The iteration : E[i+1]=(M-e*(E[i]cos(E[i]-sin(E[i]))/1-e*cos(E[i])) , by doing 4 iterations, we obtain a precise value of E for a t time.'''

def average_eccentric(M,e):
    E=np.pi
    for i in range(1,5):
        E=(M-e*(E*cos(E)-sin(E)))/1-e*cos(E)
    return E

''' Finally the true anomaly is the angle between the periapsis and the actual position of the studied object (that's what we want). We note the real anomaly 'v', then :
tan(v/2) : sqrt(1+e/1-e)*tan(E/2)
'''

def true_anomaly(E,e):
    v=2*np.arctan(sqrt(1+e/1-e))*np.tan(E/2)
    return v

''' If we want to know what is the eccentricity of an orbit, thanks to apoapsis radius(Ra) and periapsis radius(Rp), with :
e = (Ra-Rp)/(Ra+Rp)
or 
e = sqrt(1-(b²/a²))   with b the half minor axis and a the half major axis.
'''

def e(Ra,Rp):
    e = (Ra-Rp)/(Ra+Rp)
    return e

def e_V2(a,b):
    e=sqrt(1-(b**2/a**2))
    return e

## What parameters will the user enter ?

''' We absolutly need some parameters : 
- The eccentricity
- The masses
- The Half major axis

As the eccentricity can be found with Ra and Rp we can just ask these values, that can be easily understood.
Al least we must ask the value of masses.

So what the user will enter ? 
- 'a' The half major axis
- 'b' The half minor axis
- 'm' Mass of the studied object (or add it when he want to study an object)
- 'M' Mass of the massive object

With theses value we can now know we will be the studied object in the orbit.

Let's define now how to define this orbit with theses parameters.
'''

##        __
##       /  \  _ |_  . |_ 
##       \__/ |  |_) | |_ 
                  

''' To locate a position in 3D, especially a orbit, we will need three parameters : the tilt, the longitude of the ascending node and the argument of the periapsis.
Each can be found with user's entries.

Let's consider the cylindrical coordinates :
        ->     ->                                                                              ->
We call er and eθ respectively the elementary radial vector and the elementary tangent vector. ez is the elementary vector for height.
For any M point we have in the ellipse :

->     ->     ->
OM = r*er + z*ez

->          ->             ->           ->
v = (dr/dt)*er + r*(dθ/dt)*eθ + (dz/dt)*ez

->            ->                     ->                ->             ->
a = (d²r/dt²)*er + 2*(dr/dt)*(dθ/dt)*eθ + r*(dθ/dt)**2*er + (d²z/dt²)*ez
'''

## Tilt :

''' To calculate the tilt, we need to find first the orbital kinetic torque. And to find this last, we need the force exerciced on the studied object.'''

def F(M,m,r):  # Will be oriented in the contrary sens of the radial vector. So there is only a radial component.
    F=6.67408*10**-11*((m*M)/r**2)


''' The orbital kinetic torque in a O point is :1
    -------->    ->  ->              ->             ->      ->   ->      ->                                  ->
    L[orbital]= m*v ^ F = m*((dr/dt)*er + r*(dθ/dt)*eθ + (dz/dt)*ez) ^ F*er = F*m*r*(dθ/dt)*ez + F*m*(dz/dt)*eθ

      ->             
So in ez : L[orbital-z] = F*m*r*(dθ/dt)
      -> 
   in eθ : L[orbital-θ] = F*m*(dz/dt)

In this ellipse the variation of z is the sum of the altitudes (one is positive and the other is negative, or both are null) of the periapsis and the apoapsis in absolute value.
'''

# Position of the periapsis and the apoapsis :

''' We can find the position of the periapsis , it is when E=0.'''

def periapsis_position(E):


def orbital_kinetic_torque(F,r,m,E):   # It wll be orthogonal to the plan of the orbit. Here E = θ , because we found it before, this is the true anomaly.
    
