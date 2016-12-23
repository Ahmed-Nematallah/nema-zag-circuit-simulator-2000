import pygame
import copy
import enum
import sys
import struct

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

def initalize():
	global gameDisplay
	global clock
	global gridspace
	global linethickness
	global lineColor
	global backgroundColor
	global compdict
	resistoricon = pygame.image.load('Resources/res.png')
	capacitoricon = pygame.image.load('Resources/Capacitor_Symbol.png')
	diodeicon = pygame.image.load('Resources/Diode_symbol.png')
	inductoricon = pygame.image.load('Resources/Inductor.png')
	vsourceicon = pygame.image.load('Resources/Voltage_source.png')
	# , draw coordinates,width and length,start and end point in grid coordinates, color , type 
	#compdict = {"R":[0,-25,-5,50,10,1,0,-1,0,(255,150,60),"R"],"C":[0,-25,-8,50,16,1,0,-1,0,(200,150,200),"C"]
	#,"V":[0,-25,-10,50,20,1,0,-1,0,(255,0,0),"V"],"G":[0,-25,-10,50,20,1,0,1,0,(0,0,0),"G"]}
	compdict = {0:None,1:resistoricon,2:capacitoricon,3:inductoricon,4:diodeicon,5:vsourceicon}
	pygame.init()
	clock = pygame.time.Clock()
	gameDisplay = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("nema-zag circuit simulator 2000 😎 Now showing : " + title)
	gridspace = 25
	linethickness = 3
	lineColor = (0,255,255)
	backgroundColor = (150,150,150)
	#res =pygame.image.load(fileobj, namehint="")

def render():
	global componentOrientationRender
	gameDisplay.fill(backgroundColor)

#Render components
	if len(components) > 0:
		for c in components:
			if c[0] == 0:
				pygame.draw.line(gameDisplay, (0,0,255), [c[2],c[3]], [c[2]+(c[5]*c[1]),c[3]+(c[5]*~c[1])],3)
			else:
				gameDisplay.blit(compdict[c[0]],(c[2],c[3]))
				#pygame.draw.rect(gameDisplay, (0,255,0), [c[2],c[3],100,20])
	
		#	pygame.draw.rect(gameDisplay, i[4], flatten(i)[0:4])

	pygame.display.update()

def checkEvents():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return eventType.Quit, None
		elif event.type == pygame.MOUSEMOTION:
			print(event.pos)
			return eventType.Mouse_Motion, event.pos
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_s:
				return eventType.Key_Down, "s"
			elif event.key == pygame.K_r:
				return eventType.Key_Down, "r"
			elif event.key == pygame.K_l:
				return eventType.Key_Down, "l"
			elif event.key == pygame.K_o:
				return eventType.Key_Down, "o"
			elif event.key == pygame.K_v:
				return eventType.Key_Down, "v"
			elif event.key == pygame.K_g:
				return eventType.Key_Down, "g"
			elif event.key == pygame.K_c:
				return eventType.Key_Down, "c"
			else:
				return eventType.Key_Down, 0
		elif event.type == pygame.MOUSEBUTTONUP:
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

def generateNetlist():
		nodes = []
		netlist = []
def kill():
	pygame.quit()
	quit()

#variables

# clock = 0
# gameDisplay = None
killApp = False
drawingLine = False
drawingComponenet = False
currentComponent = None
initialCoordinates = [0, 0]
componentOrientationRender = 0 #0->H 1->v
gridCoordinates = [0, 0]
lines = []
verticalWire = False
global components 
components = []
if(loadFile("Adder.cir") == -1):
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
		if (eventParameter == "s"):
			drawingLine = False
			currentComponent = compdict["R"]
			componentOrientationRender = 0
			drawingComponenet = not drawingComponenet
		if (eventParameter == "c"):
			drawingLine = False
			currentComponent = compdict["C"]
			componentOrientationRender = 0
			drawingComponenet = not drawingComponenet
		if (eventParameter == "g"):
			drawingLine = False
			currentComponent = compdict["G"]
			componentOrientationRender = 0
			drawingComponenet = not drawingComponenet
		if (eventParameter == "v"):
			drawingLine = False
			currentComponent = compdict["V"]
			componentOrientationRender = 0
			drawingComponenet = not drawingComponenet
		elif (eventParameter == "r"):
			componentOrientationRender = not componentOrientationRender
#when mouse up
	elif (returnedEvent == eventType.Mouse_Up):
#start drawing lines
		if ((drawingLine == False) & (drawingComponenet == False)):
			initialCoordinates = copy.copy(gridCoordinates)
			drawingLine = True
#save drawn line
		elif drawingLine == True:
			if (componentOrientationRender):
				lines.append([initialCoordinates, [initialCoordinates[0], gridCoordinates[1]]])
				print(lines)
			else:
				lines.append([initialCoordinates, [gridCoordinates[0], initialCoordinates[1]]])
				print(lines)
			drawingLine = False
#or save drawn component
		elif drawingComponenet == True:
			drawingComponenet = False
			if componentOrientationRender == 0:
				components.append([[gridCoordinates[0] + currentComponent[1], gridCoordinates[1] + currentComponent[2]], [currentComponent[3], currentComponent[4]],[gridCoordinates[0] +currentComponent[5]*gridspace,gridCoordinates[1] +currentComponent[6]*gridspace],[gridCoordinates[0] +currentComponent[7]*gridspace,gridCoordinates[1] +currentComponent[8]*gridspace],currentComponent[9],currentComponent[10]])
			if componentOrientationRender == 1:
				components.append([[gridCoordinates[0] + currentComponent[2], gridCoordinates[1] + currentComponent[1]], [currentComponent[4], currentComponent[3]],[gridCoordinates[0] +currentComponent[6]*gridspace,gridCoordinates[1] +currentComponent[5]*gridspace],[gridCoordinates[0] +currentComponent[8]*gridspace,gridCoordinates[1] +currentComponent[7]*gridspace],currentComponent[9],currentComponent[10]])
	render()
	clock.tick(60)

kill()