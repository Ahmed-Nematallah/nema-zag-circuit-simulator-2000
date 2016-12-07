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
	pygame.init()
	clock = pygame.time.Clock()
	gameDisplay = pygame.display.set_mode((800, 600))
	pygame.display.set_caption("nema-zag circuit simulator 2000 😎")
    #res =pygame.image.load(fileobj, namehint="")

def render():
	global componentOrientation
	gameDisplay.fill((150,150,150))

	#Render components/wires currently being edited
	if drawingLine:
		if abs(initialCoordinates[0] - gridCoordinates[0]) >= abs(initialCoordinates[1] - gridCoordinates[1]):
			componentOrientation = 0
			pygame.draw.line(gameDisplay, (0,255,255), initialCoordinates, [gridCoordinates[0], initialCoordinates[1]],3)
		else:
			componentOrientation = 1
			pygame.draw.line(gameDisplay, (0,255,255), initialCoordinates, [initialCoordinates[0], gridCoordinates[1]],3)
	
	if drawingComponenet:
		if componentOrientation == 0:
			pygame.draw.rect(gameDisplay, (0,150,255), [gridCoordinates[0] - 25, gridCoordinates[1] - 5, 50, 10])
		if componentOrientation == 1:
			pygame.draw.rect(gameDisplay, (0,150,255), [gridCoordinates[0] - 5, gridCoordinates[1] - 25, 10, 50])

	#Render current components/wires
	if len(lines) > 0:
		for i in lines :
			pygame.draw.line(gameDisplay, (0, 255, 255), i[0], i[1],3)
	
	if len(components) > 0:
		for i in components:
			pygame.draw.rect(gameDisplay, (0,150,255), flatten(i))

	pygame.display.update()

def checkEvents():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			return eventType.Quit, None
		elif event.type == pygame.MOUSEMOTION:
			return eventType.Mouse_Motion, event.pos
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_c:
				return eventType.Key_Down, "c"
			elif event.key == pygame.K_r:
				return eventType.Key_Down, "r"
			else:
				return eventType.Key_Down, 0
		elif event.type == pygame.MOUSEBUTTONUP:
			return eventType.Mouse_Up, None
	
	return 0, 0

def kill():
	pygame.quit()

# clock = 0
# gameDisplay = None
killApp = False
drawingLine = False
drawingComponenet = False
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
	elif (returnedEvent == eventType.Mouse_Motion):
		gridCoordinates = snapToGrid(eventParameter[0], eventParameter[1],25)
	elif (returnedEvent == eventType.Key_Down):
		if (eventParameter == "c"):
			drawingLine = False
			componentOrientation = 0
			drawingComponenet = not drawingComponenet
		elif (eventParameter == "r"):
			componentOrientation = not componentOrientation
	elif (returnedEvent == eventType.Mouse_Up):
		if ((drawingLine == False) & (drawingComponenet == False)):
			initialCoordinates = copy.copy(gridCoordinates)
			drawingLine = True
		elif drawingLine == True:
			if (componentOrientation):
				lines.append([initialCoordinates, [initialCoordinates[0], gridCoordinates[1]]])
			else:
				lines.append([initialCoordinates, [gridCoordinates[0], initialCoordinates[1]]])
			drawingLine = False
		elif drawingComponenet == True:
			drawingComponenet = False
			if componentOrientation == 0:
				components.append([[gridCoordinates[0] - 25, gridCoordinates[1] - 5], [50, 10]])
			if componentOrientation == 1:
				components.append([[gridCoordinates[0] - 5, gridCoordinates[1] - 25], [10, 50]])
	render()
	clock.tick(60)

kill()