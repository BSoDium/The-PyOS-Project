from math import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import *
from panda3d.core import *
from direct.showbase import DirectObject # event handling
from direct.gui.OnscreenText import OnscreenText

class core(ShowBase):
	def __init__(self):
		loadPrcFileData('', 'fullscreen true')
		loadPrcFileData('','win-size 1600 900') #finalyyyyyyyyy got that f*cking fullscreen to woooork goddamit that was sooo f*cking hard to find
		ShowBase.__init__(self)
		self.ast=self.loader.loadModel("asteroid_1.egg")
		self.earth=self.loader.loadModel("generic_planet.egg")
		
		base.graphicsEngine.openWindows()
		self.ast.reparentTo(self.render)
		self.ast.setScale(1,1,1)
		self.bodyplace=(0,0,0) #positional variable, temporary
		self.ast.setPos(0,0,0) 
		self.step=0 #calculation variable, counts the number of frames passed

		self.earth.reparentTo(self.render)
		self.earth.setScale(6,6,6)
		self.earth.setPos(self.bodyplace)
		#now the lighting
		#currently under work
		self.plight1=PointLight('plight1')
		self.plight1.setColorTemperature(6500)
		self.plnp1=render.attachNewNode(self.plight1)
		self.plnp1.setPos(10,10,0)
		self.earth.setLight(self.plnp1)

		self.plight = PointLight('pointlight')
		self.plight.setColorTemperature(7000) #color defined by temperature, pretty usefull in this case
		self.plight.setAttenuation((1,0,0.001)) #see https://www.panda3d.org/manual/?title=Lighting&oldid=4737 for more info
		self.plnp = render.attachNewNode(self.plight)
		self.plnp.setPos(0,0,0)
		self.ast.setLight(self.plnp)

		#task manager stuff (further calculations will be here)
		self.taskMgr.add(self.objectspin,"objectspintask")
	
	def showsimpletext(self,content,pos,scale): #shows a predefined, basic text on the screen (variable output only)
		return OnscreenText(text=content,pos=pos,scale=scale)
	
	def temp_pos_update(self):
		self.step+=0.01
		self.bodyplace=(15*cos(self.step),15*sin(self.step),0)
		self.ast.setPos(self.bodyplace)

	def objectspin(self,task):
		self.temp_pos_update()
		self.ast.setHpr(self.ast,1,0,0) #p stands for pitch, H for heading, and r for roll, this, in particular rotates the object by 1 degree
		self.earth.setHpr(self.earth,-0.1,0,0)
		return Task.cont  
	
	

launch=core()
base.run()

