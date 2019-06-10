from direct.showbase.ShowBase import ShowBase
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.core import *
import os,ctypes
from math import *

user32 = ctypes.windll.user32
user32.SetProcessDPIAware() #windows fullscreen compatibility, fixes the getsystemmetrics bug
loadPrcFileData('', 'fullscreen true')
loadPrcFileData('','win-size '+str(user32.GetSystemMetrics(0))+' '+str(user32.GetSystemMetrics(1)))

MAINDIR=Filename.fromOsSpecific(os.getcwd())
class menu(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.intro_planet=self.loader.loadModel(MAINDIR+"/Engine/Earth2.egg")
        self.intro_planet.setPos(0,0,0)
        self.intro_planet.reparentTo(render)
        self.intro_planet.setHpr(-110,0,0)
        #camera
        self.cam.setPos(0,-70,0)

        self.disable_mouse()
        self.setBackgroundColor(0,0,0)

        dlight=render.attachNewNode(DirectionalLight('menu_plight'))
        dlight.setHpr(0,-40,0)
        render.setLight(dlight)
    
menu().run()