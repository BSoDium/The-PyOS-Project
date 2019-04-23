from math import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import *
from panda3d.core import *
from direct.showbase import DirectObject # event handling
from direct.gui.OnscreenText import OnscreenText
from direct.filter.CommonFilters import CommonFilters
from direct.particles.ParticleEffect import ParticleEffect

class core(ShowBase):
	def __init__(self):
		loadPrcFileData('', 'fullscreen true')
		loadPrcFileData('','win-size 1920 1080') #finalyyyyyyyyy got that f*cking fullscreen to woooork goddamit that was sooo f*cking hard to find
		ShowBase.__init__(self)
		self.ast=self.loader.loadModel("asteroid_1.egg")
		self.earth=self.loader.loadModel("generic_planet.egg")
		self.isphere=self.loader.loadModel("InvertedSphere.egg")
		self.tex=loader.loadCubeMap('cubemap_#.png')
		
		self.filters = CommonFilters(base.win, base.cam)
		
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
		self.filters.setVolumetricLighting(self.plnp1,numsamples=50,density=5.0,decay=0.98,exposure=0.05) # that part is not ready
                    
		self.p=ParticleEffect()

		self.plight = PointLight('pointlight')
		self.plight.setColorTemperature(7000) #color defined by temperature, pretty usefull in this case
		self.plight.setAttenuation((1,0,0.001)) #see https://www.panda3d.org/manual/?title=Lighting&oldid=4737 for more info
		self.plnp = render.attachNewNode(self.plight)
		self.plnp.setPos(0,0,0)
		self.ast.setLight(self.plnp)

		#cubemap stuff
		self.isphere.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldCubeMap)
		self.isphere.setTexProjector(TextureStage.getDefault(), render, self.isphere)
		self.isphere.setTexPos(TextureStage.getDefault(), 0, 0, 0)
		self.isphere.setTexScale(TextureStage.getDefault(), .5) # feeling a bit deezy...
		# Create some 3D texture coordinates on the sphere. For more info on this, check the Panda3D manual.
		self.isphere.setTexture(self.tex)
		self.isphere.setLightOff()
		self.isphere.setScale(1000) #hope this is enough
		self.isphere.reparentTo(self.render)


		#task manager stuff (further calculations will be here)
		self.taskMgr.add(self.objectspin,"objectspintask")
	
	def loadParticleConfig(self, filename):
        # Start of the code from steam.ptf
		self.p.cleanup()
        self.p = ParticleEffect()
        self.p.loadConfig(Filename(filename))
        # Sets particles to birth relative to the teapot, but to render at
        # toplevel
        self.p.start(self.t)
        self.p.setPos(3.000, 0.000, 2.250)
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

		self.loadParticleConfig('smoke.ptf')
		return Task.cont  
	
	

launch=core()
base.run()

