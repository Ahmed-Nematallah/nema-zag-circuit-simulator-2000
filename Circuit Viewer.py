import pygame , Buttons
import copy
import enum
import sys
import struct
import ctypes
import numpy as np
import matplotlib.pyplot as plt
from pygame.locals import *
import pygame, sys, eztext
eventType = enum.Enum("eventType", "Quit Mouse_Motion Key_Down Mouse_Up")


def snapToGrid(x, y, gridspace):
	if (x % gridspace < gridspace / 2):
		x = x - (x % gridspace)
	else:
		x = (x + gridspace)  - (x % gridspace)
	if (y % gridspace < gridspace / 2):
		y = y - (y % gridspace)
	else:
		y = (y + gridspace) - (y % gridspace)
	return x,y

def flatten(listOfLists):
	"Flatten one level of nesting"
	z = [x for sublist in listOfLists for x in sublist]
	return z

def flattenml(listOfLists):
	listOfLists2 = copy.deepcopy(listOfLists)
	while not(type(listOfLists2[0]) == int):
		listOfLists3 = flatten(listOfLists2)
		listOfLists2 = copy.deepcopy(listOfLists3)

	return listOfLists2


global font
pygame.font.init()
font = pygame.font.SysFont(None, 25)
def writeonscreen(text,color,pos):
	screentext = font.render(text,True,color)
	gameDisplay.blit(screentext,pos)
# create Buttons
buttonnamelist=["Resistor","Capacitor","Inductor","Diode","Voltage source","Current source","Ground","conductance","OPAMP"]
buttonlist = []
#for b in buttonnamelist:
 #   button = Buttons.Button()
#	buttonlist.append(button)
	
resistor = Buttons.Button()
capacitor = Buttons.Button()
inductor = Buttons.Button()
diode = Buttons.Button()
vsource = Buttons.Button()
csource = Buttons.Button()
gnd = Buttons.Button()
conductance = Buttons.Button()
opamp = Buttons.Button()
rotate = Buttons.Button()
save = Buttons.Button()
netlist = Buttons.Button()
AC = Buttons.Button()
DC = Buttons.Button()
sweep = Buttons.Button()

def initalize():
	global gameDisplay
	global clock
	global gridspace
	global linethickness
	global lineColor
	global backgroundColor
	global compdict
	global typedict
	global currentComponent
	#load component icons
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


	print (resistoricon.get_rect().size[1]) # you can get size
	# , draw coordinates,width and length,start and end point in grid coordinates, color , type
	#compdict = {"R":[0,-25,-5,50,10,1,0,-1,0,(255,150,60),"R"],"C":[0,-25,-8,50,16,1,0,-1,0,(200,150,200),"C"]
	#,"V":[0,-25,-10,50,20,1,0,-1,0,(255,0,0),"V"],"G":[0,-25,-10,50,20,1,0,1,0,(0,0,0),"G"]}
	
#create buttons

	#create component dictionary
	compdict = {0:None,1:resistoricon,2:capacitoricon,3:inductoricon,4:diodeicon,5:vsourceicon,6:csourceicon,7:gndicon,8:resistoricon,9:opampicon}
	typedict={1:'R',2:'C',3:'L',4:'D',5:'V',6:'I',7:'G',8:'g',9:'O'}
	pygame.init()
	clock = pygame.time.Clock()
	gameDisplay = pygame.display.set_mode((1000,720))
	pygame.display.set_caption("cool circuit simulator 2000 😎 Now showing : " + title)
	gridspace = 25
	linethickness = 3
	lineColor = (0,255,255)
	backgroundColor = (150,150,150)
	#res =pygame.image.load(fileobj, namehint="")

def render():
	global currentComponent
	global componentOrientationRender
	gameDisplay.fill(backgroundColor)

#Displaying buttons
		#Parameters:           surface,      color,       x,   y,   length, height, width,    text,      text_color

	resistor.create_button(   gameDisplay, (160,160,160), 0 , 0   , 200    ,    40 ,    0, "Resistor", (0,0,0))
	capacitor.create_button(  gameDisplay, (160,160,160), 200 , 0   , 200    ,    40 ,    0, "Capacitor", (0,0,0))
	inductor.create_button(   gameDisplay, (160,160,160), 400 , 0   , 200    ,    40 ,    0, "Inductor", (0,0,0))
	diode.create_button(      gameDisplay, (160,160,160), 600 , 0   , 200    ,    40 ,    0, "Diode", (0,0,0))
	vsource.create_button(    gameDisplay, (160,160,160), 800 , 0   , 200    ,    40 ,    0, "Voltage source", (0,0,0))
	csource.create_button(    gameDisplay, (160,160,160), 0 ,   40  , 200    ,    40 ,   0, "Current source", (0,0,0))
	gnd.create_button(        gameDisplay, (160,160,160), 200 , 40   , 200    ,    40 ,    0, "Ground", (0,0,0))
	conductance.create_button(gameDisplay, (160,160,160), 400 , 40   , 200    ,    40 ,    0, "Conductance", (0,0,0))
	opamp.create_button(      gameDisplay, (160,160,160), 600 ,  40   , 200    ,    40 ,    0, "OPAMP", (0,0,0))
	rotate.create_button(     gameDisplay, (160,160,160), 800 , 40   , 200    ,    40 ,    0, "Rotate", (0,0,0))
	save.create_button(       gameDisplay, (160,160,160), 0 ,   80   , 200    ,    40 ,    0, "Save", (0,0,0))
	netlist.create_button(    gameDisplay, (160,160,160), 200 , 80   , 200    ,    40 ,    0, "Netlist", (0,0,0))
	AC.create_button(         gameDisplay, (160,160,160), 400 , 80   , 200    ,    40 ,    0, "AC", (0,0,0))
	DC.create_button(         gameDisplay, (160,160,160), 600 , 80   , 200    ,    40 ,    0, "DC", (0,0,0))
	sweep.create_button(      gameDisplay, (160,160,160), 800 , 80   , 200    ,    40 ,    0, "Sweep", (0,0,0))
	
#Render components/wires currently being edited
	if drawingLine:
		if abs(initialCoordinates[0] - gridCoordinates[0]) >= abs(initialCoordinates[1] - gridCoordinates[1]):
			componentOrientationRender = 0
			pygame.draw.line(gameDisplay, lineColor, initialCoordinates, [gridCoordinates[0], initialCoordinates[1]],linethickness)
		else:
			componentOrientationRender = 1
			pygame.draw.line(gameDisplay, lineColor, initialCoordinates, [initialCoordinates[0], gridCoordinates[1]],linethickness)

	if drawingComponenet:
		compheight = compdict[currentComponent].get_rect().size[0]
		if componentOrientationRender == 0:
			gameDisplay.blit(compdict[currentComponent],(gridCoordinates[0]-(compheight/2)+1,gridCoordinates[1]))
		if componentOrientationRender == 1:
			compimage = pygame.transform.rotate(compdict[currentComponent], 270)
			gameDisplay.blit(compimage,(gridCoordinates[0],gridCoordinates[1]-(compheight/2)+1))


#Render components
	if len(components) > 0:
		for c in components:
			if c[1] == 1:
				if c[0] == 0:
					pygame.draw.line(gameDisplay, (0,0,255), [c[2],c[3]], [c[2]+c[5],c[3]],2)
				elif c[0]!= 0 :
					compheight = compdict[c[0]].get_rect().size[0]
					compimage = compdict[c[0]]
					compimage = pygame.transform.rotate(compimage, 90)
					gameDisplay.blit(compimage,(c[2],c[3]-(compheight/2)+1))
					writeonscreen(c[4],(0,255,0),[c[2],c[3]-30])
					writeonscreen("value "+str(c[5]),(0,255,0),[c[2],c[3]+30])
			elif c[1]==0:
				if c[0] == 0:
					pygame.draw.line(gameDisplay, (0,0,255), [c[2],c[3]], [c[2],c[3]+c[5]],2)
				elif c[0]!= 0 :
					compheight = compdict[c[0]].get_rect().size[0]
					compimage = compdict[c[0]]
					gameDisplay.blit(compimage,(c[2]-(compheight/2)+1,c[3]))
					writeonscreen(c[4],(0,255,0),[c[2]-30,c[3]])
					writeonscreen("value "+str(c[5]),(0,255,0),[c[2]+30,c[3]])
			elif c[1]==2:
				if c[0] == 0:
					pygame.draw.line(gameDisplay, (0,0,255), [c[2],c[3]], [c[2],c[3]+c[5]],2)
				elif c[0]!= 0 :
					compheight = compdict[c[0]].get_rect().size[0]
					compimage = compdict[c[0]]
					compimage = pygame.transform.rotate(compimage, 180)
					gameDisplay.blit(compimage,(c[2]-(compheight/2)+1,c[3]))
					writeonscreen(c[4],(0,255,0),[c[2]-30,c[3]])
					writeonscreen("value "+str(c[5]),(0,255,0),[c[2]+30,c[3]])
			elif c[1]==3:
				if c[0] == 0:
					pygame.draw.line(gameDisplay, (0,0,255), [c[2],c[3]], [c[2],c[3]+c[5]],2)
				elif c[0]!= 0 :
					compheight = compdict[c[0]].get_rect().size[0]
					compimage = compdict[c[0]]
					compimage = pygame.transform.rotate(compimage, 270)
					gameDisplay.blit(compimage,(c[2],c[3]-(compheight/2)+1))
					writeonscreen(c[4],(0,255,0),[c[2],c[3]-30])
					writeonscreen("value "+str(c[5]),(0,255,0),[c[2],c[3]+30])
				#pygame.draw.rect(gameDisplay, (0,255,0), [c[2],c[3],100,20])

		#pygame.draw.rect(gameDisplay, i[4], flatten(i)[0:4])
	pygame.display.update()

def checkEvents():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return eventType.Quit, None
		elif event.type == pygame.MOUSEMOTION:
			#print(event.pos)
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
			if resistor.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "r"
			if capacitor.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "c"
			if inductor.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "l"
			if conductance.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "x"
			if diode.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "d"
			if vsource.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "v"
			if csource.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "i"
			if opamp.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "o"
			if gnd.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "g"
			if rotate.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "q"
			if save.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "s"
			if netlist.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "n"
			if AC.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "1"
			if DC.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "2"
			if sweep.pressed(pygame.mouse.get_pos()):
				return eventType.Key_Down, "3"
			return eventType.Mouse_Up, None

	return 0, 0

def loadFile(fileName):
	global title
	global components
	f = open(fileName, 'rb')
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
	#print(componentCount)
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
		print(componentType,componentOrientation,componentCoordx,componentCoordy,componentName,componentValue)
		print('-----')
		components.append([componentType,componentOrientation,componentCoordx,componentCoordy,componentName,componentValue])
		print (components)
		componentReserveLength = int.from_bytes(data[counter:counter + 4], 'big')
		counter += 4 + componentReserveLength

	return 0

def saveFile(fileName):
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

def generateNetlist():
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
			if not(connnod == None):
				for j in connnod:
					nodes[j] = i

	for i in range(len(components)):
		if (((components[i][0] >= 1) & (components[i][0] <= 6)) | (components[i][0] == 8)):
			for j in range(len(components)):
				if (components[j][0] == 0):
					if(findCollisionWirePoint(components[j], [components[i][2], components[i][3]])):
						connections[i].append(nodes[j])
					if(findCollisionWirePoint(components[j], [components[i][2], components[i][3] + 100]) & ~components[i][1]):
						connections[i].append(nodes[j])
					if(findCollisionWirePoint(components[j], [components[i][2] + 100, components[i][3]]) & components[i][1]):
						connections[i].append(nodes[j])
		if (components[i][0] == 7):
			for j in range(len(components)):
				if (components[j][0] == 0):
					if(findCollisionWirePoint(components[j], [components[i][2], components[i][3]])):
						connections[i].append(nodes[j])
		if (components[i][0] == 9):
			for j in range(len(components)):
				if (components[j][0] == 0):
					if (components[i][1]):
						if(findCollisionWirePoint(components[j], [components[i][2] + 25, components[i][3]])):
							connections[i].append(nodes[j])
						if(findCollisionWirePoint(components[j], [components[i][2] - 25, components[i][3]])):
							connections[i].append(nodes[j])
						if(findCollisionWirePoint(components[j], [components[i][2], components[i][3] + 100])):
							connections[i].append(nodes[j])
					else:
						if(findCollisionWirePoint(components[j], [components[i][2], components[i][3] + 25])):
							connections[i].append(nodes[j])
						if(findCollisionWirePoint(components[j], [components[i][2], components[i][3] - 25])):
							connections[i].append(nodes[j])
						if(findCollisionWirePoint(components[j], [components[i][2] + 100, components[i][3]])):
							connections[i].append(nodes[j])
	
	print(nodes)
	print(connections)

def findConnectedNodes(indexw1, mask):
	rrrrrr = []
	mmmmm = copy.copy(mask)
	for i in range(len(components)):
		if(components[i][0] == 0):
			if not(mask[i] == 0):
				continue
			else:
				if(findWireCollision(components[indexw1], components[i])):
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


def findWireCollision(wire1, wire2):
	if (findCollisionWirePoint(wire1, [wire2[2], wire2[3]])):
		return True
	if (findCollisionWirePoint(wire1, [wire2[2] + wire2[5], wire2[3]]) & ~wire1[1]):
		return True
	if (findCollisionWirePoint(wire1, [wire2[2], wire2[3] + wire2[5]]) & wire1[1]):
		return True
	if (findCollisionWirePoint(wire2, [wire1[2], wire1[3]])):
		return True
	if (findCollisionWirePoint(wire2, [wire1[2] + wire1[5], wire1[3]]) & ~wire2[1]):
		return True
	if (findCollisionWirePoint(wire2, [wire1[2], wire1[3] + wire1[5]]) & wire2[1]):
		return True
	return False

def findCollisionWirePoint(wire, point):
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
	global compdict
	compheight = 100
	compwidth = 100
	if(component[1] == 0):
		#compheight = compdict[c[0]].get_rect().size[1]
		#compwidth = compdict[c[0]].get_rect().size[0]
		if ((Coordinates[0] > c[2] - compwidth / 2) & (Coordinates[0] < (c[2] + compwidth / 2)) & 
			(Coordinates[1] > c[3]) & (Coordinates[1] < (c[3] + compheight))):
			return True
		else:
			return False
	else:
	# 	compheight = compdict[c[0]].get_rect().size[0]
	# 	compwidth = compdict[c[0]].get_rect().size[1]
		if ((Coordinates[0] > c[2]) & (Coordinates[0] < (c[2] + compwidth)) & 
			(Coordinates[1] > c[3] - compheight / 2) & (Coordinates[1] < (c[3] + compheight / 2))):
			return True
		else:
			return False
		

	return False
def AC_analysis():
	print("AC analysis")
	pass

def DC_analysis():
	print("DC analysis")
	pass

def sweep_analysis():
	print("sweep analysis")
	pass

def kill():
	saveFile("123.txt")
	pygame.quit()
	quit()

#variables

# clock = 0
# gameDisplay = None
killApp = False
drawingLine = False
drawingComponenet = False
initialCoordinates = [0, 0]
componentOrientationRender = 0 #0->H 1->v
gridCoordinates = [0, 0]
lines = []
verticalWire = False
global components
components = []
if(loadFile("123.txt") == -1):
	kill()

initalize()

#main loop
while not killApp:
	returnedEvent, eventParameter = checkEvents()
	if (returnedEvent == eventType.Quit):
		killApp = True
#update grid coordinates every time the mouse moves
	elif (returnedEvent == eventType.Mouse_Motion):
		gridCoordinates = [snapToGrid(eventParameter[0], eventParameter[1],25)[0],snapToGrid(eventParameter[0], eventParameter[1],25)[1]]
		#print(gridCoordinates)
#if key pressed start drawing a component
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
			writeonscreen("saved",(255,0,0),[750,550])
			pass
		if (eventParameter == "n"):
			generateNetlist()
		if (eventParameter == "1"):
			AC_analysis()
		if (eventParameter == "2"):
			DC_analysis()
		if (eventParameter == "3"):
			sweep_analysis()
		if (eventParameter == "delete"):
			for c in components:
				if detectCollision(c, gridCoordinates):
					components.remove(c)
				elif gridCoordinates == [c[2],c[3]]:
					components.remove(c)
		elif (eventParameter == "q"):
			componentOrientationRender = not componentOrientationRender
#when mouse up
	elif (returnedEvent == eventType.Mouse_Up):
#start drawing lines
		if ((drawingLine == False) & (drawingComponenet == False)):
			initialCoordinates = copy.copy(gridCoordinates)
			drawingLine = True
#save drawn line
		elif drawingLine == True:
			linecount = 0
			for c in components:
				if c[4][0]=='N':
					linecount+=1
			if (componentOrientationRender):
				components.append([0,0,initialCoordinates[0],initialCoordinates[1],("N"+str(linecount)),gridCoordinates[1]-initialCoordinates[1]])
				print(components)
				print("check")
			else:
				components.append([0,1,initialCoordinates[0],initialCoordinates[1],("N"+str(linecount)),gridCoordinates[0]-initialCoordinates[0]])
				print(components)
			drawingLine = False
#or save drawn component
		elif drawingComponenet == True:
			compcount = 0
			for c in components:
				if c[4][0]==typedict[currentComponent]:
					compcount+=1
			drawingComponenet = False
			if componentOrientationRender == 0:
				finished = 0
				txtbx = eztext.Input(maxlength=45, color=(0,255,0), prompt='type value here: ')
				while not finished:
					# update txtbx
					clock.tick(60)
					events = pygame.event.get()
					val =txtbx.update(events)
					if val != None :
						finished = 1
					# blit txtbx on the sceen
					txtbx.draw(gameDisplay)
					pygame.display.flip()
				components.append([currentComponent,0,gridCoordinates[0],gridCoordinates[1],(typedict[currentComponent]+str(compcount)),float(val)])
				print("saved 0")
				print(components)
			if componentOrientationRender == 1:
				events = pygame.event.get()
				finished = 0
				txtbx = eztext.Input(maxlength=45, color=(255,0,0), prompt='type value here: ')
				while not finished:
					# update txtbx
					clock.tick(60)
					events = pygame.event.get()
					val =txtbx.update(events)
					if val != None :
						finished = 1
					# blit txtbx on the sceen
					txtbx.draw(gameDisplay)
					pygame.display.flip()
				components.append([currentComponent,3,gridCoordinates[0],gridCoordinates[1],(typedict[currentComponent]+str(compcount)),float(val)])
				print("saved 1")
				print(components)
	render()
	clock.tick(60)

kill()