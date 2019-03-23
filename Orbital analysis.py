from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.gui.DirectGui import *
import sys


### Orbital Analysis

## Physical approach :

''' What's an orbit ? 
    It's the gravitationally curved trajectory of an object 
    The major part of orbits are supposed circulars, but to fit with reality let's consider them elliptics.
    There is severals types of orbits :  Suborbitals trajectories
                                         Escape trajectories 
    