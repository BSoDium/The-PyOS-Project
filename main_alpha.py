from math import *
import os,sys,random,time
try:
    from direct.showbase.ShowBase import ShowBase
    from direct.task import Task
    from panda3d.core import *
    from direct.showbase import DirectObject # event handling
    from direct.gui.OnscreenText import OnscreenText
    from direct.showbase.DirectObject import DirectObject
    from direct.gui.DirectGui import *
    from direct.filter.CommonFilters import CommonFilters
    from direct.gui.OnscreenImage import OnscreenImage
    from direct.particles.ParticleEffect import ParticleEffect
except:
    sys.exit("please install library panda3d: pip install panda")
import ctypes

try:
    from pypresence import Presence # discord presence
except:
    sys.exit("pypresence module missing")

from PyOS_mod import body,hitbox,particle


# discord stuff -------------------------------
client_id = '591299679409668098' #bot id
RPC = Presence(client_id)
RPC.connect()
log=RPC.update(state="Version: 0.10-alpha", details="Crashing planets")

print(log)
# discord presence is now active -------

user32 = ctypes.windll.user32
user32.SetProcessDPIAware() #windows fullscreen compatibility, fixes the getsystemmetrics bug
fullscreen=True
if fullscreen:
    loadPrcFileData('', 'fullscreen true') 
    loadPrcFileData('','win-size '+str(user32.GetSystemMetrics(0))+' '+str(user32.GetSystemMetrics(1))) # fullscreen stuff for one monitor, for multi monitor setup try 78 79
loadPrcFileData('','window-title PyOS')
loadPrcFileData('','load-display pandagl')
#loadPrcFileData('','basic-shaders-only #f') # is that useful? 
loadPrcFileData('', 'textures-power-2 none')
# Antialiasing
loadPrcFileData('','framebuffer-multisample 1')
loadPrcFileData('','multisamples 2') 

SKYBOX='sky'
BLUR=False # debug
MAINDIR=Filename.fromOsSpecific(os.getcwd())

class state(DirectObject):
    def __init__(self):
        super().__init__()
        self.root_node=NodePath('State Root')
        self.root_node.reparentTo(base.render)
        return None
    
    def cleanup(self):
        self.ignoreAll()
        self.root_node.remove_node()
        self.root_node=None
        self.root_node=NodePath('State Root')
        self.root_node.reparentTo(base.render)
        return None




class world(ShowBase):
    def __init__(self):
        try:
            ShowBase.__init__(self)
        except:
            sys.exit("something went wrong: error while loading ShowBase")
        
        
        # ------------------------------- Begin of parameter variables (pretty messy actually) ------------------------------------
        #debug ------
        self.debug=False #REMEMBER TO TURN THIS OFF WHEN COMMITTING THIS TO GITHUB YOU GODDAM MORRON !!!
        #debug ------

        self.stored_collision_count=0 # this counts the amount of collisions and allows us to detect the income of a new collision in order to create a new particle effect when it appears
        
        self.timescale=5 # this can be changed at any moment, it represents the speed of the ingame time
        self.worldscale=0.1 # currently unused
        
        self.camera_delta=0.5 # camera delta displacement
        self.sensitivity_x,self.sensitivity_y=20,20
        self.watched=None # watched object (object focused by the cursor)
        
        self.state=['paused','free',None] # state of things: [simulation paused/running,camera following object/free,followed object/None]
        print('free mode on')
        self.iteration=0 #iteration for the menu to be drawn once
        self.collision_status=False # Keep this on False, that's definitely not a setting # currently unused

        self.u_constant=6.67408*10**(-11) #just a quick reminder
        self.u_radius=5 #just what I said earlier 
        
        # ------------------------------- End of parameter variables (sry for the mess) --------------------------------------------
        

        self.Game_state=state()
        self.taskMgr.add(self.wait,'wait_task')
        self.setBackgroundColor(0,0,0)
        
    def wait(self,task):
        if not(task.time):
            self.screen_fill=OnscreenImage(image=str(MAINDIR)+"/Engine/main_page.png",pos = (0, 0, 0),scale=(1.77777778,1,1))
        elif task.time>4:
            self.taskMgr.remove('wait_task')
            self.screen_fill.destroy()
            self.menu()
            return None
        return task.cont


    def menu(self):
        # loading time
        # music
        self.menu_music=self.loader.loadSfx(str(MAINDIR)+'/Sound/deadmau5-cabin.mp3')
        self.menu_music.setLoop(True)
        self.menu_music.play()
        # filters
        self.filters = CommonFilters(base.win, base.cam)
        self.Game_state.root_node.setAntialias(AntialiasAttrib.MAuto)
        def quit():
            sys.exit(0)
        maps_start=loader.loadModel(str(MAINDIR)+'/Engine/start.egg')
        maps_quit=loader.loadModel(str(MAINDIR)+'/Engine/quit.egg')
        self.start_button=DirectButton(pos=(0,0.35,0.60),frameColor=(0,0,0,0),scale=(0.4,0.4,0.1368),geom=(maps_start.find('**/Start'),maps_start.find('**/Start_push'),maps_start.find('**/Start_on'),maps_start.find('**/Start')),command=self.loadgame)
        self.quit_button=DirectButton(pos=(0,0.35,0.45),frameColor=(0,0,0,0),scale=(0.4,0.4,0.1368),geom=(maps_quit.find('**/Quit'),maps_quit.find('**/Quit_push'),maps_quit.find('**/Quit_on'),maps_quit.find('**/Quit')),command=quit)
        self.title_pic=OnscreenImage(image=str(MAINDIR)+'/Engine/title.png',pos=(0,0.35,0.80), scale=(1,1,0.0504))
        self.title_pic.setTransparency(TransparencyAttrib.MAlpha)
        self.activity_log=OnscreenImage(image=str(MAINDIR)+'/Engine/activity_log.png',pos=(-1.2,0.35,0.3),scale=(0.375,0.75,0.086775))
        self.activity_log.setTransparency(TransparencyAttrib.MAlpha)
        self.activity_log_bg=OnscreenImage(image=str(MAINDIR)+'/Engine/activity_log_bg.png',pos=(-1.2,-0.35,-0.3),scale=(0.5,0.4,0.675))
        self.activity_log_bg.setTransparency(TransparencyAttrib.MAlpha)
        #spaces compensate the center text effect
        self.logs=OnscreenText(text='   PyOS v0.10-alpha\n\n                              Added main menu in last update\n                                             Particle support has now become reality\n                                  but still needs some improvement\n\n\n          Feature in progress:\n      collision animation\n\n\nRelease date >>',pos=(-1.5,0.11,0), scale=(0.05,0.05,0.05),fg=(1,1,1,1))
        self.shrug=OnscreenImage(image=str(MAINDIR)+'/Engine/shrug.png',pos=(-1.55,0.35,-0.5),scale=(0.1,1,0.0317))
        self.shrug.setTransparency(TransparencyAttrib.MAlpha)

        self.backgrnd=OnscreenImage(image=str(MAINDIR)+'/Engine/Stars.png',scale=(1.78,1,1))
        self.backgrnd.setHpr(0,0,0)
        self.backgrnd.reparentTo(self.Game_state.root_node)
        self.backgrnd.setPos(0,0,0)
        self.moon=self.loader.loadModel(str(MAINDIR)+"/Engine/Icy.egg")
        self.moon.setScale(9,9,9)
        self.moon.setPos(0,-63,-46.5)
        self.moon.reparentTo(self.Game_state.root_node)
        self.intro_planet=self.loader.loadModel(str(MAINDIR)+"/Engine/tessena.egg")
        self.intro_planet_atm=self.loader.loadModel(str(MAINDIR)+"/Engine/tessena_atm.egg")
        self.intro_planet.setPos(0,0,0)
        self.intro_planet_atm.setPos(0,0,0)
        self.intro_planet.reparentTo(self.Game_state.root_node)
        self.intro_planet_atm.reparentTo(self.Game_state.root_node)
        self.intro_planet.setHpr(-110,0,0)
        self.intro_planet_atm.setHpr(-110,0,0)
        self.cam.setPos(0,-70,0)

        self.disable_mouse()
        # lighting
        dlight=self.Game_state.root_node.attachNewNode(DirectionalLight('menu_plight'))
        dlight.setHpr(0,-40,0)
        self.moon.setLight(dlight)
        self.intro_planet.setLight(dlight)
        self.intro_planet_atm.setLight(dlight)

        self.task_mgr.add(self.rotate,'rotationtask') # penser a l'enlever

        
    
    def rotate(self,task):
        self.intro_planet.setHpr(self.intro_planet,(0.1,0,0))
        self.intro_planet_atm.setHpr(self.intro_planet_atm,(0.07,0,0))
        self.moon.setHpr(self.moon,(0,0.01,0))
        return task.cont
    
    # end of menu subfunctions


    def loadgame(self):
        # transition phase
        self.menu_music.setLoop(False)
        self.menu_music.stop()
        
        
        self.taskMgr.remove('rotationtask')
        self.cam.setPos(0,0,0)
        self.Game_state.cleanup()
        self.activity_log.hide()
        self.activity_log_bg.hide()
        self.logs.hide()
        self.shrug.hide()
        self.start_button.hide()
        self.quit_button.hide()
        self.title_pic.hide()
        
        

        # end of transition phase

        # Mouse parameters 
        self.hidden_mouse=True
        wp = WindowProperties()
        wp.setCursorHidden(self.hidden_mouse)
        self.win.requestProperties(wp)

        # preparing the menu text list:
        self.menu_text=[]
        self.menu_text.append(self.showsimpletext('The PyOS project V0.10 alpha',(0,0.4),(0.07,0.07),None,(1,1,1,True)))
        self.menu_text.append(self.showsimpletext('Game Paused',(0,0.3),(0.06,0.06),None,(1,1,1,True)))

        # btw I found something about energy transmission through thermal radiation. I think it uses some Boltzmann formula stuff. Link here:
        # https://fr.wikibooks.org/wiki/Plan%C3%A9tologie/La_temp%C3%A9rature_de_surface_des_plan%C3%A8tes#Puissance_re%C3%A7ue_par_la_Terre

        # Defining important data lists
        # music imports (paths)
        self.sounds=[str(MAINDIR)+"/Sound/001.mp3",
        str(MAINDIR)+"/Sound/Blazing-Stars.mp3",
        str(MAINDIR)+"/Sound/Cold-Moon.mp3",
        str(MAINDIR)+"/Sound/Light-Years_v001.mp3",
        str(MAINDIR)+"/Sound/The-Darkness-Below.mp3",
        str(MAINDIR)+"/Sound/Retro-Sci-Fi-Planet.mp3",
        str(MAINDIR)+"/Sound/droid-bishop-nightland.mp3",
        str(MAINDIR)+"/Sound/interstellar-ost-03-dust-by-hans-zimmer.mp3",
        str(MAINDIR)+"/Sound/interstellar-ost-04-day-one-by-hans-zimmer.mp3",
        str(MAINDIR)+"/Sound/ascendant-remains-2015.mp3",
        str(MAINDIR)+"/Sound/droid-bishop-nightland.mp3",
        str(MAINDIR)+"/Sound/john-carpenter-utopian-facade-official-music-video.mp3",
        str(MAINDIR)+"/Sound/stranger-things-2-eulogy.mp3",
        str(MAINDIR)+"/Sound/interstellar-ost-07-the-wormhole-by-hans-zimmer.mp3"] 
        
        self.collision_solids=[] #collision related stuff - comments are useless - just RTFM
        self.light_Mngr=[]
        self.data=[
        [0,0,0,-0.00,0.003,0,0.30,0.30,0.30,100000.00,True,[self.loader.loadModel(str(MAINDIR)+"/Engine/lp_planet_0.egg"),(0.1,0,0),self.loader.loadModel(str(MAINDIR)+"/Engine/lp_planet_1.egg"),(0.14,0,0)],"low_poly_planet01",False,0.1]
        ,[10,0,0,0,0.003,0,0.05,0.05,0.05,20.00,True,[self.loader.loadModel(str(MAINDIR)+"/Engine/Icy.egg"),(0.05,0,0)],"Ottilia_modified",False,0.1]
        ,[0,70,10,0,0.005,0,0.1,0.1,0.1,40.00,True,[self.loader.loadModel(str(MAINDIR)+"/Engine/asteroid_1.egg"),(0,0,0.2)],"Selena",False,1]
        ,[100,0,10,0,0,0,5,5,5,1000000,True,[self.loader.loadModel(str(MAINDIR)+"/Engine/sun1.egg"),(0.01,0,0),self.loader.loadModel(str(MAINDIR)+"/Engine/sun1_atm.egg"),(0.01,0,0)],"Sun",True,0.1]
        ,[-100,50,70,0,0,0.003,0.15,0.15,0.15,1000.00,True,[self.loader.loadModel(str(MAINDIR)+"/Engine/Earth2.egg"),(-0.1,0,0),self.loader.loadModel(str(MAINDIR)+"/Engine/Earth2_atm.egg"),(-0.15,0,0)],"big_fucking_planet",False,0.1]
        ,[200,0,0,-0.001,0,0.01,0.1,0.1,0.1,100000,False,[self.loader.loadModel(MAINDIR+"/Engine/realistic_asteroid.egg"),(0,0.01,0)],"spaceship",False,0]
        ,[0,-120,0,0.004,0,0,0.3,0.3,0.3,100000,True,[self.loader.loadModel(str(MAINDIR)+"/Engine/FG1.egg"),(0.01,0,0),self.loader.loadModel(str(MAINDIR)+"/Engine/FG2.egg"),(0.01,0,0),self.loader.loadModel(str(MAINDIR)+"/Engine/FG3.egg"),(0.01,0,0),self.loader.loadModel(str(MAINDIR)+"/Engine/FG4.egg"),(0.01,0,0),self.loader.loadModel(str(MAINDIR)+"/Engine/FG5.egg"),(0.01,0,0)],"Frozen_giant",False,0.1]
        # insert your 3d models here, following the syntax (this is the default scene that will be loaded on startup)
        ] 
        # the correct reading syntax is [x,y,z,l,m,n,scale1,scale2,scale3,mass,static,[file,(H,p,r),file,(H,p,r)...],id,lightsource,brakeforce] for each body - x,y,z: position - l,m,n: speed - scale1,scale2,scale3: obvious (x,y,z) - mass: kg - static: boolean - [files]: panda3d readfiles list (first file must be the ground, the others are atmosphere models)
        #id: str - lightsource: boolean -
        #if you want the hitbox to be correctly scaled,and your body to have reasonable proportions, your 3d model must be a 5*5 sphere, or at least have these proportions
        
        # create the real data list, the one used by the program
        self.bodies=[]
        
        for c in self.data:
            temp=body()
            temp.fill_entries(c)
            self.bodies.append(temp)
            temp=None
        #self.bodies.reverse()
        
        # Quick presetting
        self.setBackgroundColor(0,0,0,True)
        
        # enable particles
        
        self.enableParticles()
        self.toggle_particles() # debug
        # create particle class object
        self.particle=particle()
        # intialize object:
        self.particle.config_path='/Engine/destruction_sphere.ptf' # the MAINDIR is already included inside the class definition

        # non-body type structures loading
        if SKYBOX=='sky':
            self.isphere=self.loader.loadModel(str(MAINDIR)+"/Engine/InvertedSphere.egg") #loading skybox structure
            self.tex=loader.loadCubeMap(str(MAINDIR)+'/Engine/Skybox4/skybox_#.png')
        elif SKYBOX=='arena':
            self.box=self.loader.loadModel(str(MAINDIR)+"/Engine/arena.egg") 
        
        #load shaders (optionnal)
        '''
        sun_shader=Shader.load(Shader.SLGLSL,MAINDIR+'/Engine/Shaders/flare_v.glsl',MAINDIR+'/Engine/Shaders/flare_f.glsl')
        '''
        self.camLens.setNearFar(0.5, 100000)
        
        self.orbit_lines=[] #under developement
        
        # see https://www.panda3d.org/manual/?title=Collision_Solids for further collision interaction informations
        base.graphicsEngine.openWindows()
        try:
            print('\n[Loader manager]:\n')
            '''
            self.filters.setBlurSharpen(amount=0) # just messing around
            '''
            if not self.debug:
                self.filters.set_gamma_adjust(1.0) # can be usefull
                self.filters.set_bloom(intensity=1,size="medium")
            

            for c in self.bodies: # loading and displaying the preloaded planets and bodies
                
                if c.is_lightSource and not self.debug:
                    # VM filtering
                    self.filters.setVolumetricLighting(c.filelist[0],numsamples=50,density=0.5,decay=0.95,exposure=0.035) 
                    #c.filelist[u].set_shader(sun_shader)
                    if BLUR: self.filters.setCartoonInk()
                
                for u in range(0,len(c.filelist),2): # loading each sub-file
                    c.filelist[u].reparentTo(self.Game_state.root_node)
                    c.filelist[u].setScale(tuple(c.scale))
                    c.filelist[u].setPos(tuple(c.position))
                    if u==0 and not(c.is_lightSource):
                        c.filelist[u].setShaderAuto() #activate auto shading for compact, non translucent bodies
                    #setting the collision solid up
                temp=hitbox()
                temp.Volume=CollisionSphere(0,0,0,self.u_radius)
                temp.NodePath=c.filelist[0].attachNewNode(CollisionNode(c.id))
                temp.CollisionNode=temp.NodePath.node()
                self.collision_solids.append(temp) #the radius is calculated by using the average scale + the self.u_radius 
                # the structure of the collision_solids list will be: [temp1,temp2,...]
                # asteroids and irregular shapes must be slightly bigger than their hitbox in order to avoid visual glitches
                self.collision_solids[len(self.collision_solids)-1].CollisionNode.addSolid(self.collision_solids[len(self.collision_solids)-1].Volume) #I am definitely not explaining that
                temp=None
                if self.debug:
                    loadPrcFileData('', 'show-frame-rate-meter true')
                    self.collision_solids[len(self.collision_solids)-1].NodePath.show() # debugging purposes only
                
                print("collision: ok")
                print("placing body: done")
                if c.is_lightSource:
                    self.light_Mngr.append([PointLight(c.id+"_other")])
                    self.light_Mngr[len(self.light_Mngr)-1].append(self.Game_state.root_node.attachNewNode(self.light_Mngr[len(self.light_Mngr)-1][0]))
                    self.light_Mngr[len(self.light_Mngr)-1][1].setPos(tuple(c.position))
                    ''' # shadow stuff
                    self.light_Mngr[len(self.light_Mngr)-1][1].node().setShadowCaster(True)
                    self.light_Mngr[len(self.light_Mngr)-1][1].node().getLens().setFov(40)
                    self.light_Mngr[len(self.light_Mngr)-1][1].node().getLens().setNearFar(10, 100)
                    '''
                    self.Game_state.root_node.setLight(self.light_Mngr[len(self.light_Mngr)-1][1]) 

                    self.light_Mngr.append([AmbientLight(c.id+"_self")])
                    self.light_Mngr[len(self.light_Mngr)-1][0].setColorTemperature(3000)
                    self.light_Mngr[len(self.light_Mngr)-1].append(self.Game_state.root_node.attachNewNode(self.light_Mngr[len(self.light_Mngr)-1][0]))
                    for u in range(0,len(c.filelist),2):
                        c.filelist[u].setLight(self.light_Mngr[len(self.light_Mngr)-1][1])
                    print("lights: done")
                else:
                    self.light_Mngr.append([]) #create an empty list, so that the coordinates of the data in the list is the same as in self.bodies (easier for further analysis and potential deletion)
                    self.light_Mngr.append([])
                
                print("loaded new body, out: done")
            if SKYBOX=='sky':
                self.isphere.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldCubeMap)  # *takes a deep breath* cubemap stuff !
                self.isphere.setTexProjector(TextureStage.getDefault(), self.Game_state.root_node, self.isphere)
                self.isphere.setTexPos(TextureStage.getDefault(), 0, 0, 0)
                self.isphere.setTexScale(TextureStage.getDefault(), .5) # that's a thing...
                self.isphere.setTexture(self.tex)# Create some 3D texture coordinates on the sphere. For more info on this, check the Panda3D manual.
                self.isphere.setLightOff()
                self.isphere.setScale(10000) #hope this is enough
                self.isphere.reparentTo(self.Game_state.root_node)
            elif SKYBOX=='arena':
                self.box.setPos(0,0,0)
                self.box.setScale(100)
                self.box.reparentTo(self.Game_state.root_node)
            # collision traverser and other collision stuff # that's super important, and super tricky to explain so just check the wiki
            self.ctrav = CollisionTraverser()
            self.queue = CollisionHandlerQueue()
            for n in self.collision_solids:
                self.ctrav.add_collider(n.NodePath,self.queue)
            # the traverser will be automatically updated, no need to repeat this every frame
            # debugging only
            if self.debug:
                self.ctrav.showCollisions(self.Game_state.root_node) 
            # play a random music
            self.current_playing=random.randint(0,len(self.sounds)-1)
            self.current_song=self.loader.loadSfx(self.sounds[self.current_playing])
            self.current_song.play()

            # task manager stuff comes here
            self.intro_loop()
        except:
            sys.exit(":( something went wrong: files could not be loaded")
        
        '''
        self.showsimpletext("All modules loaded, simulation running",(-1.42,0.95),(0.04,0.04),None,(1,1,1,True))
        self.showsimpletext("PyOS build V0.10",(-1.5,0.90),(0.04,0.04),None,(1,1,1,True))
        self.showsimpletext("By l3alr0g",(-1.68,0.85),(0.04,0.04),None,(1,1,1,True))
        '''
        
        # key bindings
        self.accept('backspace',self.system_break)
        self.accept('escape',self.toggle_pause)
        self.accept('mouse1',self.handle_select,[True])
        self.accept('wheel_up',self.handle_scrolling,[True]) # center button (just a quick test)
        self.accept('wheel_down',self.handle_scrolling,[False])
        self.accept('z',self.move_camera,[0,True])
        self.accept('q',self.move_camera,[1,True])
        self.accept('s',self.move_camera,[2,True])
        self.accept('d',self.move_camera,[3,True])
        self.accept('a',self.move_camera,[4,True])
        self.accept('e',self.move_camera,[5,True])
        self.accept('arrow_right',self.time_change,[True])
        self.accept('arrow_left',self.time_change,[False])
        
        self.accept('z-up',self.move_camera,[0,False])
        self.accept('q-up',self.move_camera,[1,False])
        self.accept('s-up',self.move_camera,[2,False])
        self.accept('d-up',self.move_camera,[3,False])
        self.accept('a-up',self.move_camera,[4,False])
        self.accept('e-up',self.move_camera,[5,False])
        self.keymap=['z',0,'q',0,'s',0,'d',0,'a',0,'e',0,'mouse1',0]
        
        
        if self.debug: 
            # draw axis
            coord=[(1,0,0),(0,1,0),(0,0,1)]
            axis=[]
            for c in range(3): 
                axis.append(LineSegs())
                axis[c].moveTo(0,0,0)
                axis[c].drawTo(coord[c])
                axis[c].setThickness(3)
                axis[c].setColor(tuple([coord[c][u]*255 for u in range(len(coord[c]))] +[True]))
                NodePath(axis[c].create()).reparent_to(self.Game_state.root_node)

        # camera positionning -------
        self.focus_point=[0,0,0] # point focused: can become a body's coordinates if the user tells the program to do so
        self.zoom_distance=30 # distance to the focus point in common 3D units (can be modified by scrolling)
        self.cam_Hpr=[0,0,0] # phi, alpha, theta - aka yaw, pitch, roll
        self.cam_Hpr=[self.cam_Hpr[n]*pi/180 for n in range(len(self.cam_Hpr))] # convert to rad
        phi,alpha,theta,zoom,object=self.cam_Hpr[0]*pi/180,self.cam_Hpr[1]*pi/180,self.cam_Hpr[2]*pi/180,self.zoom_distance,self.state[2] # temporary vars
        if self.state[1]=='free':
            self.camera_pos=[0,0,0]
            self.camera.setPos(tuple(self.camera_pos))
        elif self.state[1]=='linked':
            # find the object (self.state[2]) in the data list
            list_pos=[self.bodies[n].filelist[0] for n in range(len(self.bodies))].index(object.getParent())
            self.focus_point=self.bodies[list_pos].position # take the focused object's coordinates
            self.camera_pos=[self.focus_point[0]+sin(phi)*cos(-alpha)*zoom,self.focus_point[1]-cos(phi)*cos(-alpha)*zoom,self.focus_point[2]+sin(-alpha)*zoom] #keep it up to date so that it's not hard to find whend switching modes
            self.camera.setPos(tuple(self.camera_pos))
            self.camera.setHpr(self.cam_Hpr)

        # cursor
        self.cursor=self.showsimpletext('.',(0,0),(0.08,0.08),None,(1,1,1,True)) # yeah, you can laugh, but this still works so I don't care
        self.pointerNode=CollisionNode('cursor')
        self.pointerNP=camera.attachNewNode(self.pointerNode)
        self.pointerNode.setFromCollideMask(BitMask32.bit(1)) # separate collisions (in order to avoid mistakes during physical calculations)
        self.cursor_ray=CollisionRay() # create the mouse control ray
        self.pointerNode.addSolid(self.cursor_ray)
        self.ctrav.add_collider(self.pointerNP,self.queue)

        #self.screen_fill.destroy() # delete the displayed picture
        return None




    
    def showsimpletext(self,content,pos,scale,bg,fg): #shows a predefined, basic text on the screen (variable output only)
        return OnscreenText(text=content,pos=pos,scale=scale,bg=bg,fg=fg)
    
    def intro_loop(self):
        
        self.taskMgr.add(self.mouse_check,'mousePositionTask')
        self.taskMgr.add(self.placement_Mngr,'frameUpdateTask')
        self.taskMgr.add(self.Sound_Mngr,'MusicHandle')
        self.taskMgr.add(self.camera_update,'cameraPosition')
        self.taskMgr.remove('showIntroPic')
        return None
    
    def placement_Mngr(self,task): # main game mechanics, frame updating function (kinda, all pausing and menu functions must be applied here
        if self.state[0]=='running' or not task.time:
            self.ctrav.traverse(self.Game_state.root_node)
            #self.queue = CollisionHandlerQueue() # update the collision queue
            brakeforce=[0 for n in range(len(self.bodies))] # create an empty brakeforce list
            if self.queue.getNumEntries():
                if self.debug:
                    print(self.queue.getNumEntries()) # debug
                # now we have to create a temp list containing only the Entries that refer to collisions between bodies,
                # not cursor-type collisions:
                temp1,temp2=[],[]
                for count in range(len(self.queue.getEntries())):
                    if self.queue.getEntries()[count].getFromNodePath()!=self.pointerNP: temp1.append(self.queue.getEntries()[count])
                    else: temp2.append(self.queue.getEntries()[count])
                # the temp1 and temp2 lists have been created 

                # run the check for the body-with-body collisions 
                if len(temp1)>self.stored_collision_count:
                    print('[WARNING]: New collision') # debugging , detects when a collision occurs AND IT FUCKING WORKS BITCH !! (actually I created this system so that the particles linked to the collision are only created once)
                    self.particle.add_particle(temp1[self.stored_collision_count:len(temp1)])
                    b=len(temp1[self.stored_collision_count:len(temp1)])
                    for x in temp1[self.stored_collision_count:len(temp1)]:
                        self.particle.activate(x.getIntoNodePath().getParent(),self.Game_state.root_node)
                elif len(temp1)<self.stored_collision_count:
                    print('Collision ended')
                    # at this point we should probably delete the particle object, as if we don't, it might still be updated, even if the collision doesn't exist in the self.queue anymore
                self.stored_collision_count=len(temp1) #else do nothing
                for c in range(0,len(temp1),2): 
                    entry=temp1[c]
                    brakeforce=self.collision_log(entry,brakeforce)
                
                # run the check for the cursor-with-body collisions
                for c in range(len(temp2)):
                    entry=temp2[c]
                    self.watched=entry.getIntoNodePath()
                # print "out"

                # update the collider list
                self.ctrav.clear_colliders()
                self.queue = CollisionHandlerQueue()
                for n in self.collision_solids:
                    self.ctrav.add_collider(n.NodePath,self.queue)
                self.ctrav.add_collider(self.pointerNP,self.queue) # add the cursor ray again
            else:
                self.watched=None
                
            # collision events are now under constant surveillance
            acceleration=[]
            for c in range(len(self.bodies)): #selects the analysed body
                var=self.bodies[c]
                Bdf=[0,0,0] #Bdf stands for 'bilan des forces' in french, it's the resulting acceleration
                for d in self.bodies[0:c]+self.bodies[c+1:len(self.bodies)-1]: #selects the body which action on the analysed body we're studying...not sure about that english sentence though
                    S,M=[d.mass]+d.position,[var.mass]+var.position
                    temp=self.dual_a(S,M)
                    Bdf=[Bdf[x]+temp[x] for x in range(3)] # list sum
                # add the result to the global save list
                acceleration.append(Bdf)
            #update the bodies' position
            self.speed_update(acceleration,brakeforce)
            self.pos_update()
            self.apply_update()
        elif self.state[0]=='paused':
            self.handle_menu(self.iteration)
            self.iteration+=1
        return task.cont
    
    def speed_update(self,a,brakeforce):
        for c in range(len(self.bodies)): #the function updates the speed tuple accordingly
            self.bodies[c].speed[0]+=self.timescale*a[c][0]
            #self.bodies[c].speed[0]/=brakeforce[c]+1 # aero/lytho braking has to be applied to the colliding object
            # actually, speed isn't applied that way
            self.bodies[c].speed[1]+=self.timescale*a[c][1]
            #self.bodies[c].speed[1]/=brakeforce[c]+1
            self.bodies[c].speed[2]+=self.timescale*a[c][2]
            #self.bodies[c].speed[2]/=brakeforce[c]+1 
        return 0
    
    def pos_update(self): #updates the positional coordinates
        for c in range(len(self.bodies)):
            self.bodies[c].position[0]+=self.timescale*self.bodies[c].speed[0]
            self.bodies[c].position[1]+=self.timescale*self.bodies[c].speed[1]
            self.bodies[c].position[2]+=self.timescale*self.bodies[c].speed[2]
        return 0
    
    def apply_update(self): #actually moves the hole 3d stuff around
        count=0 #local counter
        for c in self.bodies:
            for u in range(len(c.filelist)):
                if u%2!=0:
                    c.filelist[u-1].setHpr(c.filelist[u-1],tuple([self.timescale*i for i in c.filelist[u]]))
                else:    
                    c.filelist[u].setPos(tuple(c.position))    
            if c.is_lightSource:
                self.light_Mngr[count][1].setPos(tuple(c.position))
            count+=2
        return 0
    
    def camera_update(self,task):
        phi,alpha,theta,zoom,object=self.cam_Hpr[0]*pi/180,self.cam_Hpr[1]*pi/180,self.cam_Hpr[2]*pi/180,self.zoom_distance,self.state[2]
        if self.state[1]=='free':
            self.camera.setPos(tuple(self.camera_pos))
        elif self.state[1]=='linked':
            # find the object (self.state[2]) in the data list
            list_pos=[self.bodies[n].filelist[0] for n in range(len(self.bodies))].index(object.getParent())
            self.focus_point=self.bodies[list_pos].position # take the focused object's coordinates
            self.camera_pos=[self.focus_point[0]+sin(phi)*cos(-alpha)*zoom,self.focus_point[1]-cos(phi)*cos(-alpha)*zoom,self.focus_point[2]+sin(-alpha)*zoom]
            self.camera.setPos(tuple(self.camera_pos))
            self.camera.setHpr(tuple(self.cam_Hpr))
        
        # collision cursor stuff goes here:
        self.cursor_ray.setFromLens(self.camNode,0,0) 
        # relatively to the camera, the cursor position will always be 0,0 which is the position of the 
        # white point on the screen


        if self.keymap!=['z',0,'q',0,'s',0,'d',0]:
            for x in range(1,len(self.keymap),2):
                if self.keymap[x]:
                    self.move_camera(int((x-1)/2),True) # why (x-1)/2 ? because we have to make the tow readable as a key number, like 0,1,2,3
        return task.cont

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
    
    def collision_log(self,entry,brakeforce):
        from_pos=[self.bodies[n].filelist[0] for n in range(len(self.bodies))].index(entry.getFromNodePath().getParent())
        into_pos=[self.bodies[n].filelist[0] for n in range(len(self.bodies))].index(entry.getIntoNodePath().getParent()) #find the nodepath in the list
        f_radius=sum(self.bodies[from_pos].scale)*self.u_radius/3
        i_radius=sum(self.bodies[into_pos].scale)*self.u_radius/3
        if max(f_radius,i_radius)==f_radius:
            inverted=True
            into_pos,from_pos=from_pos,into_pos
        else:
            inverted=False # currently unused
        brakeforce[from_pos]=self.bodies[from_pos].brakeforce # get the force given in the data list
        # those are the two positions of the nodepaths, now we need to know which one is bigger, in order to obtain the fusion effect
        # from_pos is the smaller body, into_pos is the bigger one
        self.collision_gfx(self.momentum_transfer(from_pos,into_pos,entry,inverted),f_radius,i_radius) #some useless data remains from version 0.9
        return brakeforce
    
    def momentum_transfer(self,f_pos,i_pos,entry,inverted):
        if self.debug:
            print("colliding") # debug, makes the game laggy (only activated when the self.debug var is on)
        interior = entry.getInteriorPoint(self.Game_state.root_node) # default
        surface = entry.getSurfacePoint(self.Game_state.root_node)
        print((interior - surface).length()) # debug, doesn't slow the game down too much so I haven't removed it


        if (interior - surface).length() >= self.u_radius*2*sum(self.bodies[f_pos].scale)/3: # this is the body deletion routine
            if self.state[2]==self.collision_solids[f_pos].NodePath:
                self.state[1]='free'
                self.state[2]=None

            # Lighting
            if self.bodies[f_pos].is_lightSource:
                self.light_Mngr[2*f_pos][1].removeNode()
                self.light_Mngr[2*f_pos][1].removeNode()
                self.filters.delVolumetricLighting() #temp
            
            self.ctrav.remove_collider(self.collision_solids[f_pos].NodePath)
            self.bodies[f_pos].delete_body()
            
            self.bodies[i_pos].scale[0]*=(self.bodies[i_pos].mass+self.bodies[f_pos].mass)/self.bodies[i_pos].mass
            self.bodies[i_pos].scale[1]*=(self.bodies[i_pos].mass+self.bodies[f_pos].mass)/self.bodies[i_pos].mass
            self.bodies[i_pos].scale[2]*=(self.bodies[i_pos].mass+self.bodies[f_pos].mass)/self.bodies[i_pos].mass
            self.bodies[i_pos].mass+=self.bodies[f_pos].mass
            
            # particle deletion

            self.particle.deactivate(self.collision_solids[f_pos].NodePath.getParent())
            self.particle.deactivate(self.collision_solids[i_pos].NodePath.getParent())
                
            # scale updating ()
            ''' temporarly removed
            for c in range(0,len(self.bodies[i_pos].filelist),2):
                self.bodies[i_pos].filelist[c].setScale(tuple(self.bodies[i_pos].scale))
            '''
            # deleting the destroyed planet's data
            self.bodies=self.bodies[:f_pos]+self.bodies[f_pos+1:len(self.bodies)]
            self.collision_solids=self.collision_solids[:f_pos]+self.collision_solids[f_pos+1:len(self.collision_solids)]
            # update the light list
            self.light_Mngr=self.light_Mngr[:2*f_pos]+self.light_Mngr[2*f_pos+2:len(self.light_Mngr)]
            
            
            # just a quick test
            if self.debug:
                self.ctrav.showCollisions(self.Game_state.root_node) 
            if self.debug:
                print("planet destroyed")
        return interior,surface # used for the collision gfx calculations
    
    def printScene(self):  #debug
        file=open("scenegraph.txt","a")
        ls = LineStream()
        self.Game_state.root_node.ls(ls)
        while ls.isTextAvailable():
            file.write(ls.getLine())
            file.write("\n")
        file.write("\n")
        file.write("END\n")
        file.write("\n")
        file.close()
    
    def Sound_Mngr(self,task):
        if self.current_song.length()-self.current_song.getTime()==0: #could have just used not()
            self.current_playing=random.choice(list(range(0,self.current_playing))+list(range(self.current_playing+1,len(self.sounds))))
            self.current_song=self.loader.loadSfx(self.sounds[self.current_playing])
            self.current_song.play()
            print(self.current_playing)
        return task.cont

    def collision_gfx(self,points,Rf,Ri): # collision animation calculations
        # section size calculation
        # we know the depth of penetration (no silly jokes please), which allows us, knowing the radius of each body, 
        # to calculate the radius of the section (I've got no idea how to say that in correct english)
        # the display of the particles all over this circle will be a piece of cake (at least I hope so)  - edit - it wasn't
        # see documents in the screenshot folder for more informations about the maths
        '''
        interior,surface=points[0],points[1]
        p=(interior - surface).length()
        p2=(p**2-2*Ri*p)/(2*Ri-2*p-2*Rf)
        p1=p-p2
        ''' #currently useless
        self.update_particle_pos()
        # now we know everything about our impact section (the circle that defines the contact between the two bodies)
        # we just have to find the coord of the circle's center: we will take the surfacepoint impact point
         
        return 0

    def create_crater(self): # see project for more informations
        return None

    def toggle_pause(self):
        self.toggle_particles() # pause the particles
        temp=['paused','running']
        self.state[0]=temp[self.state[0]==temp[0]] # switches between paused and running
        self.iteration=0
        if self.state[0]=='paused':
            self.handle_menu(self.iteration)
        else:
            self.filters.del_blur_sharpen()
            # make the mouse invisible
            self.hidden_mouse=True
            wp = WindowProperties()
            wp.setCursorHidden(self.hidden_mouse)
            # set the mouse pos to 0 
            self.center_mouse()

            self.win.requestProperties(wp)
            for u in self.menu_text:
                u.hide()
        return None
    
    def handle_menu(self,iteration):
        if not iteration:
            self.accept('escape',self.toggle_pause)
            self.draw_menu()
            # make the mouse visible
            self.hidden_mouse=False
            wp = WindowProperties()
            wp.setCursorHidden(self.hidden_mouse)
            self.win.requestProperties(wp)
        else:
            a=1 # indentation (temporary)
            #put your mouse detection stuff here
            # menu stuff
            # menu stuff
            # please use directGui for that purpose (better rendering performances)
            # the menu doesn't actually work, as the whole clicking reaction routine is not implemented
        return None
    
    def draw_menu(self):
        self.filters.setBlurSharpen(amount=0)
        for u in self.menu_text:
                u.show()
        return None
    
    def show_credits(self):
        print("created by l3alr0g, zudo and Fang (at least this part) --> I'll do something better later")
        return None
        
    def system_break(self):
        # place your data saving routines here
        print("system exit successful, data saved")
        print("executing sys.exit()")
        print("out: done")
        sys.exit(0)
        return None
    
    def handle_scrolling(self,up): # up is a boolean: up=True means up, up=False means down
        if up and self.state[0]=='running':
            if self.state[1]=='linked':
                self.zoom_distance*=0.95
            else:
                self.camera_delta*=1.1
        elif not up and self.state[0]=='running':
            if self.state[1]=='linked':
                self.zoom_distance/=0.95
            else:
                self.camera_delta/=1.1
        return None

    
    def rotate_camera(self):
        self.camera.setHpr(tuple(self.cam_Hpr))
        return None
    
    def move_camera(self,tow,pressed): # tow stands for towards, pressed is a boolean which indicates the state of the key
        if pressed:
            self.keymap[2*tow+1]=1
            self.state[1]='free'
            #print('free mode on')
            self.state[2]=None
        else:
            self.keymap[2*tow+1]=0
        
        if self.keymap[2*tow+1]:
            phi,alpha,theta,delta,zoom=self.cam_Hpr[0]*pi/180,self.cam_Hpr[1]*pi/180,self.cam_Hpr[2]*pi/180,self.camera_delta,self.zoom_distance
            if self.keymap[2*tow]=='q':
                if self.state[1]=='free':
                    self.camera_pos=[self.camera_pos[0]-cos(phi)*cos(theta)*delta,self.camera_pos[1]-sin(phi)*cos(theta)*delta,self.camera_pos[2]+sin(theta)*delta] # moving the camera
            if self.keymap[2*tow]=='z':
                if self.state[1]=='free':
                    self.camera_pos=[self.camera_pos[0]-sin(phi)*cos(alpha)*delta,self.camera_pos[1]+cos(phi)*cos(alpha)*delta,self.camera_pos[2]+sin(alpha)*delta]
            if self.keymap[2*tow]=='s':
                if self.state[1]=='free':
                    self.camera_pos=[self.camera_pos[0]+sin(phi)*cos(alpha)*delta,self.camera_pos[1]-cos(phi)*cos(alpha)*delta,self.camera_pos[2]-sin(alpha)*delta]
            if self.keymap[2*tow]=='d':
                if self.state[1]=='free':
                    self.camera_pos=[self.camera_pos[0]+cos(phi)*cos(theta)*delta,self.camera_pos[1]+sin(phi)*cos(theta)*delta,self.camera_pos[2]-sin(theta)*delta]
            if self.keymap[2*tow]=='a':
                self.cam_Hpr[2]-=1
            if self.keymap[2*tow]=='e':
                self.cam_Hpr[2]+=1
        return None
    
    def mouse_check(self,task): # gets the mouse's coordinates
        mwn = self.mouseWatcherNode
        if mwn.hasMouse():
            x,y=mwn.getMouseX(),mwn.getMouseY()
            #print(x,y) # debug
            # focus_point coordinates modifier code here:
            if self.state==['running','free',None]:
                self.cam_Hpr[0]-=x*self.sensitivity_x # the - fixes a bug I can't solve
                # sensitivity is a coefficient used for mouse displacement routines
                self.cam_Hpr[1]+=y*self.sensitivity_y # those formulas do not work when theta (self.cam_Hpr[2]) changes 
                self.rotate_camera()
                self.center_mouse()
            elif self.state[0]=='running' and self.state[1]=='linked':
                self.cam_Hpr[0]-=x*self.sensitivity_x
                self.cam_Hpr[1]-=y*self.sensitivity_y
                self.rotate_camera()
                self.center_mouse()
            '''
            if self.debug:
                print(self.cam_Hpr,self.camera_pos) # debug
        '''
        return task.cont

    def center_mouse(self):
        self.win.movePointer(0,
          int(self.win.getProperties().getXSize() / 2),
          int(self.win.getProperties().getYSize() / 2)) # move mouse back to center --> careful ! this makes the delta calculation code buggy
    
    def handle_select(self,is_clicked): 
        if is_clicked and self.watched!=None:
            self.state[1]='linked' # toggle following mode
            self.state[2]=self.watched
            print('linked mode on, focusing: ',self.watched)
        #else: # do nothing actually
        return None
    
    def update_particle_pos(self): # harder than I thought
        for x in range(len(self.particle.particle_list)):
            a=[i.getIntoNodePath() for i in self.queue.getEntries()].index(self.particle.particle_list[x][1]) # finding the intonodepath inside self.queue.getEntries()
            self.particle.particle_list[x][0].setPos(self.queue.getEntries()[a].getSurfacePoint(self.Game_state.root_node)) # all particles are being displaced to the position of the surface impact point
            tempvar=self.queue.getEntries()[a].getSurfacePoint(self.Game_state.root_node) - self.queue.getEntries()[a].getIntoNodePath().getParent().getPos()
            H,P,R=-atan(tempvar[0]/tempvar[1])*180/pi+180,(-atan(tempvar[2]/tempvar[1])+pi/2)*180/pi,0
            self.particle.particle_list[x][0].setHpr(H,P,R)
        # self.queue.getEntries()[a].getIntoNodePath().getParent().getPos()
        # +self.queue.getEntries()[a].getSurfacePoint(self.queue.getEntries()[a].getIntoNodePath())  
        
        return None
    
    def time_change(self,income): # income is a boolean, True means speed up, False means speed down
        if income:
            self.timescale*=1.2
        else:
            self.timescale*=0.80
        return None
    
    def easter_egg(self):
        return "please be patient, our hens are working on it"
    

launch=world()
base.run()
        

