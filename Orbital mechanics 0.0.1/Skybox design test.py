import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import Texture, TextureStage, DirectionalLight, AmbientLight, TexGenAttrib, VBase4

class SkySphere(DirectObject):
	def __init__(self):		
		self.sphere = loader.loadModel("generic_planet.egg")
		# Load the most common spherical planet 3d model (I finally got this blender plugin to work).
		# I'm planning on doing some 3d model in-game modification later
		
		self.sphere.setTexGen(TextureStage.getDefault(), TexGenAttrib.MWorldPosition)
		self.sphere.setTexProjector(TextureStage.getDefault(), render, self.sphere)
		self.sphere.setTexPos(TextureStage.getDefault(), 0, 0, 0)
		self.sphere.setTexScale(TextureStage.getDefault(), .5)
		# Create some 3D texture coordinates on the sphere. For more info on this, check the Panda3D manual.
		
		tex = loader.loadCubeMap("BlueGreenNebula_#.png")
		self.sphere.setTexture(tex)
		# Load the cube map and apply it to the sphere.
		
		self.sphere.setLightOff()
		# Tell the sphere to ignore the lighting.
			
		self.sphere.setScale(1000)
		# Increase the scale of the sphere so it will be larger than the scene.
		
		self.sphere.reparentTo(render)
		# Reparent the sphere to render so you can see it.
		
		result = self.sphere.writeBamFile("SkySphere.bam")
		# Save out the bam file.
		print(result)
		# Print out whether the saving succeeded or not.

SS = SkySphere()
run()