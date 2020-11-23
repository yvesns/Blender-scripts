"""
Simple script to render several images in sequence by shape key steps.

Settings:

baseName: output file base name;
shapeKeyName: name of the shape key to be rendered;
shapeKeyStep: step to apply to the shape key value at each iteration. If this is set to a negative value, the shape key is rendered in reverse order;

The output directory should be set inside Blender.
"""

import bpy
import math
import numpy
import mathutils

outputDirectory = bpy.data.scenes["Scene"].render.filepath

camera = None
cameraName = "Camera"

baseName = "fileName"
shapeKeyName = "shapeKey"
shapeKeyStep = 0.1

def start():
	setupCamera()
	renderSprites()
	
	bpy.data.scenes["Scene"].render.filepath = outputDirectory
	
def setupCamera():
	global camera
	camera = bpy.data.objects.get(cameraName)
	
def renderSprites():
	finalShapeKeyValue = 1
	shapeKey = bpy.context.object.data.shape_keys.key_blocks[shapeKeyName]
	imageCount = 0
	
	if shapeKeyStep < 0:
		finalShapeKeyValue = 0
		
	while shapeKey.value != finalShapeKeyValue:
		bpy.data.scenes["Scene"].render.filepath = outputDirectory + baseName + "-" + str(imageCount)
		bpy.ops.render.render(write_still = True)
		shapeKey.value += shapeKeyStep
		imageCount += 1
		
start()