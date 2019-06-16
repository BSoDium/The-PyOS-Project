from panda3d.core import *

class body:
    def __init__(self):
        self.position=[0,0,0]
        self.speed=[0,0,0]
        self.scale=[1,1,1]
        self.mass=1
        self.is_static=True
        self.filelist=[]
        self.id=''
        self.is_lightSource=False
        self.brakeforce=0
    
    def fill_entries(self,list):
        try:
            test=list[14] # test the lenght of the list
        except:
            sys.exit('incorrect data entry, please modify your bodies data list')
        self.position=list[0:3]
        self.speed=list[3:6]
        self.scale=list[6:9]
        self.mass=list[9]
        self.is_static=list[10]
        self.filelist=list[11]
        self.id=list[12]
        self.is_lightSource=list[13]
        self.brakeforce=list[14]
        return 0
    
    def delete_body(self):
        for c in range(0,len(self.filelist),2):
            self.filelist[c].removeNode()
        return 0

class hitbox:
    def __init__(self):
        self.Volume=None
        self.NodePath=None
        self.CollisionNode=None
    
class particle:
    def __init__(self):
        self.config_path=None
        self.particle_list=[] # list containing the whole particle scene stuff
        self.garbage=[] # particles that will fade out and be destroy after a short period of time
        return None
    def activate(self,nodep,focus): # collision is the associated collision (defined when creating the particle)
        try:
            rank=[self.particle_list[x][1].getParent() for x in range(len(self.particle_list))].index(nodep)
            self.particle_list[rank][0].start(parent=focus,renderParent=focus)
            self.particle_list[rank][0].setScale(nodep.getScale())
            self.particle_list[rank][0].setLightOff()
        except: print('[WARNING]: incorrect rank value / generate_base_part() must be executed first')
        return None
    def deactivate(self,nodep):
        try:
            rank=[self.particle_list[x][1].getParent() for x in range(len(self.particle_list))].index(nodep)
            self.particle_list[rank][0].softStop()
            self.garbage.append(self.particle_list[rank][0])
            self.particle_list.remove(self.particle_list[rank])
        except: print('[WARNING]: incorrect rank value / generate_base_part() must be executed first')
        return None
    def add_particle(self,datalist): # the datalist is the self.queue list (we get the collision count and write the particle files accordingly)
        try:
            for x in datalist:
                self.particle_list.append([ParticleEffect(),x.getIntoNodePath()]) # by default, there is only one particle per planet, more can be added in the sub-list
                self.particle_list[len(self.particle_list)-1][0].loadConfig(str(MAINDIR)+self.config_path)
        except: print('[WARNING]: incorrect datalist')
        return None
            
