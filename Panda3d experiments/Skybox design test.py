from math import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import *
from panda3d.core import WindowProperties
from direct.showbase import DirectObject # event handling
import os

#ConfigVariableBool('fullscreen').setValue(1)
#wp=WindowProperties()
#wp.setSize(1600,900)
#from direct.directbase.DirectStart import *

class core(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		self.scene=self.loader.loadModel("random_rock.egg")
		wp = WindowProperties()
		wp.setFullscreen(1)
		wp.setSize(1920, 1080)
		Z=0
		Y=0
		base.openMainWindow()
		base.win.requestProperties(wp)
		base.graphicsEngine.openWindows()
		self.scene.reparentTo(self.render)
		self.scene.setScale(3,3,3)
		self.scene.setPos(0,0,0)
		self.objectspin(Z,Y)

	def objectspin(self,angle_Z,angle_Y):
		angle_Z+=1
		angle_Y+=0.05
		self.scene.setHpr(self.scene,0,angle_Y,angle_Z) #p stands for pitch, H for heading, and r for roll
		return 0
	
	

launch=core()
base.run()

