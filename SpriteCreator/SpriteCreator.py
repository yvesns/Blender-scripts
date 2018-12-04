import bpy
import math
import numpy

outputDirectory = bpy.data.scenes["Scene"].render.filepath
baseSpriteName = "Sprite"

#Circle settings
circleName = "SpriteCreatorCircle"
circleRadius = 25
circleHeight = 12

#Camera settings
cameraName = "SpriteCreatorCamera"
cameraXRotation = math.radians(73)

directionsRight = {
	"S": math.radians(0),
	"SE": math.radians(-45),
	"E": math.radians(-90),
	"NE": math.radians(-135),
	"N": math.radians(180)
}

directionsLeft = {
	"SW": math.radians(45),
	"W": math.radians(90),
	"NW": math.radians(135)
}

createCameraSetup = True
mirrorSprites = True

def start():
	circle = bpy.data.objects.get(circleName)
	camera = bpy.data.objects.get(cameraName)
	
	if createCameraSetup:
		if circle is None:
			circle = createCircle()
			
		if camera is None:
			camera = createCamera(circle)
			
	for obj in bpy.context.scene.objects:
		obj.select = False
	
	for obj in bpy.context.visible_objects:
		if not (obj.hide or obj.hide_render):
			if (obj != circle and obj != camera):
				obj.select = True
			
	for direction, rotation in directionsRight.items():
		circle.rotation_euler = (0, 0, rotation)
		bpy.ops.view3d.camera_to_view_selected()
		bpy.data.scenes["Scene"].render.filepath = outputDirectory + baseSpriteName + direction
		bpy.ops.render.render(write_still = True)
	
	if not mirrorSprites:
		for direction, rotation in directionsLeft.items():
			circle.rotation_euler = (0, 0, rotation)
			bpy.ops.view3d.camera_to_view_selected()
			bpy.data.scenes["Scene"].render.filepath = outputDirectory + baseSpriteName + direction
			bpy.ops.render.render(write_still = True)
			
	bpy.data.scenes["Scene"].render.filepath = outputDirectory
		
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