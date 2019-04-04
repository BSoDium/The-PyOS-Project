from math import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import *
from panda3d.core import *
from direct.showbase import DirectObject # event handling
from direct.gui.OnscreenText import OnscreenText
loadPrcFileData('', 'fullscreen true')
loadPrcFileData('','win-size 1600 900') 
#finalyyyyyyyyy got that f*cking fullscreen to woooork goddamit that was sooo f*cking hard to find

class core(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		self.ast=self.loader.loadModel("random_rock.egg")
		self.sun=self.loader.loadModel("low_poly_planet.egg")
		
		base.openMainWindow()
		base.graphicsEngine.openWindows()
		self.ast.reparentTo(self.render)
		self.ast.setScale(1,1,1)
		self.bodyplace=(0,0,0) #positional variable
		self.ast.setPos(0,0,0) 
		self.step=0 #calculation variable, counts the number of frames passed

		self.sun.reparentTo(self.render)
		self.sun.setScale(1,1,1)
		self.sun.setPos(self.bodyplace)
		#now the lighting
		#currently under work
		
		self.plight = PointLight('pointlight')
		self.plight.setColorTemperature(700) #color defined by temperature, pretty usefull in this case
		self.plight.setAttenuation((1,0,1)) #see https://www.panda3d.org/manual/?title=Lighting&oldid=4737 for more info
		self.plnp = render.attachNewNode(self.plight)
		self.plnp.setPos(0,0,0)
		self.ast.setLight(self.plnp)
		
		#task manager stuff (further calculations will be here)
		self.angle_Y=0
		self.angle_Z=0
		self.taskMgr.add(self.objectspin,"objectspintask")
	
	def showsimpletext(self,content,pos,scale): #shows a predefined, basic text on the screen (variable output only)
		return OnscreenText(text=content,pos=pos,scale=scale)
	
	def temp_pos_update(self):
		self.step+=0.01
		self.bodyplace=(7*cos(self.step),7*sin(self.step),0)
		self.ast.setPos(self.bodyplace)

	def objectspin(self,task):
		self.temp_pos_update()
		try:
			self.angle_Y+=0.01
		except:
			pass
		render.setLight(self.plnp)
		self.ast.setHpr(self.ast,0,0,0) #p stands for pitch, H for heading, and r for roll
		return Task.cont  
	
	

launch=core()
base.run()

