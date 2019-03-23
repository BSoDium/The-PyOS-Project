from direct.showbase.ShowBase import ShowBase
base = ShowBase()
from panda3d.core import *
from direct.gui.DirectGui import *
import sys
bite=15000000

class Loading(object):
    def __init__(self):
        self.title = OnscreenText(
            text="Python Orbital Mechanics",
            parent=base.a2dBottomCenter, align=TextNode.A_right,
            style=3, fg=(1, 1, 1, 1), pos=(0.1,0.1), scale= 0.07)
        
        base.setBackgroundColor(0, 0, 0)
        camera.setPos(0, 0, 45)
        camera.setHpr(0, -90, 0)


class Core(object): # main class
    def __init__(self): # just building the object
        self.timescale=1
        self.lightspeed=299792458
        self.gravityconstant=0.0000000000667408
        # self.load_assets()
    class Planet(object,mass,name,radius,rspeed,id):
        def __init__(self):
            self.mass=mass
            self.name=name
            self.radius=radius
            self.rspeed=rspeed
            self.kind=id
            

    #def load_assets():


l=Loading()
c=Core()
base.run()
