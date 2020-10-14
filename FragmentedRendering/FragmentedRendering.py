"""
Fragmented rendering script for Blender for use with large models to be rendered at a high resolution.

The script assumes that the camera is in orthographic mode and renders the images in increments of the size
of the camera's orthographic scale.

It is also assumed that the camera is placed at the starting top-left position of the overall image to be rendered.

Settings:

cameraName: the name of the current active camera on Blender;
baseName: output file base name;
lines: number of lines to render;
columns: number of columns to render at each line;

The output directory should be set inside Blender.
"""

import bpy
import math
import numpy
import mathutils

outputDirectory = bpy.data.scenes["Scene"].render.filepath

camera = None
cameraName = "Camera"

baseName = "Output"
lines = 11
columns = 17

def start():
	setupCamera()
	renderSprites()
	
	bpy.data.scenes["Scene"].render.filepath = outputDirectory
	
def setupCamera():
	global camera
	camera = bpy.data.objects.get(cameraName)
	
def renderSprites():
	origin = mathutils.Vector((camera.location.x, camera.location.y, camera.location.z))
	offsetIncrement = camera.data.ortho_scale
	
	for line in range(lines):
		camera.location = mathutils.Vector((origin.x, origin.y, origin.z))
		camera.location.y -= offsetIncrement * line
		
		for column in range(columns):
			bpy.data.scenes["Scene"].render.filepath = outputDirectory + baseName + str(line) + "-" + str(column)
			bpy.ops.render.render(write_still = True)
			camera.location.x += offsetIncrement
			
	camera.location = mathutils.Vector((origin.x, origin.y, origin.z))
	
start()