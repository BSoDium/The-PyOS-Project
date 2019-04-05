from math import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import *
from panda3d.core import *
from direct.showbase import DirectObject # event handling
from direct.gui.OnscreenText import OnscreenText
import os,sys
from win32api import GetSystemMetrics #pywin32 package

loadPrcFileData('', 'fullscreen true')
loadPrcFileData('','win-size '+str(GetSystemMetrics(0))+' '+str(GetSystemMetrics(1))) # fullscreen stuff

class world(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.pathname = os.path.dirname(sys.argv[0]) #currently unused
        self.light_Mngr=[]
        self.data=[[0,0,0,0,0,0,3,3,3,1.3*10**22,True,self.loader.loadModel("generic_planet.egg"),"pluto",True],[10,0,0,0,100,0,1,1,1,1.02*10**18,True,self.loader.loadModel("asteroid_1.egg"),"Ottilia",False]] # the correct reading syntax is [x,y,z,l,m,n,scale1,scale2,scale3,mass,static,file,id,lightsource] for each body - x,y,z: position - l,m,n: speed - scale1,scale2,scale3: obvious (x,y,z) - mass: kg - static: boolean - file: panda3d tupple - id: str - lightsource: boolean -
        self.u_constant=6.67408*10**(-11) #just a quick reminder
        self.isphere=self.loader.loadModel("InvertedSphere.egg") #loading skybox structure
        self.tex=loader.loadCubeMap('cubemap_#.png')
        base.graphicsEngine.openWindows()
        for c in self.data:
            c[11].reparentTo(self.render)
            c[11].setScale(c[6],c[7],c[8])
            c[11].setPos(c[0],c[1],c[2])
            print("placing body: 0")
            if c[13]:
                self.light_Mngr.append([PointLight(c[12]+"_other")])
                self.light_Mngr[len(self.light_Mngr)-1].append(render.attachNewNode(self.light_Mngr[len(self.light_Mngr)-1][0]))
                self.light_Mngr[len(self.light_Mngr)-1][1].setPos(c[0],c[1],c[2])
                render.setLight(self.light_Mngr[len(self.light_Mngr)-1][1]) 
                self.light_Mngr.append([AmbientLight(c[12]+"_self")])
                self.light_Mngr[len(self.light_Mngr)-1].append(render.attachNewNode(self.light_Mngr[len(self.light_Mngr)-1][0]))
                c[11].setLight(self.light_Mngr[len(self.light_Mngr)-1][1])
                print("lights: 0")
            print("loaded new body, out: 0")
        
        self.isphere.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldCubeMap)# *takes a deep breath* cubemap stuff !
        self.isphere.setTexProjector(TextureStage.getDefault(), render, self.isphere)
        self.isphere.setTexPos(TextureStage.getDefault(), 0, 0, 0)
        self.isphere.setTexScale(TextureStage.getDefault(), .5) # that's a thing...
        self.isphere.setTexture(self.tex)# Create some 3D texture coordinates on the sphere. For more info on this, check the Panda3D manual.
        self.isphere.setLightOff()
        self.isphere.setScale(1000) #hope this is enough
        self.isphere.reparentTo(self.render)
    
    def showsimpletext(self,content,pos,scale): #shows a predefined, basic text on the screen (variable output only)
        return OnscreenText(text=content,pos=pos,scale=scale)
    

launch=world()
base.run()
        
