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

def true_anomaly(E,e):   # E = average anomaly, e = eccentricity
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


''' Thanks all others functions we can determine for a 't' time, the value or the distance between the object and its center. :
We have a r(E) relation, but also a E(t) relation so a r(E(t)) relation , a is the half major axis again'''

def r(E,a,e):
        r=a*(1-e*cos(E))
        return r


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
- 'v0' The inital speed

With theses value we can now know we will be the studied object in the orbit.

Let's define now how to define this orbit with theses parameters.
'''

##        __
##       /  \  _ |_  . |_ 
##       \__/ |  |_) | |_ 
                  

''' To locate a position in 3D, especially a orbit, we will need two parameters : the tilt and the argument of the periapsis.
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
    -------->   ->  ->      ->            ->             ->           ->                     ->               ->
    L[orbital]= F ^ mv  = F*er m*((dr/dt)*er + r*(dθ/dt)*eθ + (dz/dt)*ez) ^  = F*m*r*(dθ/dt)*ez - F*m*(dz/dt)*eθ

      ->             
So on ez : L[orbital-z] = F*m*r*(dθ/dt)
      -> 
   on eθ : L[orbital-θ] = -F*m*(dz/dt)

'''

'''Find the initial orbital kentic torque, it won't change, find the tilt by calculating the angle between the initial orbital kinetic torque and the ecuador plan. Then remove 90°
and we will find what we wanted.'''

# We will search the z-component of Lo(M) which is the orbital kinetic torque at a M point.   

def inital_orbital_kinetic_torque(F,m,vo): # v0 is the inital speed, it will be entered by the user. 
        #Lo(M)=F^m*v
        #    ->
        # on ez : Lzo(M)=F*m*r*(dθ/dt) = F*m*r*Ω = F*m*v      # Where Ω is the angular speed , v=Ω*r
        L=F*m*v0
        return L


''' Let's find now the argument of the periapsis :

We will name ω the argument of the periapsis, which can be found thanks :
ω = arccos((n*e)/|n|*|e|)
Where n is a vector pointing towards the ascending node and e the eccentricity vector pointing towards the periapsis.
'''