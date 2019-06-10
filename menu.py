from direct.showbase.ShowBase import ShowBase
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.core import *
import os,ctypes
from math import *
from direct.filter.CommonFilters import CommonFilters
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectGui import *
import sys

user32 = ctypes.windll.user32
user32.SetProcessDPIAware() #windows fullscreen compatibility, fixes the getsystemmetrics bug
'''
loadPrcFileData('', 'fullscreen true')
loadPrcFileData('','win-size '+str(user32.GetSystemMetrics(0))+' '+str(user32.GetSystemMetrics(1)))
'''

loadPrcFileData('','framebuffer-multisample 1')
loadPrcFileData('','multisamples 2')

MAINDIR=Filename.fromOsSpecific(os.getcwd())
class menu(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # filters

        self.filters = CommonFilters(base.win, base.cam)
        render.setAntialias(AntialiasAttrib.MAuto)

        # Rajout :

        def quit():
            sys.exit(0)
        
        maps_start=loader.loadModel(MAINDIR+'/Engine/start.egg')
        maps_quit=loader.loadModel(MAINDIR+'/Engine/quit.egg')
        self.start_button=DirectButton(pos=(0,0.35,0.60),frameColor=(0,0,0,0),scale=(0.4,0.4,0.1368),geom=(maps_start.find('**/Start'),maps_start.find('**/Start_push'),maps_start.find('**/Start_on'),maps_start.find('**/Start')))
        self.quit_button=DirectButton(pos=(0,0.35,0.45),frameColor=(0,0,0,0),scale=(0.4,0.4,0.1368),geom=(maps_quit.find('**/Quit'),maps_quit.find('**/Quit_push'),maps_quit.find('**/Quit_on'),maps_quit.find('**/Quit')),command=quit)

        # Fin du rajout :

        self.moon=self.loader.loadModel(MAINDIR+"/Engine/Icy.egg")
        self.moon.setScale(9,9,9)
        self.moon.setPos(0,-63,-46.5)
        self.moon.reparentTo(render)
        self.intro_planet=self.loader.loadModel(MAINDIR+"/Engine/Earth2.egg")
        self.intro_planet.setPos(0,0,0)
        self.intro_planet.reparentTo(render)
        self.intro_planet.setHpr(-110,0,0)
        
        #self.star_pic=OnscreenImage(image=MAINDIR+'/Engine/Stars.png',scale=(1))
        #camera
        self.cam.setPos(0,-70,0)

        self.disable_mouse()
        self.setBackgroundColor(0,0,0)

        dlight=render.attachNewNode(DirectionalLight('menu_plight'))
        dlight.setHpr(0,-40,0)
        render.setLight(dlight)

        self.task_mgr.add(self.rotate,'rotationtask')
        

    def rotate(self,task):
        self.intro_planet.setHpr(self.intro_planet,(0.1,0,0))
        self.moon.setHpr(self.moon,(0,0.01,0))
        return task.cont





menu().run()