from math import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import *
from panda3d.core import WindowProperties
#ConfigVariableBool('fullscreen').setValue(1)
#wp=WindowProperties()
#wp.setSize(1600,900)
#from direct.directbase.DirectStart import *

class core(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		#wp=WindowProperties()
		#wp.setSize(1600,900)
        #self.win.requestProperties(wp)
		self.scene=self.loader.loadModel("random_rock.egg")
		self.scene.reparentTo(self.render)
		self.scene.setScale(3,3,3)
		self.scene.setPos(0,0,0)
		self.taskMgr.add(self.objectspin, "SpinObjectTask")


	def objectspin(self,task):
		angle_Z=task.time*0.1
		angle_Y=task.time*0.05
		self.scene.setHpr(self.scene,0,angle_Y,angle_Z) #p stands for pitch, H for heading, and r for roll
		return task.cont
	
	

launch=core()
launch.run()

