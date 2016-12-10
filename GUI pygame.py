import pygame
import copy
import enum

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
	compdict = {"R":[0,-25,-5,50,10,-25,25],"C":[0,-25,-8,50,16,-25,25]}
	pygame.init()
	clock = pygame.time.Clock()
	gameDisplay = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("nema-zag circuit simulator 2000 😎")
	gridspace = 25
	linethickness = 3
	lineColor = (0,255,255)
	backgroundColor = (150,150,150)
	#res =pygame.image.load(fileobj, namehint="")

def render():
	global componentOrientation
	gameDisplay.fill(backgroundColor)

#Render components/wires currently being edited
	if drawingLine:
		if abs(initialCoordinates[0] - gridCoordinates[0]) >= abs(initialCoordinates[1] - gridCoordinates[1]):
			componentOrientation = 0
			pygame.draw.line(gameDisplay, lineColor, initialCoordinates, [gridCoordinates[0], initialCoordinates[1]],linethickness)
		else:
			componentOrientation = 1
			pygame.draw.line(gameDisplay, lineColor, initialCoordinates, [initialCoordinates[0], gridCoordinates[1]],linethickness)

	if drawingComponenet:
		if componentOrientation == 0:
			pygame.draw.rect(gameDisplay, (0,150,255), [gridCoordinates[0] + currentComponent[1], gridCoordinates[1]+ currentComponent[2], currentComponent[3], currentComponent[4]])
		if componentOrientation == 1:
			pygame.draw.rect(gameDisplay, (0,150,255), [gridCoordinates[0] + currentComponent[2], gridCoordinates[1] + currentComponent[1], currentComponent[4], currentComponent[3]])

#Render current components/wires
	if len(lines) > 0:
		for i in lines :
			pygame.draw.line(gameDisplay, lineColor, i[0], i[1],linethickness)
	
	if len(components) > 0:
		for i in components:
			pygame.draw.rect(gameDisplay, (0,150,255), flatten(i)[0:4])

	pygame.display.update()

def checkEvents():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return eventType.Quit, None
		elif event.type == pygame.MOUSEMOTION:
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

def kill():
	pygame.quit()

#variables

# clock = 0
# gameDisplay = None
killApp = False
drawingLine = False
drawingComponenet = False
currentComponent = None
initialCoordinates = [0, 0]
componentOrientation = 0 #0->H 1->v
gridCoordinates = [0, 0]
lines = []
components = []
verticalWire = False

initalize()

#main loop
while not killApp:
	returnedEvent, eventParameter = checkEvents()
	if (returnedEvent == eventType.Quit):
		killApp = True
#update grid coordinates every time the mouse moves 
	elif (returnedEvent == eventType.Mouse_Motion):
		gridCoordinates = snapToGrid(eventParameter[0], eventParameter[1],25)
#if key pressed start drawing a component
	elif (returnedEvent == eventType.Key_Down):
		if (eventParameter == "s"):
			drawingLine = False
			currentComponent = compdict["R"]
			componentOrientation = 0
			drawingComponenet = not drawingComponenet
		if (eventParameter == "c"):
			drawingLine = False
			currentComponent = compdict["C"]
			componentOrientation = 0
			drawingComponenet = not drawingComponenet
		elif (eventParameter == "r"):
			componentOrientation = not componentOrientation
#when mouse up
	elif (returnedEvent == eventType.Mouse_Up):
#start drawing lines
		if ((drawingLine == False) & (drawingComponenet == False)):
			initialCoordinates = copy.copy(gridCoordinates)
			drawingLine = True
#save drawn line
		elif drawingLine == True:
			if (componentOrientation):
				lines.append([initialCoordinates, [initialCoordinates[0], gridCoordinates[1]]])
			else:
				lines.append([initialCoordinates, [gridCoordinates[0], initialCoordinates[1]]])
			drawingLine = False
#or save drawn component
		elif drawingComponenet == True:
			drawingComponenet = False
			if componentOrientation == 0:
				components.append([[gridCoordinates[0] + currentComponent[1], gridCoordinates[1] + currentComponent[2]], [currentComponent[3], currentComponent[4]]])
			if componentOrientation == 1:
				components.append([[gridCoordinates[0] + currentComponent[2], gridCoordinates[1] + currentComponent[1]], [currentComponent[4], currentComponent[3]],[currentComponent[5],currentComponent[6]]])
	render()
	clock.tick(60)

kill()