from math import *
import os,sys,random
try:
    from direct.showbase.ShowBase import ShowBase
    from direct.task import Task
    from panda3d.core import *
    from direct.showbase import DirectObject # event handling
    from direct.gui.OnscreenText import OnscreenText
    from direct.filter.CommonFilters import CommonFilters
except:
    sys.exit("please install library panda3d: pip install panda")
import ctypes

user32 = ctypes.windll.user32
user32.SetProcessDPIAware() #windows cross platform compatibility, fixes the getsystemmetrics bug
fullscreen=True
if fullscreen:
    loadPrcFileData('', 'fullscreen true')
    loadPrcFileData('','win-size '+str(user32.GetSystemMetrics(0))+' '+str(user32.GetSystemMetrics(1))) # fullscreen stuff for one monitor, for multi monitor setup try 78 79
loadPrcFileData('','window-title PyOS')
loadPrcFileData('','load-display pandagl')
loadPrcFileData('','basic-shaders-only #f') # is that useful? 
loadPrcFileData("", "textures-power-2 none")

class world(ShowBase):
    def __init__(self):
        try:
            ShowBase.__init__(self)
        except:
            sys.exit(":( something went wrong: error while loading OpenGL")
        #debug
        self.debug=False #REMEMBER TO TURN THIS OFF WHEN COMMITTING THIS TO GITHUB YOU GODDAM MORRON !!!
        #debug
        self.dir=Filename.fromOsSpecific(os.getcwd())
        self.timescale=10
        self.worldscale=0.1 # currently unused

        self.state=['paused'] # state of things
        self.iteration=0 #iteraton for the menu to be drawn once
        # preparing the menu text list:
        self.menu_text=[]
        self.menu_text.append(self.showsimpletext('The PyOS project V0.5',(0,0.4),(0.07,0.07),None,(1,1,1,True)))
        self.menu_text.append(self.showsimpletext('Resume',(0,0.3),(0.06,0.06),None,(1,1,1,True)))
        self.menu_text.append(self.showsimpletext('Quit',(0,0.2),(0.06,0.06),None,(1,1,1,True)))

        self.collision_status=False # Keep this on False, that's definitely not a setting # currently unused
        # btw I found something about energy transmition through thermal radiation. I think it uses some Boltzmann formula stuff. Link here:
        # https://fr.wikibooks.org/wiki/Plan%C3%A9tologie/La_temp%C3%A9rature_de_surface_des_plan%C3%A8tes#Puissance_re%C3%A7ue_par_la_Terre
        self.sounds=[self.loader.loadSfx(self.dir+"/Sound/001.mp3"),self.loader.loadSfx(self.dir+"/Sound/002.mp3"),self.loader.loadSfx(self.dir+"/Sound/003.mp3"),self.loader.loadSfx(self.dir+"/Sound/004.mp3"),self.loader.loadSfx(self.dir+"/Sound/005.mp3")] #buggy
        self.collision_solids=[] #collision related stuff - comments are useless - just RTFM
        self.light_Mngr=[]
        self.data=[[0,0,0,0,0.003,0,1,1,1,100000.00,True,[self.loader.loadModel(self.dir+"/Engine/lp_planet_0.egg"),(0.1,0,0),self.loader.loadModel(self.dir+"/Engine/lp_planet_1.egg"),(0.14,0,0)],"lp_planet",False],
        [40,0,0,0,0.003,0,0.5,0.5,0.5,20.00,True,[self.loader.loadModel(self.dir+"/Engine/Icy.egg"),(0.5,0,0)],"Ottilia",False],
        [0,70,10,0,0.005,0,0.2,0.2,0.2,40.00,True,[self.loader.loadModel(self.dir+"/Engine/asteroid_1.egg"),(0,0,0.2)],"Selena",False],[100,0,10,0,0,0,5,5,5,1000000,True,[self.loader.loadModel(self.dir+"/Engine/sun1.egg"),(0.01,0,0),self.loader.loadModel(self.dir+"/Engine/sun1_atm.egg"),(0.01,0,0)],"Sun",True]] 
        # the correct reading syntax is [x,y,z,l,m,n,scale1,scale2,scale3,mass,static,[file,(H,p,r),file,(H,p,r)...],id,lightsource,radius] for each body - x,y,z: position - l,m,n: speed - scale1,scale2,scale3: obvious (x,y,z) - mass: kg - static: boolean - [files]: panda3d readfiles list - id: str - lightsource: boolean - radius: positive value -
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
        try:
            # filters predefining
            self.filters = CommonFilters(base.win, base.cam)
            '''
            self.filters.setBlurSharpen(amount=0) # just messing around
            '''

            self.filters.set_bloom(intensity=1,size="large")
            

            for c in self.data: # loading and displaying the preloaded planets and bodies
                for u in range(0,len(c[11]),2): # loading each sub-file
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
                    # filters
                    
                    #self.filters.setVolumetricLighting(c[11][0],numsamples=32,density=5.0,decay=0.98,exposure=0.05) # that part is not ready

                    self.light_Mngr.append([AmbientLight(c[12]+"_self")])
                    self.light_Mngr[len(self.light_Mngr)-1][0].setColorTemperature(1000)
                    self.light_Mngr[len(self.light_Mngr)-1].append(render.attachNewNode(self.light_Mngr[len(self.light_Mngr)-1][0]))
                    for u in range(0,len(c[11]),2):
                        c[11][u].setLight(self.light_Mngr[len(self.light_Mngr)-1][1])
                    print("lights: done")
                print("loaded new body, out: done")
            self.isphere.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldCubeMap)  # *takes a deep breath* cubemap stuff !
            self.isphere.setTexProjector(TextureStage.getDefault(), render, self.isphere)
            self.isphere.setTexPos(TextureStage.getDefault(), 0, 0, 0)
            self.isphere.setTexScale(TextureStage.getDefault(), .5) # that's a thing...
            self.isphere.setTexture(self.tex)# Create some 3D texture coordinates on the sphere. For more info on this, check the Panda3D manual.
            self.isphere.setLightOff()
            self.isphere.setScale(10000) #hope this is enough
            self.isphere.reparentTo(self.render)
            # collision traverser and other collision stuff # that's super important, and super tricky to explain so just check the wiki
            self.ctrav = CollisionTraverser()
            self.queue = CollisionHandlerQueue()
            for n in self.collision_solids:
                self.ctrav.add_collider(n[1],self.queue)
            # the traverser will be automatically updated, no need to repeat this every frame
            # debugging only
            if self.debug:
                self.ctrav.showCollisions(render) 
            # play a random music
            self.current_playing=random.randint(0,len(self.sounds)-1)
            self.sounds[self.current_playing].play()
            # task manager stuff comes here
            self.taskMgr.add(self.mouse_check,'mousePositionTask')
            self.taskMgr.add(self.placement_Mngr,'frameUpdateTask')
            self.taskMgr.add(self.Sound_Mngr,'MusicHandle')
        except:
            sys.exit(":( something went wrong: 3d models could not be loaded")
        
        '''
        self.showsimpletext("All modules loaded, simulation running",(-1.42,0.95),(0.04,0.04),None,(1,1,1,True))
        self.showsimpletext("PyOS experimental build V0.4",(-1.5,0.90),(0.04,0.04),None,(1,1,1,True))
        self.showsimpletext("By l3alr0g",(-1.68,0.85),(0.04,0.04),None,(1,1,1,True))
        '''
        
        # key bindings
        self.accept('escape',self.toggle_pause)
        self.accept('z',self.move_camera,[0])
        self.accept('q',self.move_camera,[1])
        self.accept('s',self.move_camera,[2])
        self.accept('d',self.move_camera,[3])
    
    def showsimpletext(self,content,pos,scale,bg,fg): #shows a predefined, basic text on the screen (variable output only)
        return OnscreenText(text=content,pos=pos,scale=scale,bg=bg,fg=fg)
    
    def placement_Mngr(self,task): # main game mechanics, frame updating function (kinda, all pausing and menu functions must be applied here
        if self.state[0]=='running' or not task.time:
            self.ctrav.traverse(render)
            #self.queue = CollisionHandlerQueue() # update the collision queue
            if self.queue.getNumEntries():
                if self.debug:
                    print(self.queue.getNumEntries()) # debug
                for c in range(0,len(self.queue.getEntries()),2):
                    # print(entry)#experimental, debugging purposes only
                    #print(entry.getInteriorPoint(entry.getIntoNodePath()))# we have to run a collision check for each couple
                    self.collision_log(self.queue.getEntries()[c])
                # print "out"
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
        elif self.state[0]=='paused':
            self.handle_menu(self.iteration)
            self.iteration+=1
        return task.cont
    
    def speed_update(self,a):
        for c in range(len(self.data)): #the function updates the speed tuple accordingly
            self.data[c][3]+=self.timescale*a[c][0]
            self.data[c][4]+=self.timescale*a[c][1]
            self.data[c][5]+=self.timescale*a[c][2]
            #print(self.data[c][3],self.data[c][4],self.data[c][5],"#")    # slow (debug phase)
        return 0
    
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
                if u%2!=0:
                    c[11][u-1].setHpr(c[11][u-1],c[11][u])
                else:    
                    c[11][u].setPos(c[0],c[1],c[2])    
            if c[13]:
                self.light_Mngr[count][1].setPos(c[0],c[1],c[2])
                count+=2 #we have to change the position of the pointlight, not the ambientlight
        return 0
            
    def dual_a(self,S,M): #S is the "static object", the one that applies the force to the "moving" object M
        O=[]  #This will be the list with the accelerations for an object 
        d=sqrt((S[1]-M[1])**2+(S[2]-M[2])**2+(S[3]-M[3])**2)
        x=(self.u_constant*S[0]*(S[1]-M[1]))/d**2
        y=(self.u_constant*S[0]*(S[2]-M[2]))/d**2
        z=(self.u_constant*S[0]*(S[3]-M[3]))/d**2
        O.append(x)
        O.append(y)
        O.append(z)
        return O 
    
    def collision_log(self,entry):
        from_pos=[self.data[n][11][0] for n in range(len(self.data))].index(entry.getFromNodePath().getParent())
        into_pos=[self.data[n][11][0] for n in range(len(self.data))].index(entry.getIntoNodePath().getParent()) #find the nodepath in the list
        f_radius=(self.data[from_pos][6]+self.data[from_pos][7]+self.data[from_pos][8])*self.u_radius/3
        i_radius=(self.data[into_pos][6]+self.data[into_pos][7]+self.data[into_pos][8])*self.u_radius/3
        if max(f_radius,i_radius)==f_radius:
            into_pos,from_pos=from_pos,into_pos
        # those are the two positions of the nodepaths, now we need to know which one is bigger, in order to obtain the fusion effect
        # from_pos is the smaller body, into_pos is the bigger one
        self.collision_gfx(self.momentum_transfer(from_pos,into_pos,entry),f_radius,i_radius)
        return 0
    
    def momentum_transfer(self,f_pos,i_pos,entry):
        if self.debug:
            print("colliding") # debug, makes the game laggy
        #that part is completely fucked up
        interior = entry.getInteriorPoint(entry.getIntoNodePath())
        surface = entry.getSurfacePoint(entry.getIntoNodePath())
        if (interior - surface).length() >= 2*(self.data[f_pos][6]+self.data[f_pos][7]+self.data[f_pos][8])*self.u_radius/3:
            #Here's Johny
            for c in range(0,len(self.data[f_pos][11]),2):
                self.ctrav.remove_collider(self.collision_solids[f_pos][1])
                #self.collision_solids[f_pos][1].node().removeSolid()
                #self.collision_solids[f_pos][1]=None
                self.data[f_pos][11][c].removeNode()
                #self.data[f_pos][11][c]=None
            
            self.data[i_pos][6],self.data[i_pos][7],self.data[i_pos][8]=self.data[i_pos][6]*(self.data[i_pos][9]+self.data[f_pos][9])/self.data[i_pos][9],self.data[i_pos][7]*(self.data[i_pos][9]+self.data[f_pos][9])/self.data[i_pos][9],self.data[i_pos][8]*(self.data[i_pos][9]+self.data[f_pos][9])/self.data[i_pos][9]
            self.data[i_pos][9]+=self.data[f_pos][9]
            # scale updating ()
            for c in range(0,len(self.data[i_pos][11]),2):
                self.data[i_pos][11][c].setScale(self.data[i_pos][6],self.data[i_pos][7],self.data[i_pos][8])
            # deleting the destroyed planet's data, it is not fully functionnal as the other models remain intact
            self.data=self.data[:f_pos]+self.data[f_pos+1:len(self.data)]
            self.collision_solids=self.collision_solids[:f_pos]+self.collision_solids[f_pos+1:len(self.collision_solids)]
            # just a quick test
            self.ctrav.clear_colliders()
            self.queue = CollisionHandlerQueue()
            for n in self.collision_solids:
                self.ctrav.add_collider(n[1],self.queue)
            if self.debug:
                self.ctrav.showCollisions(render) 
            # update the queue (simple test actually) -edit- it works
            if self.debug:
                print("planet destroyed")
        return interior,surface # used for the collision gfx calculations
    
    def printScene(self):  #debug
        file=open("scenegraph.txt","a")
        ls = LineStream()
        render.ls(ls)
        while ls.isTextAvailable():
            file.write(ls.getLine())
            file.write("\n")
        file.write("\n")
        file.write("END\n")
        file.write("\n")
        file.close()
    
    def Sound_Mngr(self,task):
        if self.sounds[self.current_playing].length()-self.sounds[self.current_playing].getTime()==0: #could have just used not()
            self.current_playing=random.choice(list(range(0,self.current_playing))+list(range(self.current_playing+1,len(self.sounds))))
            self.sounds[self.current_playing].play()
        return task.cont

    def collision_gfx(self,points,Rf,Ri):
        # section size calculation
        # we know the depth of penetration (no silly jokes please), which allows us, knowing the radius of each body, 
        # to calculate the radius of the section (I've got no idea how to say that in correct english)
        # the display of the particles all over this circle will be a piece of cake (at least I hope so)
        # see documents in the screenshot folder for more informations about the maths
        interior,surface=points[0],points[1]
        p=(interior - surface).length()
        p2=(p**2-2*Ri*p)/(2*Ri-2*p-2*Rf)
        p1=p-p2
        # now we know everything about our impact section (the circle that defines the contact between the two bodies)
        # we just have to find the coord of the circle's center 
         
        return 0

    def create_crater(self):
        return None

    def toggle_pause(self):
        temp=['paused','running']
        self.state[0]=temp[self.state[0]==temp[0]] # switches between paused and running
        self.iteration=0
        if self.state[0]=='paused':
            self.handle_menu(self.iteration)
        else:
            self.filters.del_blur_sharpen()
            for u in self.menu_text:
                u.hide()
        return None
    
    def handle_menu(self,iteration):
        if not iteration:
            self.draw_menu()
        else:
            self.accept('escape',self.toggle_pause)
            #put your mouse detection stuff here
        return None
    
    def draw_menu(self):
        self.filters.setBlurSharpen(amount=0)
        for u in self.menu_text:
                u.show()
        return None
    
    def show_credits(self):
        return "created by l3alr0g (at least this part, I'll do something better at the end)"
        
    def system_break(self):
        # place your data saving routines here
        print("system exit successful, data saved")
        print("executing sys.exit()")
        print("out: done")
        sys.exit(0)
        return None
    
    def rotate_camera(self):
        return None
    
    def move_camera(self,tow): # tow stands for towards
        print(tow)
        return None
    
    def mouse_check(self,task): # returns the mouse's coordinates
        return None
    
    def answer_click(self):
        return None
    
    def easter_egg(self):
        return "please be patient, hens are working on it"
    

launch=world()
base.run()
        

