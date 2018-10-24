import bpy
import math
import numpy

baseSpriteName = "Sprite"
cameraBlendFile = "SpriteCreatorCamera.blend"

#Circle settings
circleName = "SpriteCreatorCircle"
circleRadius = 25
circleHeight = 12

#Camera settings
cameraName = "SpriteCreatorCamera"
cameraXRotation = math.radians(73)

importCameraSetup = True
importAppending = True
createCameraSetup = True

setupRender = True
mirrorSprites = True

def start():
	circle = bpy.data.objects.get(circleName)
	camera = bpy.data.objects.get(cameraName)
	
	if createCameraSetup:
		if circle is None:
			circle = createCircle()
			
		if camera is None:
			camera = createCamera(circle)
	
	#This freezes Blender until the render is done
	bpy.ops.render.render(write_still = False)
		
def createCircle():
	bpy.ops.mesh.primitive_circle_add(radius=circleRadius, fill_type='NOTHING', location=[0, 0, circleHeight])
	bpy.context.active_object.name = circleName
	
	return bpy.context.active_object

def createCamera(circle):
	bpy.ops.object.camera_add(view_align = False, location = [0, -circleRadius, circle.location.z], rotation = [cameraXRotation, 0, 0])
	camera = bpy.context.active_object
	camera.name = cameraName
	
	circle.select = True
	camera.select = True
	bpy.context.scene.objects.active = circle
	bpy.ops.object.parent_set()
	
	camera.data.type = "ORTHO"
	camera.data.ortho_scale = 10
	
start()