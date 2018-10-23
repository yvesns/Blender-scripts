import bpy
import math
import numpy

blockCount = 0

class Mesh:
	def __init__(self, vertices, faces):
		self.vertices = vertices
		self.faces = faces

class Point:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

class Object:
	def __init__(self, obj, center):
		self.obj = obj
		self.center = center
		
def createMesh(name, meshData):
	mesh = bpy.data.meshes.new(name)
	mesh.from_pydata(meshData.vertices, [], meshData.faces)
	mesh.update()

	obj = bpy.data.objects.new(name, mesh)

	scene = bpy.context.scene
	scene.objects.link(obj)
	obj.select = True
	
	return obj

def buildBlockMeshData(start, finish):
	width = finish.x - start.x
	depth = finish.y - start.y
	height = finish.z - start.z
	x = start.x
	y = start.y
	z = start.z

	vertices = [
		(x, y, z), 							#0 - Down, left, front.
		(x, y, z + height), 				#1 - Up, left, front.
		(x + width, y, z + height), 		#2 - Up, right, front.
		(x + width, y, z), 					#3 - Down, right, front.
		(x, y + depth, z), 					#4 - Down, left, back.
		(x, y + depth, z + height), 		#5 - Up, left, back.
		(x + width, y + depth, z + height), #6 - Up, right, back.
		(x + width, y + depth, z),			#7 - Down, right, back.
	]
	
	faces = [
		(0, 1, 2, 3),
		(0, 1, 5, 4),
		(4, 5, 6, 7),
		(2, 3, 7, 6),
		(1, 2, 6, 5),
		(0, 4, 7, 3),
	]
	
	mesh = Mesh(vertices, faces)

	return mesh
	
def createBlock(start, finish, height, depth, name = "block" + str(blockCount)):
	p = Point(start.x + math.fabs(finish.x - start.x), start.y + depth, start.z + height)
	center = Point(math.fabs(finish.x - start.x)/2, (start.y + depth)/2, (start.z + height)/2)
	meshData = buildBlockMeshData(start, p)
	obj = createMesh(name, meshData)
	rotationY = 0 
	rotationZ = 0
	
	if(start.y != finish.y or start.x > finish.x):
		rotationZ = math.atan2(finish.y - start.y, finish.x - start.x)
		
	if(start.z != finish.z):
		rotationY = math.atan2(finish.z - start.z, finish.x - start.x)
		
	obj.rotation_euler = (0, -rotationY, rotationZ)
	
	global blockCount
	blockCount += 1
	
	return Object(obj, center)
	
def createArch(archWidth, archHeight, zStep = 0.1, start = Point(0,0,0), thickness = 1, rotation = (0,0,0)):
	curveCoords = []
	xRadius = archWidth/2
	
	for i in numpy.arange(0, archHeight + zStep, zStep):
		cx = start.x - (getEllipseX(xRadius, archHeight, i))
		curveCoords.append((cx, start.y, start.z + i))
	
	for i in numpy.arange(archHeight-zStep, -zStep, -zStep):
		cx = start.x + getEllipseX(xRadius, archHeight, i)
		curveCoords.append((cx, start.y, start.z + i))
	
	curveData = bpy.data.curves.new('archCurve', type='CURVE')
	curveData.dimensions = '3D'
	
	line = curveData.splines.new('POLY')
	line.points.add(len(curveCoords) - 1)
	for i, coord in enumerate(curveCoords):
		x,y,z = coord
		line.points[i].co = (x, y, z, 1)
	
	curveData.fill_mode = 'FULL'
	curveData.bevel_depth = thickness
	curveObj = bpy.data.objects.new('myCurve', curveData)
	curveObj.rotation_euler = rotation
	
	scn = bpy.context.scene
	scn.objects.link(curveObj)
	scn.objects.active = curveObj
	
	return curveObj
	
def getEllipseX(xRadius, yRadius, y = 0):
	return math.sqrt(math.pow(xRadius, 2) * math.fabs((1 - (math.pow(y, 2)/math.pow(yRadius, 2)))))
	
def getEllipseY(xRadius, yRadius, x = 0):
	return math.sqrt(math.pow(yRadius, 2) * math.fabs((1 - (math.pow(x, 2)/math.pow(xRadius, 2)))))