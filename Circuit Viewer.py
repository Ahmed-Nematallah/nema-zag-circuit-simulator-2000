"""This is the circuit viewer module."""
import pygame
import Buttons
import copy
import enum
# import sys
import struct
# import ctypes
import numpy as np
import matplotlib.pyplot as plt
from pygame.locals import *
import eztext
import time
import Analyze
import importlib
eventType = enum.Enum("eventType", "Quit Mouse_Motion Key_Down Mouse_Up")

def snapToGrid(x, y, gridspace):
	"""Snap cursor to grid."""
	if (x % gridspace < gridspace / 2):
		x = x - (x % gridspace)
	else:
		x = (x + gridspace) - (x % gridspace)
	if (y % gridspace < gridspace / 2):
		y = y - (y % gridspace)
	else:
		y = (y + gridspace) - (y % gridspace)
	return x, y

def flatten(listOfLists):
	"""Flatten one level of nesting."""
	z = [x for sublist in listOfLists for x in sublist]
	return z

def flattenml(listOfLists):
	"""Flatten multiple levels of nesting."""
	listOfLists2 = copy.deepcopy(listOfLists)
	while not(type(listOfLists2[0]) == int):
		listOfLists3 = flatten(listOfLists2)
		listOfLists2 = copy.deepcopy(listOfLists3)

	return listOfLists2

def getComponentValue(componentValue):
	"""Convert component value suffix to floatinv value."""
	if(componentValue.lower().endswith('k')):
		val = complex(componentValue[:-1]) * 1000
	elif(componentValue.lower().endswith('meg')):
		val = complex(componentValue[:-3]) * 1000000
	elif(componentValue.lower().endswith('g')):
		val = complex(componentValue[:-1]) * 1000000000
	elif(componentValue.lower().endswith('t')):
		val = complex(componentValue[:-1]) * 1000000000000
	elif(componentValue.lower().endswith('m')):
		val = complex(componentValue[:-1]) / 1000
	elif(componentValue.lower().endswith('u')):
		val = complex(componentValue[:-1]) / 1000000
	elif(componentValue.lower().endswith('n')):
		val = complex(componentValue[:-1]) / 1000000000
	elif(componentValue.lower().endswith('p')):
		val = complex(componentValue[:-1]) / 1000000000000
	elif(componentValue.lower().endswith('f')):
		val = complex(componentValue[:-1]) / 1000000000000000
	else:
		val = complex(componentValue)

	return val


global font
pygame.font.init()
font = pygame.font.SysFont(None, 25)

def writeonscreen(text, color, pos):
	screentext = font.render(text, True, color)
	gameDisplay.blit(screentext, pos)

def Writeonstatusbar(text):
	writeonscreen(text,(0,0,0),[0,Windowsize[1]-20])
	pass

# create Buttons
buttonnamelist = ["Resistor", "Capacitor", "Inductor", "Diode", "Voltage source", "Current source", "Ground", "conductance", "OPAMP"]
buttonlist = []
# for b in buttonnamelist:
# button = Buttons.Button()
# buttonlist.append(button)

resistorButton = Buttons.Button()
capacitorButton = Buttons.Button()
inductorButton = Buttons.Button()
diodeButton = Buttons.Button()
vsourceButton = Buttons.Button()
csourceButton = Buttons.Button()
gndButton = Buttons.Button()
conductanceButton = Buttons.Button()
opampButton = Buttons.Button()
rotateButton = Buttons.Button()
saveButton = Buttons.Button()
netlistButton = Buttons.Button()
ACButton = Buttons.Button()
DCButton = Buttons.Button()
sweepButton = Buttons.Button()
changetitleButton = Buttons.Button()
deleteButton = Buttons.Button()
graphButton = Buttons.Button()
newButton = Buttons.Button()
startsimButton = Buttons.Button()

def initalize():
	"""Initialize SDL and other stuff."""
	#some global var
	global gameDisplay
	global clock
	global gridspace
	global linethickness
	global lineColor
	global backgroundColor
	global compdict
	global typedict
	global currentComponent
	global Windowsize 
	global status
	# load component icons
	resistoricon = pygame.image.load('Resources/res.png')
	resistoricon = pygame.transform.rotate(resistoricon, 90)
	capacitoricon = pygame.image.load('Resources/Capacitor_Symbol.png')
	capacitoricon = pygame.transform.rotate(capacitoricon, 90)
	diodeicon = pygame.image.load('Resources/Diode_symbol.png')
	diodeicon = pygame.transform.rotate(diodeicon, 90)
	inductoricon = pygame.image.load('Resources/Inductor.png')
	inductoricon = pygame.transform.rotate(inductoricon, 90)
	vsourceicon = pygame.image.load('Resources/Voltage_source.png')
	csourceicon = pygame.image.load('Resources/Current_source.png')
	gndicon = pygame.image.load('Resources/GND.png')
	opampicon = pygame.image.load('Resources/Op-amp_symbol.png')
	opampicon = pygame.transform.rotate(opampicon, 90)

	print (resistoricon.get_rect().size[1])  # you can get size
	# , draw coordinates,width and length,start and end point in grid coordinates, color , type
	# compdict = {"R":[0,-25,-5,50,10,1,0,-1,0,(255,150,60),"R"],"C":[0,-25,-8,50,16,1,0,-1,0,(200,150,200),"C"]
	# ,"V":[0,-25,-10,50,20,1,0,-1,0,(255,0,0),"V"],"G":[0,-25,-10,50,20,1,0,1,0,(0,0,0),"G"]}

	# initialize Display
	Windowsize = (1000,720)
	pygame.init()
	clock = pygame.time.Clock()
	gameDisplay = pygame.display.set_mode(Windowsize)
	pygame.display.set_caption("cool circuit simulator 2000 😎 Now showing : " + title)
	# create component dictionary
	compdict = {0:None, 1:resistoricon, 2:capacitoricon, 3:inductoricon, 4:diodeicon, 5:vsourceicon, 6:csourceicon, 7:gndicon, 8:resistoricon, 9:opampicon}
	typedict = {1 : 'R', 2 : 'C', 3 : 'L', 4 : 'D', 5 : 'V', 6 : 'I', 7 : 'G', 8 : 'g', 9 : 'O'}
	gridspace = 25
	linethickness = 3
	lineColor = (0, 255, 255)
	backgroundColor = (150, 150, 150)
	status ="Good"
	# res =pygame.image.load(fileobj, namehint="")

x = 0
def render():
	"""Render the scene."""
	global currentComponent
	global componentOrientationRender
	global status
	global x
	gameDisplay.fill(backgroundColor)
	
	#write node names on statusbar when hovering on them
	foundsomething = False
	#if x > 2:
	#	x = 0
	#for c in components:
	#	if detectCollision(c, pygame.mouse.get_pos())[0]:
	#		if c[0] == 0:
	#			status = ("This is node " + str(nodes[components.index(c)]))
				#else:
				#	status = str(c[4])
	#		foundsomething = True
	if not deletemode and not graphMode and not foundsomething: 
			status = "good"
			#gameDisplay.fill(backgroundColor)

	#x+=1
	#write component names on statusbar when hovering on them
	
	#update statusbar with status
	Writeonstatusbar(status)	
	# Display node names on wires
	nodenames=[]
	for c in components:
		if c[0] == 0 and (len(nodes) > 0):
			text = "N" + str(nodes[components.index(c)])
			if not text in nodenames:
				nodenames.append(text)
				writeonscreen(text,(194, 87, 26),[c[2],c[3]])
	nodenames=[]
	# Displaying buttons
	# Parameters:           surface,      color,       x,   y,   length, height, width,    text,      text_color
	resistorButton.create_button(   gameDisplay, (160,160,160), 0 , 0   , 200    ,    40 ,    0, "Resistor", (0,0,0))
	capacitorButton.create_button(  gameDisplay, (160,160,160), 200 , 0   , 200    ,    40 ,    0, "Capacitor", (0,0,0))
	inductorButton.create_button(   gameDisplay, (160,160,160), 400 , 0   , 200    ,    40 ,    0, "Inductor", (0,0,0))
	diodeButton.create_button(      gameDisplay, (160,160,160), 600 , 0   , 200    ,    40 ,    0, "Diode", (0,0,0))
	vsourceButton.create_button(    gameDisplay, (160,160,160), 800 , 0   , 200    ,    40 ,    0, "Voltage source", (0,0,0))
	csourceButton.create_button(    gameDisplay, (160,160,160), 0 ,   40  , 200    ,    40 ,    0,"Current source", (0,0,0))
	gndButton.create_button(        gameDisplay, (160,160,160), 200 , 40   , 200    ,   40 ,    0, "Ground", (0,0,0))
	conductanceButton.create_button(gameDisplay, (160,160,160), 400 , 40   , 200    ,   40 ,    0, "Conductance", (0,0,0))
	opampButton.create_button(      gameDisplay, (160,160,160), 600 ,  40   , 200    ,  40 ,    0, "OPAMP", (0,0,0))
	rotateButton.create_button(     gameDisplay, (160,160,160), 800 , 40   , 200    ,   40 ,    0, "Rotate", (0,0,0))
	saveButton.create_button(       gameDisplay, (160,160,160), 0 ,   80   , 200    ,   40 ,    0, "Save", (0,0,0))
	netlistButton.create_button(    gameDisplay, (160,160,160), 200 , 80   , 200    ,   40 ,    0, "Netlist", (0,0,0))
	ACButton.create_button(         gameDisplay, (160,160,160), 400 , 80   , 200    ,   40 ,    0, "AC", (0,0,0))
	DCButton.create_button(         gameDisplay, (160,160,160), 600 , 80   , 200    ,   40 ,    0, "DC", (0,0,0))
	sweepButton.create_button(      gameDisplay, (160,160,160), 800 , 80   , 200    ,   40 ,    0, "Sweep", (0,0,0))
	changetitleButton.create_button(gameDisplay, (160,160,160), 0 , 120   ,  200    ,   40 ,    0, "Change Title", (0,0,0))
	deleteButton.create_button(     gameDisplay, (160,160,160), 200 , 120   , 200    ,  40 ,    0, "Delete", (0,0,0))
	graphButton.create_button(      gameDisplay, (160,160,160), 400 , 120   , 200    ,  40 ,    0, "Graph", (0,0,0))
	newButton.create_button(        gameDisplay, (160,160,160), 600 , 120   , 200    ,  40 ,    0, "New", (0,0,0))
	startsimButton.create_button(   gameDisplay, (160,160,160), 800 , 120   , 200    ,    40 ,    0, "Start simulation", (0,0,0))
	# Render components/wires currently being edited
	if drawingLine:
		if abs(initialCoordinates[0] - gridCoordinates[0]) >= abs(initialCoordinates[1] - gridCoordinates[1]):
			componentOrientationRender = 0
			pygame.draw.line(gameDisplay, lineColor, initialCoordinates, [gridCoordinates[0], initialCoordinates[1]],linethickness)
		else:
			componentOrientationRender = 1
			pygame.draw.line(gameDisplay, lineColor, initialCoordinates, [initialCoordinates[0], gridCoordinates[1]],linethickness)

	if drawingComponenet:
		compheight = compdict[currentComponent].get_rect().size[0]
		compwidth = compdict[currentComponent].get_rect().size[1]
		if currentComponent != 9:
			if componentOrientationRender == 0:
				gameDisplay.blit(compdict[currentComponent], (gridCoordinates[0] - (compheight / 2) + 1, gridCoordinates[1]))
			if componentOrientationRender == 1:
				compimage = pygame.transform.rotate(compdict[currentComponent], 270)
				gameDisplay.blit(compimage, (gridCoordinates[0], gridCoordinates[1] - (compheight / 2) + 1))
		if currentComponent == 9:
			if componentOrientationRender == 0:
				gameDisplay.blit(compdict[currentComponent], (gridCoordinates[0] - (compheight / 2), gridCoordinates[1]-(compwidth)))
			if componentOrientationRender == 1:
				compimage = pygame.transform.rotate(compdict[currentComponent], 270)
				gameDisplay.blit(compimage, (gridCoordinates[0], gridCoordinates[1] - (compheight / 2) + 1))
	# Render components
	if len(components) > 0:
		for c in components:
			#add wire joints
			if c[0] == 0:
				for n in components:
					if n[0] == 0:
						if n != c:
							if findCollisionWireWire(n,c)[0]:
								if findCollisionWireWire(n,c)[1] != None:
									joint = pygame.draw.rect(gameDisplay, (0,0,200), (findCollisionWireWire(n,c)[1][0]-3,findCollisionWireWire(n,c)[1][1]-3,8,8), 0)

			#rendering
			if c[1] == 1:
				if c[0] == 0:
					pygame.draw.line(gameDisplay, (0, 0, 255), [c[2], c[3]], [c[2] + c[5], c[3]], 2)
				elif c[0] != 0:
					compheight = compdict[c[0]].get_rect().size[0]
					compimage = compdict[c[0]]
					compimage = pygame.transform.rotate(compimage, 90)
					gameDisplay.blit(compimage, (c[2], c[3] - (compheight / 2) + 1))
					writeonscreen(c[4], (0, 255, 0), [c[2], c[3] - 30])
					if (c[0] in [1, 2, 3, 5, 6, 8]):
						writeonscreen("value " + str(c[5]), (0, 255, 0), [c[2], c[3] + 30])

			elif c[1] == 0:
				if c[0] == 0:
					pygame.draw.line(gameDisplay, (0, 0, 255), [c[2], c[3]], [c[2], c[3] + c[5]], 2)
				elif c[0] != 0 and c[0] != 9 :
					compheight = compdict[c[0]].get_rect().size[0]
					compwidth = compdict[c[0]].get_rect().size[1]
					compimage = compdict[c[0]]
					gameDisplay.blit(compimage, (c[2] - (compheight / 2) + 1, c[3]))
					writeonscreen(c[4], (0, 255, 0), [c[2] - 30, c[3]])
					if (c[0] in [1, 2, 3, 5, 6, 8]):
						writeonscreen("value " + str(c[5]), (0, 255, 0), [c[2] , c[3] + (compwidth/2)])
				elif c[0] == 9 :
					compheight = compdict[c[0]].get_rect().size[0]
					compwidth = compdict[c[0]].get_rect().size[1]
					compimage = compdict[c[0]]
					gameDisplay.blit(compimage, (c[2] - (compheight / 2) , c[3]-compwidth))
					writeonscreen(c[4], (0, 255, 0), [c[2] , c[3]])
			elif c[1] == 2:
				if c[0] == 0:
					pygame.draw.line(gameDisplay, (0, 0, 255), [c[2], c[3]], [c[2], c[3] + c[5]], 2)
				elif c[0] != 0:
					compheight = compdict[c[0]].get_rect().size[0]
					compwidth = compdict[c[0]].get_rect().size[1]
					compimage = compdict[c[0]]
					compimage = pygame.transform.rotate(compimage, 180)
					gameDisplay.blit(compimage, (c[2] - (compheight / 2) + 1, c[3]))
					writeonscreen(c[4], (0, 255, 0), [c[2] - 30, c[3]])
					if (c[0] in [1, 2, 3, 5, 6, 8]):
						writeonscreen("value " + str(c[5]), (0, 255, 0), [c[2] + 30, c[3]])
			elif c[1] == 3:
				if c[0] == 0:
					pygame.draw.line(gameDisplay, (0, 0, 255), [c[2], c[3]], [c[2], c[3] + c[5]], 2)
				elif c[0] != 0 :
					compheight = compdict[c[0]].get_rect().size[0]
					compwidth = compdict[c[0]].get_rect().size[1]
					compimage = compdict[c[0]]
					compimage = pygame.transform.rotate(compimage, 270)
					gameDisplay.blit(compimage, (c[2], c[3] - (compheight / 2) + 1))
					if c[0] != 9 :
						writeonscreen(c[4], (0, 255, 0), [c[2], c[3] - 30])
					if c[0] == 9 :
						writeonscreen(c[4], (0, 255, 0), [c[2], c[3] ])
					if (c[0] in [1, 2, 3, 5, 6, 8]):
						writeonscreen("value " + str(c[5]), (0, 255, 0), [c[2], c[3] - (compwidth)/2])
				# pygame.draw.rect(gameDisplay, (0,255,0), [c[2],c[3],100,20])
		
	
		# pygame.draw.rect(gameDisplay, i[4], flatten(i)[0:4])
	#render joints
	#for n in joints :
	#	pygame.draw.rect(gameDisplay, (0,0,255), (n[0]-2,n[1]-2,4,4), 0)


				# pygame.draw.rect(gameDisplay, i[4], flatten(i)[0:4])
	pygame.display.update()

def checkEvents():
	"""Check Pygame Events."""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return eventType.Quit, None
		elif event.type == pygame.MOUSEMOTION:
			# print(event.pos)
			return eventType.Mouse_Motion, event.pos
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				return eventType.Key_Down, "r"
			elif event.key == pygame.K_c:
				return eventType.Key_Down, "c"
			elif event.key == pygame.K_l:
				return eventType.Key_Down, "l"
			elif event.key == pygame.K_x:
				return eventType.Key_Down, "x"
			elif event.key == pygame.K_d:
				return eventType.Key_Down, "d"
			elif event.key == pygame.K_v:
				return eventType.Key_Down, "v"
			elif event.key == pygame.K_i:
				return eventType.Key_Down, "i"
			elif event.key == pygame.K_o:
				return eventType.Key_Down, "o"
			elif event.key == pygame.K_g:
				return eventType.Key_Down, "g"
			elif event.key == pygame.K_q:
				return eventType.Key_Down, "q"
			elif event.key == pygame.K_s:
				return eventType.Key_Down, "s"
			elif event.key == pygame.K_e:
				return eventType.Key_Down, "e"
			elif event.key == pygame.K_n:
				return eventType.Key_Down, "n"
			elif event.key == pygame.K_RETURN:
				return eventType.Key_Down, "return"
			elif event.key == pygame.K_DELETE:
				return eventType.Key_Down, "delete"
			else:
				return eventType.Key_Down, 0
		elif event.type == pygame.MOUSEBUTTONUP:
			if resistorButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "r"
			if capacitorButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "c"
			if inductorButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "l"
			if conductanceButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "x"
			if diodeButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "d"
			if vsourceButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "v"
			if csourceButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "i"
			if opampButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "o"
			if gndButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "g"
			if rotateButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "q"
			if saveButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "s"
			if netlistButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "n"
			if ACButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "ACButton"
			if DCButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "DCButton"
			if sweepButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "SweepButton"
			if deleteButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "delete"
			if graphButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "GraphButton"
			if newButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "new"
			if startsimButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "startsim"
			if changetitleButton.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "change"
			return eventType.Mouse_Up, None

	return 0, 0

def loadFile(fileName):
	"""Load a file into the simulator."""
	global title
	global components
	try:
		f = open(fileName, 'rb')
	except:
		return -1
	data = f.read()
	counter = 0
	magicno = chr(data[0]) + chr(data[1]) + chr(data[2]) + chr(data[3])
	if not(magicno == "CIR0"):
		print("Error")
		return -1

	counter = 20
	nameLength = int.from_bytes(data[counter:counter + 2], 'big')
	counter += 2
	title = ""
	for i in range(nameLength):
		title += chr(data[counter])
		counter += 1

	componentCount = int.from_bytes(data[counter:counter + 8], 'big')
	# print(componentCount)
	counter += 8
	reservedBits = int.from_bytes(data[counter:counter + 4], 'big')
	counter += 4 + reservedBits

	for i in range(componentCount):
		componentType = int.from_bytes(data[counter:counter + 4], 'big')
		counter += 4
		componentOrientation = int.from_bytes(data[counter:counter + 1], 'big')
		counter += 1
		componentCoordx = int.from_bytes(data[counter:counter + 4], 'big')
		counter += 4
		componentCoordy = int.from_bytes(data[counter:counter + 4], 'big')
		counter += 4
		componentNameLength = int.from_bytes(data[counter:counter + 2], 'big')
		counter += 2
		componentName = ""
		for i in range(componentNameLength):
			componentName += chr(data[counter])
			counter += 1

		componentValue = struct.unpack('!d', data[counter:counter + 8])[0]
		counter += 8
		print(componentType, componentOrientation, componentCoordx, componentCoordy, componentName, componentValue)
		print('-----')
		components.append([componentType, componentOrientation, componentCoordx, componentCoordy, componentName, componentValue])
		print (components)
		componentReserveLength = int.from_bytes(data[counter:counter + 4], 'big')
		counter += 4 + componentReserveLength

	return 0

def saveFile(fileName):
	"""Save current circuit to file."""
	f = open(fileName, 'wb+')
	f.write(bytes("CIR0", 'ascii'))
	for i in range(16):
		f.write(bytes(chr(0), 'ascii'))

	f.write(struct.pack("!H", len(title)))
	f.write(bytes(title, 'ascii'))

	f.write(struct.pack("!Q", len(components) + len(lines)))
	for i in range(4):
		f.write(bytes(chr(0), 'ascii'))

	for i in range(len(components)):
		f.write(struct.pack("!I", components[i][0]))
		f.write(struct.pack("!B", components[i][1]))
		f.write(struct.pack("!I", components[i][2]))
		f.write(struct.pack("!I", components[i][3]))
		f.write(struct.pack("!H", len(components[i][4])))
		f.write(bytes(components[i][4], 'ascii'))

		f.write(struct.pack('!d', components[i][5]))
		for i in range(4):
			f.write(bytes(chr(0), 'ascii'))
	print("saved")
	f.close()

def askForValue(text):
	finished = 0
	txtbx = eztext.Input(maxlength=50, color=(0, 255, 0), prompt=text)
	while not finished:
		# update txtbx
		clock.tick(60)
		events = pygame.event.get()
		val = txtbx.update(events)
		if val != None:
			finished = 1
		# blit txtbx on the sceen
		txtbx.draw(gameDisplay)
		pygame.display.flip()
		render()
	
	return val

def generateNetlist():
	"""Generate netlist for simulation."""
	global nodes
	global status
	nodes = [0 for i in components]
	connections = [[] for i in components]
	netlist = ""
	for i in range(len(components)):
		if not(components[i][0] == 0):
			nodes[i] = -1

	for i in range(len(nodes)):
		if nodes[i] == 0:
			nodes[i] = i
			connnod = findConnectedNodes(i, nodes)
			if not(connnod is None):
				for j in connnod:
					nodes[j] = i

	for i in range(len(components)):
		if (((components[i][0] >= 1) & (components[i][0] <= 6)) | (components[i][0] == 8)):
			for j in range(len(components)):
				if (components[j][0] == 0):
					if(findCollisionWirePoint(components[j], [components[i][2], components[i][3]])):
						connections[i].append("T1")
						connections[i].append(nodes[j])
					if(findCollisionWirePoint(components[j], [components[i][2], components[i][3] + 100]) & ~components[i][1]):
						connections[i].append("T2")
						connections[i].append(nodes[j])
					if(findCollisionWirePoint(components[j], [components[i][2] + 100, components[i][3]]) & components[i][1]):
						connections[i].append("T2")
						connections[i].append(nodes[j])
		if (components[i][0] == 7):
			for j in range(len(components)):
				if (components[j][0] == 0):
					if(findCollisionWirePoint(components[j], [components[i][2], components[i][3]])):
						connections[i].append("T1")
						connections[i].append(nodes[j])
		if (components[i][0] == 9):
			for j in range(len(components)):
				if (components[j][0] == 0):
					if not(components[i][1]):
						if(findCollisionWirePoint(components[j], [components[i][2] + 25, components[i][3]])):
							connections[i].append("T1")
							connections[i].append(nodes[j])
						if(findCollisionWirePoint(components[j], [components[i][2] - 25, components[i][3]])):
							connections[i].append("T2")
							connections[i].append(nodes[j])
						if(findCollisionWirePoint(components[j], [components[i][2], components[i][3] - 125])):
							connections[i].append("T3")
							connections[i].append(nodes[j])
					else:
						if(findCollisionWirePoint(components[j], [components[i][2], components[i][3] + 25])):
							connections[i].append("T1")
							connections[i].append(nodes[j])
						if(findCollisionWirePoint(components[j], [components[i][2], components[i][3] - 25])):
							connections[i].append("T2")
							connections[i].append(nodes[j])
						if(findCollisionWirePoint(components[j], [components[i][2] + 125, components[i][3]])):
							connections[i].append("T3")
							connections[i].append(nodes[j])

	# Short all grounds together
	short_to = -1
	for i in range(len(components)):
		if (components[i][0] == 7):
			if(short_to == -1):
				short_to = connections[i][1]
			short_from = connections[i][1]
			for j in range(len(nodes)):
				if (nodes[j] == short_from):
					nodes[j] = short_to
			for j in connections:
				for k in range(len(j)):
					if(j[k] == short_from):
						j[k] = short_to

	if (simType == "DC"):
		netlist += ".DC OP\n"
	elif (simType == "AC"):
		netlist += ".AC OP\n"
	elif (simType == "Sweep"):
		netlist += ".AC SWEEP FREQ " + ACParameters[2] + " " + str(ACParameters[0]) + " " + \
					str(ACParameters[1]) + " " + toGraph[1] + "\n"
		netlist += ".GRAPH " + toGraph[0] + " " + toGraph[1] + "\n"

	# Set ground to the ground node with .GND
	if (short_to > -1):
		netlist += ".GND N" + str(short_to) + "\n"
	else:
		print("ERROR : No ground node!")
		status = "ERROR : No ground node!"
		return

	# Add components one by one
	for i in range(len(components)):
		if(components[i][0] != 0) & (components[i][0] != 7):
			temp = ""
			compType = typedict[components[i][0]]
			if compType == "O":
				compType = "OPAMP3"
			temp += compType + " "
			temp += components[i][4] + " "
			t1 = -1
			t2 = -1
			t3 = -1
			for j in range(0, len(connections[i]), 2):
				if(connections[i][j] == "T1"):
					t1 = connections[i][j + 1]
				if(connections[i][j] == "T2"):
					t2 = connections[i][j + 1]
				if(connections[i][j] == "T3"):
					t3 = connections[i][j + 1]
			temp += "("
			if (t1 > -1):
				temp += "N" + str(t1) + ";"
			if (t2 > -1):
				temp += "N" + str(t2) + ";"
			if (t3 > -1):
				temp += "N" + str(t3) + ";"
			temp = temp[0:-1]
			temp += ") "
			if (components[i][0] in [1, 2, 3, 5, 6, 8]):
				temp += str(components[i][5]) + " "
			if (simType == "AC"):
				if (components[i][0] in [5, 6]):
					temp += str(ACParameters[0])
			temp += "\n"
			netlist += temp

	print(nodes)
	print(connections)
	print(netlist)
	figure1 = plt.figure(1)
	fig = figure1.add_subplot(111)
	fig.text(0.5, 0, netlist, fontsize=15)
	fig.axis([0, 10, 0, 10])
	plt.show()
	f = open("circuit.net", 'w+')
	f.write(netlist)
	f.close()
	status = "Netlist generated"

def findConnectedNodes(indexw1, mask):
	"""Find all nodes connected to a wire."""
	rrrrrr = []
	mmmmm = copy.copy(mask)
	for i in range(len(components)):
		if(components[i][0] == 0):
			if not(mask[i] == 0):
				continue
			else:
				if(findCollisionWireWire(components[indexw1], components[i])[0]):
					rrrrrr.append(i)
					mmmmm[i] = -1
					for j in rrrrrr:
						k = findConnectedNodes(j, mmmmm)
						for l in k:
							if not(rrrrrr.__contains__(l)):
								if(type(l) == int):
									rrrrrr.append(l)
								else:
									flattenml(l)
									rrrrrr.append(l[0])
	return rrrrrr


def findCollisionWireWire(wire1, wire2):
	"""Find if one wire ends on another."""
	if (findCollisionWirePoint(wire1, [wire2[2], wire2[3]])):
		if wire1[2] == wire2[2] and wire1[3]==wire2[3]:
			return True, None
		return True, [wire2[2], wire2[3]]
	if (findCollisionWirePoint(wire1, [wire2[2], wire2[3] + wire2[5]]) & ~wire2[1]):
		return True, [wire2[2], wire2[3] + wire2[5]]
	if (findCollisionWirePoint(wire1, [wire2[2] + wire2[5], wire2[3]]) & wire2[1]):
		return True, [wire2[2] + wire2[5], wire2[3]]

	if (findCollisionWirePoint(wire2, [wire1[2], wire1[3]])):
		if wire1[2] == wire2[2] and wire1[3]==wire2[3]:
			return True, None
		return True , [wire1[2], wire1[3]]
	if (findCollisionWirePoint(wire2, [wire1[2], wire1[3] + wire1[5]]) & ~wire1[1]):
		return True, [wire1[2], wire1[3] + wire1[5]]
		#return True, [wire1[2] + wire1[5], wire1[3]]
	if (findCollisionWirePoint(wire2, [wire1[2] + wire1[5], wire1[3]]) & wire1[1]):
		return True, [wire1[2] + wire1[5], wire1[3]]
		#return True, [wire1[2], wire1[3] + wire1[5]]
	return False, [0, 0]

def findCollisionWirePoint(wire, point):
	"""Find if a point lies on a wire."""
	if (wire[5] > 0):
		if((point[0] >= wire[2]) & (point[0] <= wire[2] + wire[5]) & (point[1] == wire[3]) & (wire[1])):
			return True
		if((point[1] >= wire[3]) & (point[1] <= wire[3] + wire[5]) & (point[0] == wire[2]) & ~(wire[1])):
			return True
	else:
		if((point[0] <= wire[2]) & (point[0] >= wire[2] + wire[5]) & (point[1] == wire[3]) & (wire[1])):
			return True
		if((point[1] <= wire[3]) & (point[1] >= wire[3] + wire[5]) & (point[0] == wire[2]) & ~(wire[1])):
			return True

	return False

def detectCollision(component, Coordinates):
	"""Find if coordinates are on a component."""
	global compdict
	global currentComponent
	global componentOrientationRender
	global status
	mouserect  = pygame.draw.rect(gameDisplay, (255,255,255), (Coordinates[0]-9,Coordinates[1]-9,20,20), 1)
	c = component
	if(component[0] != 0):
		compheight = compdict[component[0]].get_rect().size[0]
		compwidth  = compdict[component[0]].get_rect().size[1]
		#detect component collision
		if (component[1] == 0 or component[1] == 2):
			if component[0] != 9:
				comprect = pygame.draw.rect(gameDisplay, (255,255,255), (c[2]-compheight/2,c[3],compheight,compwidth), 1)
				pygame.display.flip()
			else:
				comprect = pygame.draw.rect(gameDisplay, (255,255,255), (c[2]-compheight/2,c[3]-compwidth,compheight,compwidth), 1)
				pygame.display.flip()
		elif (component[1] ==1 or component[1] ==3):
			if component[0] != 9:
				comprect = pygame.draw.rect(gameDisplay, (255,255,255), (c[2],c[3]-compheight/2,compwidth,compheight), 1)
				pygame.display.flip()
			else:
				comprect = pygame.draw.rect(gameDisplay, (255,255,255), (c[2],c[3]-compheight/2,compwidth,compheight), 1)
				pygame.display.flip()
		return comprect.colliderect(mouserect), component[0]
		#detect wire collision
	else:
		if component[1] == 1:
			line = pygame.draw.line(gameDisplay, (255, 255, 255), [component[2], component[3]], [component[2] + component[5], component[3]], 2)
		elif component[1] == 0:
			line = pygame.draw.line(gameDisplay, (255, 255, 255), [component[2], component[3]], [component[2], component[3] + component[5]], 2)
		return line.colliderect(mouserect), component[0]

	return False

def AC_analysis():
	"""Perform AC Analysis."""
	global simType
	global ACParameters
	global status
	print("AC analysis")
	simType = "AC"
	ACParameters = []
	frequency = float(getComponentValue(askForValue("Enter the desired freuency : ")).real)
	ACParameters.append(frequency)
	status = "AC analysis mode"


def DC_analysis():
	"""Perform DC Analysis."""
	global simType
	global status
	global ACParameters
	print("DC analysis")
	simType = "DC"
	status = "DC analysis mode"

def sweep_analysis():
	"""Perform Sweep Analysis."""
	global simType
	global status
	global ACParameters
	print("sweep analysis")
	ACParameters = []
	simType = "Sweep"
	status = "Sweep analysis mode"
	ACParameters.append(float(getComponentValue(askForValue("Enter the start freuency : ")).real))
	ACParameters.append(float(getComponentValue(askForValue("Enter the end freuency : ")).real))
	ACParameters.append(askForValue("Enter the source to sweep freuency : "))

def Changetitle():
	global title
	global status
	title = askForValue("Enter the new title : ")
	pygame.display.set_caption("cool circuit simulator 2000 😎 Now showing : " + title)
	status = "Title changed"

def Deduplicatewire():
	global nodes
	# DEDUP CODE

	# Remove zero length wires
	for c in components:
		if c[0] == 0 and c[5] == 0:
			components.remove(c)
	
	# Update nodes
	
	nodes = [0 for i in components]
	grounds = [0 for i in components]
	
	for i in range(len(components)):
		if not(components[i][0] == 0):
			nodes[i] = -1

	for i in range(len(nodes)):
		if nodes[i] == 0:
			nodes[i] = i
			connnod = findConnectedNodes(i, nodes)
			if not(connnod is None):
				for j in connnod:
					nodes[j] = i

	for i in range(len(components)):
		if (components[i][0] == 7):
			for j in range(len(components)):
				if (components[j][0] == 0):
					if(findCollisionWirePoint(components[j], [components[i][2], components[i][3]])):
						grounds[i] = nodes[j]

	short_to = -1
	for i in range(len(components)):
		if (components[i][0] == 7):
			if(short_to == -1):
				short_to = grounds[i]
			short_from = grounds[i]
			for j in range(len(nodes)):
				if (nodes[j] == short_from):
					nodes[j] = short_to
			for j in range(len(grounds)):
				if(grounds[j] == short_from):
					grounds[j] = short_to

def Newfile():
	global components
	global title
	components = []
	title = ""
	pygame.display.set_caption("cool circuit simulator 2000 😎 Now showing : " + title)

def Startsimulation():
	global status
	global Analyze
	Analyze = importlib.reload(Analyze)
	result = Analyze.__main__()
	status = "Simulation Done"

def kill():
	"""End Circuit Simulator."""
	saveFile("myfirstcir.cir")
	pygame.quit()
	quit()

# variables

# clock = 0
# gameDisplay = None
global status
killApp = False
drawingLine = False
drawingComponenet = False
global deletemode
deletemode = False
initialCoordinates = [0, 0]
componentOrientationRender = 0  # 0->H 1->v
gridCoordinates = [0, 0]
lines = []
verticalWire = False
simType = "DC"
ACParameters = []
components = []
joints =[]
title = ""
toGraph = ["N0", "N0"]
global graphMode
graphMode = False
# if(loadFile("myfirstcir.cir") == -1):
# 	kill()
loadFile("myfirstcir.cir")

initalize()
nodes = [0 for i in components]
#Deduplicatewire()
# main loop
while not killApp:
	time.sleep(0.05)
	returnedEvent, eventParameter = checkEvents()
	if (returnedEvent == eventType.Quit):
		killApp = True
# update grid coordinates every time the mouse moves
	elif (returnedEvent == eventType.Mouse_Motion):
		gridCoordinates = [snapToGrid(eventParameter[0], eventParameter[1], 25)[0], snapToGrid(eventParameter[0], eventParameter[1], 25)[1]]
		# print(gridCoordinates)
	# if key pressed start drawing a component
	elif (returnedEvent == eventType.Key_Down):
		if (eventParameter == "r"):
			drawingLine = False
			currentComponent = 1
			componentOrientationRender = 0
			drawingComponenet = not drawingComponenet
		if (eventParameter == "c"):
			drawingLine = False
			currentComponent = 2
			componentOrientationRender = 0
			drawingComponenet = not drawingComponenet
		if (eventParameter == "l"):
			drawingLine = False
			currentComponent = 3
			componentOrientationRender = 0
			drawingComponenet = not drawingComponenet
		if (eventParameter == "x"):
			drawingLine = False
			currentComponent = 8
			componentOrientationRender = 0
			drawingComponenet = not drawingComponenet
		if (eventParameter == "d"):
			drawingLine = False
			currentComponent = 4
			componentOrientationRender = 0
			drawingComponenet = not drawingComponenet
		if (eventParameter == "v"):
			drawingLine = False
			currentComponent = 5
			componentOrientationRender = 0
			drawingComponenet = not drawingComponenet
		if (eventParameter == "i"):
			drawingLine = False
			currentComponent = 6
			componentOrientationRender = 0
			drawingComponenet = not drawingComponenet
		if (eventParameter == "g"):
			drawingLine = False
			currentComponent = 7
			componentOrientationRender = 0
			drawingComponenet = not drawingComponenet
		if (eventParameter == "o"):
			drawingLine = False
			currentComponent = 9
			componentOrientationRender = 0
			drawingComponenet = not drawingComponenet
		if (eventParameter == "s"):
			#TODO
			saveFile("myfirstcir.cir")
			status = "Saved"
			pass
		if (eventParameter == "n"):
			generateNetlist()
		if (eventParameter == "ACButton"):
			AC_analysis()
		if (eventParameter == "DCButton"):
			DC_analysis()
		if (eventParameter == "SweepButton"):
			sweep_analysis()
		if (eventParameter == "GraphButton"):
			graphMode = ~graphMode
			deletemode = False
			if graphMode:
				status = "Graph mode"
			else:
				status = "Good"
		if (eventParameter == "change"):
			Changetitle()
		if (eventParameter == "new"):
			Newfile()
		if (eventParameter == "startsim"):
			Startsimulation()
		if (eventParameter == "delete"):
			#for c in components:
			#	if detectCollision(c, pygame.mouse.get_pos())[0]:
			#		components.remove(c)
			#	elif gridCoordinates == [c[2], c[3]]:
			#		components.remove(c)
			Deduplicatewire()
			deletemode = not deletemode
			graphMode = False
			if deletemode:
				status = "Delete mode"
			else:
				status = "Good"
		elif (eventParameter == "q"):
			componentOrientationRender = not componentOrientationRender
	# when mouse up
	elif (returnedEvent == eventType.Mouse_Up):
		if (deletemode == False) and (graphMode == False):
			# start drawing lines
			if ((drawingLine == False) & (drawingComponenet == False)):
				initialCoordinates = copy.copy(gridCoordinates)
				drawingLine = True
			# save drawn line
			elif drawingLine == True:
				linecount = 0
				for c in components:
					if c[4][0] == 'N':
						linecount += 1
				if (componentOrientationRender):
					components.append([0, 0, initialCoordinates[0], initialCoordinates[1], ("N" + str(linecount)), 
										gridCoordinates[1] - initialCoordinates[1]])
					Deduplicatewire()
					print(components)
					print("check")
				else:
					components.append([0, 1, initialCoordinates[0], initialCoordinates[1], ("N" + str(linecount)),
						gridCoordinates[0] - initialCoordinates[0]])
					Deduplicatewire()
					print(components)
				drawingLine = False
			# or save drawn component
			elif drawingComponenet == True:
				compcount = 0
				for c in components:
					if c[4][0] == typedict[currentComponent]:
						compcount += 1
				events = pygame.event.get()
				val = "0"
				if (currentComponent in [1, 2, 3, 5, 6, 8]):
					val = askForValue('type value here: ')
				drawingComponenet = False
				components.append([currentComponent, componentOrientationRender * 3 ,gridCoordinates[0], gridCoordinates[1],
									(typedict[currentComponent] + str(compcount)), float(getComponentValue(val).real)])
				print("saved")
				print(components)
		if deletemode:
			#pygame.draw.rect(gameDisplay, (0,0,0), (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],2,2), 0)
			foundsomething = False
			for c in components:
				if detectCollision(c, pygame.mouse.get_pos())[0]:
					components.remove(c)
					foundsomething = True
			if foundsomething == False:
				deletemode = False
				#elif gridCoordinates == [c[2], c[3]]:
					#components.remove(c)
		if graphMode:
			foundsomething = False
			for c in components:
				colDetector = detectCollision(c, pygame.mouse.get_pos())
				if colDetector[0] & (colDetector[1] == 0):
					toGraph[0] = toGraph[1]
					toGraph[1] = "N" + str(nodes[components.index(c)])
					if (toGraph[0] == "N0"):
						toGraph[0] = toGraph[1]
					foundsomething = True
					break
			if foundsomething == False:
				graphMode = False

	if deletemode | graphMode:
		drawingComponenet = False
		drawingLine = False
		if deletemode:
			status = "Delete mode"
		else:
			status = "Graph mode"
		
	render()
	clock.tick(60)

kill()
