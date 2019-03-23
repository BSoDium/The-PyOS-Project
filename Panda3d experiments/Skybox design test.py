from math import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import *
ConfigVariableBool('fullscreen').setValue(1)
wp=WindowProperties()
wp.setSize(1600,900)
#from direct.directbase.DirectStart import *

class core(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)
		self.scene=self.loader.loadModel("generic_planet.egg")
		self.scene.reparentTo(self.render)
		self.scene.setScale(1,1,1)
		self.scene.setPos(-8,42,0)

		self.taskMgr.add(self.Cameraspin, "SpinCameraTask") #I believe taskMgr stands for "task manager"


	def Cameraspin(self,task):
		angle_deg=task.time*6.0
		angle_rad=angle_deg*(pi/180.0)
		self.camera.setPos(20*sin(angle_rad),-20*cos(angle_rad),3)
		self.camera.setHpr(angle_deg,0,0)
		return task.cont
	
	

launch=core()
launch.run()

