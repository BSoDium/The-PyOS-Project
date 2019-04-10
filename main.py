from math import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import *
from direct.showbase import DirectObject # event handling
from direct.gui.OnscreenText import OnscreenText
import os,sys
import ctypes

user32 = ctypes.windll.user32
user32.SetProcessDPIAware() #windows cross platform compatibility, fixes the getsystemmetrics bug

loadPrcFileData('', 'fullscreen true')
loadPrcFileData('','win-size '+str(user32.GetSystemMetrics(0))+' '+str(user32.GetSystemMetrics(1))) # fullscreen stuff for one monitor, for multi monitor setup try 78 79
loadPrcFileData('','window-title PyOS')
loadPrcFileData('','load-display pandagl')

class world(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        #debug
        self.debug=False
        #debug
        self.dir=Filename.fromOsSpecific(os.getcwd())
        self.timescale=10
        self.worldscale=0.1
        self.pathname = os.path.dirname(sys.argv[0]) #currently unused
        # btw I found something about energy transmition through thermal radiation. I think it uses some Boltzmann formula stuff. Link here:
        # https://fr.wikibooks.org/wiki/Plan%C3%A9tologie/La_temp%C3%A9rature_de_surface_des_plan%C3%A8tes#Puissance_re%C3%A7ue_par_la_Terre
        self.collision_solids=[] #collision related stuff - comments are useless - just RTFM
        self.light_Mngr=[]
        self.data=[[0,0,0,0,0.003,0,1,1,1,100000.00,True,[self.loader.loadModel(self.dir+"/Engine/lp_planet_0.egg"),self.loader.loadModel(self.dir+"/Engine/lp_planet_1.egg")],"lp_planet",False],
        [40,0,0,0,0.003,0,1,1,1,20.00,True,[self.loader.loadModel(self.dir+"/Engine/asteroid_1.egg")],"Ottilia",False],
        [0,70,10,0,0.005,0,0.2,0.2,0.2,40.00,True,[self.loader.loadModel(self.dir+"/Engine/asteroid_1.egg")],"Selena",False],[100,0,10,0,0,0,5,5,5,1000000,True,[self.loader.loadModel(self.dir+"/Engine/sun1.egg")],"Sun",True]] 
        # the correct reading syntax is [x,y,z,l,m,n,scale1,scale2,scale3,mass,static,[files],id,lightsource,radius] for each body - x,y,z: position - l,m,n: speed - scale1,scale2,scale3: obvious (x,y,z) - mass: kg - static: boolean - [files]: panda3d readfiles list - id: str - lightsource: boolean - radius: positive value -
        #if you want the hitbox to be correctly scaled, and your body to have reasonable proportions, your 3d model must be a 5*5 sphere, or at least have these proportions
        self.u_constant=6.67408*10**(-11) #just a quick reminder
        self.u_radius=5.25 #just what I said earlier 
        self.u_radius_margin=0.1 #a margin added to the generic radius as a safety feature (mountains and stuff, atmosphere)
        #currently unused
        self.isphere=self.loader.loadModel(self.dir+"/Engine/InvertedSphere.egg") #loading skybox structure
        self.tex=loader.loadCubeMap(self.dir+'/Engine/cubemap_#.png')

        self.orbit_lines=[] #under developement
        
        # see https://www.panda3d.org/manual/?title=Collision_Solids for further collision interaction informations
        base.graphicsEngine.openWindows()
        for c in self.data: # loading and displaying the preloaded planets and bodies
            for u in range(len(c[11])): # loading each sub-file
                c[11][u].reparentTo(self.render)
                c[11][u].setScale(c[6],c[7],c[8])
                c[11][u].setPos(c[0],c[1],c[2])
                #setting the collision solid up
            self.collision_solids.append([CollisionSphere(0,0,0,self.u_radius)]) #the radius is calculated by using the average scale + the u_radius 
            # still not working
            self.collision_solids[len(self.collision_solids)-1].append(c[11][0].attachNewNode(CollisionNode(c[12])))
            # the structure of the collision_solids list will be: [[(0,1,2),1],[(0,1,2),1],[(0,1,2),1],...]
            # asteroids and irregular shapes must be slightly bigger than their hitbox in order to avoid visual glitches
            self.collision_solids[len(self.collision_solids)-1][1].node().addSolid(self.collision_solids[len(self.collision_solids)-1][0]) #I am definitely not explaining that
            if self.debug:
                self.collision_solids[len(self.collision_solids)-1][1].show() # debugging purposes only
            print("collision: ok")
            print("placing body: done")
            if c[13]:
                self.light_Mngr.append([PointLight(c[12]+"_other")])
                self.light_Mngr[len(self.light_Mngr)-1].append(render.attachNewNode(self.light_Mngr[len(self.light_Mngr)-1][0]))
                self.light_Mngr[len(self.light_Mngr)-1][1].setPos(c[0],c[1],c[2])
                render.setLight(self.light_Mngr[len(self.light_Mngr)-1][1]) 
                self.light_Mngr.append([AmbientLight(c[12]+"_self")])
                self.light_Mngr[len(self.light_Mngr)-1][0].setColorTemperature(1000)
                self.light_Mngr[len(self.light_Mngr)-1].append(render.attachNewNode(self.light_Mngr[len(self.light_Mngr)-1][0]))
                for u in range(len(c[11])):
                    c[11][u].setLight(self.light_Mngr[len(self.light_Mngr)-1][1])
                print("lights: done")
            print("loaded new body, out: done")
        
        self.isphere.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldCubeMap)# *takes a deep breath* cubemap stuff !
        self.isphere.setTexProjector(TextureStage.getDefault(), render, self.isphere)
        self.isphere.setTexPos(TextureStage.getDefault(), 0, 0, 0)
        self.isphere.setTexScale(TextureStage.getDefault(), .5) # that's a thing...
        self.isphere.setTexture(self.tex)# Create some 3D texture coordinates on the sphere. For more info on this, check the Panda3D manual.
        self.isphere.setLightOff()
        self.isphere.setScale(10000) #hope this is enough
        self.isphere.reparentTo(self.render)
        # quick test
        self.ctrav = CollisionTraverser()
        self.queue = CollisionHandlerQueue()
        for n in self.collision_solids:
            self.ctrav.add_collider(n[1],self.queue)
        # the traverser will be automatically updated, no need to repeat this every frame
        # debugging only
        if self.debug:
            self.ctrav.showCollisions(render) 
        self.taskMgr.add(self.placement_Mngr,'frameUpdateTask')
    
    def showsimpletext(self,content,pos,scale): #shows a predefined, basic text on the screen (variable output only)
        return OnscreenText(text=content,pos=pos,scale=scale)
    
    def placement_Mngr(self,task): #main game mechanics # does not work
        self.ctrav.traverse(render)
        if self.debug:
            for intake in self.queue.getEntries():
                print(intake) #experimental, debugging purposes only
        # collision events are now under constant surveillance
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
        self.apply_update()
        return task.cont
    
    def speed_update(self,a):
        for c in range(len(self.data)): #the function updates the speed tuple accordingly
            self.data[c][3]+=self.timescale*a[c][0]
            self.data[c][4]+=self.timescale*a[c][1]
            self.data[c][5]+=self.timescale*a[c][2]
            #print(self.data[c][3],self.data[c][4],self.data[c][5],"#")    # slow (debug phase)
    
    def pos_update(self): #updates the positional coordinates
        for c in range(len(self.data)):
            self.data[c][0]+=self.timescale*self.data[c][3]
            self.data[c][1]+=self.timescale*self.data[c][4]
            self.data[c][2]+=self.timescale*self.data[c][5]
        return 0
    
    def apply_update(self): #actually moves the hole 3d stuff around
        count=0 #local counter
        for c in self.data:
            for u in range(len(c[11])):
                c[11][u].setPos(c[0],c[1],c[2])
            if c[13]:
                self.light_Mngr[count][1].setPos(c[0],c[1],c[2])
                count+=2 #we have to change the position of the pointlight, not the ambientlight
            
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
        
