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
        self.timescale=10
        self.pathname = os.path.dirname(sys.argv[0]) #currently unused
        self.light_Mngr=[]
        self.data=[[0,0,0,0,0,0,20,20,20,100000.00,True,self.loader.loadModel("generic_planet.egg"),"pluto",True],[40,0,0,0,0.003,0,1,1,1,20.00,True,self.loader.loadModel("asteroid_1.egg"),"Ottilia",False],[0,70,10,0,0.005,0,3,3,3,40.00,True,self.loader.loadModel("asteroid_1.egg"),"Selena",False]] # the correct reading syntax is [x,y,z,l,m,n,scale1,scale2,scale3,mass,static,file,id,lightsource] for each body - x,y,z: position - l,m,n: speed - scale1,scale2,scale3: obvious (x,y,z) - mass: kg - static: boolean - file: panda3d tupple - id: str - lightsource: boolean -
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
        self.isphere.setScale(10000) #hope this is enough
        self.isphere.reparentTo(self.render)
        self.taskMgr.add(self.placement_Mngr,'frameUpdateTask')
    
    def showsimpletext(self,content,pos,scale): #shows a predefined, basic text on the screen (variable output only)
        return OnscreenText(text=content,pos=pos,scale=scale)
    
    def placement_Mngr(self,task): #main game mechanics
        acceleration=[]
        for c in range(len(self.data)): #selects the analysed body
            var=self.data[c]
            Bdf=[0,0,0] #Bdf stands for 'bilan des forces' in french, it's the resulting acceleration
            for d in self.data[0:c]+self.data[c+1:len(self.data)-1]: #selects the body which action on the analysed body we're studying...not sure about that english sentence though
                S,M=[d[9],d[0],d[1],d[2]],[var[9],var[0],var[1],var[2]]
                temp=self.dual_a(S,M)
                Bdf=[Bdf[x]+temp[x] for x in range(3)] # list sum
            # add the result to the global save list
            acceleration.append(Bdf)
        #update the bodies' position
        self.speed_update(acceleration)
        self.pos_update()
        self.disp_update()

        return task.cont
    
    def speed_update(self,a):
        for c in range(len(self.data)): #the function updates the coordinates accordingly
            self.data[c][3]+=self.timescale*a[c][0]
            self.data[c][4]+=self.timescale*a[c][1]
            self.data[c][5]+=self.timescale*a[c][2]
            #print(self.data[c][3],self.data[c][4],self.data[c][5],"#")
    
    def pos_update(self):
        for c in range(len(self.data)):
            self.data[c][0]+=self.timescale*self.data[c][3]
            self.data[c][1]+=self.timescale*self.data[c][4]
            self.data[c][2]+=self.timescale*self.data[c][5]
    
    def disp_update(self):
        for c in self.data:
            c[11].setPos(c[0],c[1],c[2])

    def dual_a(self,S,M): #S is the "static object", the one that apply the force to the "moving" object M, S seems to contain 
        O=[]  #This will be the list with the accelerations for an object 
        d=sqrt((S[1]-M[1])**2+(S[2]-M[2])**2+(S[3]-M[3])**2)
        x=(self.u_constant*S[0]*(S[1]-M[1]))/d**2
        y=(self.u_constant*S[0]*(S[2]-M[2]))/d**2
        z=(self.u_constant*S[0]*(S[3]-M[3]))/d**2
        O.append(x)
        O.append(y)
        O.append(z)
        return O 

launch=world()
base.run()
        
