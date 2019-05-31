from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
import os

class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # ShowBase instance created
        self.dir=Filename.fromOsSpecific(os.getcwd())
        self.set_background_color(0,0,0,True)
        # current directory stored into self.dir
        self.test_object=self.loader.loadModel(self.dir+"/Engine/sun1.egg")
        self.test_object.reparentTo(self.render)
        self.test_object.setPos(0,0,0)

        # create a light if we want the object to behave correctly
        self.ambient_light=PointLight('sun')
        self.a_light_node=self.render.attachNewNode(self.ambient_light)
        self.a_light_node.setPos(0,0,0)
        self.render.setLight(self.a_light_node)
        # loading first shader
        sun_shader=Shader.load(Shader.SLGLSL,self.dir+'/Engine/Shaders/flare_v.glsl',self.dir+'/Engine/Shaders/flare_f.glsl')
        self.test_object.set_shader(sun_shader)

MyApp=App()
MyApp.run()
