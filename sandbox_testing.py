from direct.showbase.ShowBase import ShowBase
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.core import *
import os
from math import *
from direct.gui.OnscreenImage import OnscreenImage

MAINDIR=Filename.fromOsSpecific(os.getcwd())
class app(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        self.planet=self.loader.loadModel(MAINDIR+'/Engine/Dark_soul.egg')
        self.planet.setPos(0,0,0)
        self.planet.setScale(0.09,0.09,0.09)
        self.planet.reparentTo(render)
        
        self.setBackgroundColor(0.2,0.2,0.2,1)

        self.backgrnd=OnscreenImage(image=str(MAINDIR)+'/Engine/Stars.png',scale=(1.78,1,1))
        self.backgrnd.reparentTo(render)
        self.backgrnd.setPos(0,0,0)

        self.enableParticles()
        self.testpart=ParticleEffect()
        self.testpart.loadConfig(MAINDIR+'/Engine/destruction_sphere.ptf')
        self.testpart.start(parent=render,renderParent=render)
        self.pointA,self.pointB=LPoint3f(0,0,0),LPoint3f(1,3,2)
        vec = self.pointB - self.pointA
        norm=vec.length()
        H,P,R=-atan(vec[0]/vec[1])*180/pi+180,(-atan(vec[2]/vec[1])+pi/2)*180/pi,0 # cette formule vaut son poids en or X)
        #H,P,R=30,-30,0
        self.planet.setHpr(H,P,R)
        self.testpart.setHpr(H,P,R) 
        self.testpart.radiateOrigin=(vec[0]/norm,vec[1]/norm,vec[2]/norm)
        
        # axis
        coord=[(1,0,0),(0,1,0),(0,0,1)]
        axis=[]
        for c in range(3): 
            axis.append(LineSegs())
            axis[c].moveTo(0,0,0)
            axis[c].drawTo(coord[c])
            axis[c].setThickness(3)
            axis[c].setColor(tuple([coord[c][u]*255 for u in range(len(coord[c]))] +[0.05]))
            NodePath(axis[c].create()).reparent_to(render)

        # end of axis

        testline=LineSegs()
        testline.moveTo(self.pointA)
        testline.drawTo(self.pointB)
        testline.setThickness(3)
        testline.set_color(0,0,0,1)
        NodePath(testline.create()).reparent_to(render)


        plight=render.attachNewNode(PointLight('plight01'))
        plight.setPos(5,0,0)
        self.planet.setLight(plight)

        
    
    



app().run()

