import bpy
import math
import numpy

baseSpriteName = "Sprite"

circleName = "SpriteCreatorCircle"
circleRadius = 10
circleHeight = 10

cameraName = "SpriteCreatorCamera"
cameraXRotation = math.radians(72)

createCameraSetup = True

def start():
	circle = bpy.data.objects.get(circleName)
	camera = bpy.data.objects.get(cameraName)
	
	if createCameraSetup:
		if circle is None:
			circle = createCircle()
			
		if camera is None:
			camera = createCamera(circle)
		
def createCircle():
	bpy.ops.mesh.primitive_circle_add(radius=circleRadius, fill_type='NOTHING', location=[0, 0, circleHeight])
	
	return bpy.context.active_object

def createCamera(circle):
	bpy.ops.object.camera_add(view_align = False, location = [0, -circleRadius, circle.location.z], rotation = [cameraXRotation, 0, 0])
	camera = bpy.context.active_object
	camera.name = cameraName

	camera.parent_set(circle)
	
start()