import pygame
import copy


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
	global killApp
	global drawingLine
	global drawingComponenet
	global initialCoordinates
	global componentOrientation
	global gridCoordinates
	global lines
	global components
	global verticalWire
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			killApp = True
		if event.type == pygame.MOUSEMOTION:
			gridCoordinates = snapToGrid(event.pos[0],event.pos[1],25)
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_c:
				if drawingComponenet == False:
					drawingComponenet = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				if componentOrientation ==0:
					componentOrientation = 1
				elif componentOrientation ==1:
					componentOrientation = 0
		if event.type == pygame.MOUSEBUTTONUP:
			if drawingLine == False and drawingComponenet == False :
				initialCoordinates = copy.copy(gridCoordinates)
				drawingLine = True
			elif drawingLine == True:
				if (componentOrientation):
					lines.append([initialCoordinates, [initialCoordinates[0], gridCoordinates[1]]])
				else:
					lines.append([initialCoordinates, [gridCoordinates[0], initialCoordinates[1]]])
				drawingLine = False
			if drawingComponenet == True:
				drawingComponenet = False
				if componentOrientation ==0:
					components.append([[gridCoordinates[0] - 25, gridCoordinates[1] - 5], [50, 10]])
				if componentOrientation ==1:
					components.append([[gridCoordinates[0] - 5, gridCoordinates[1] - 25], [10, 50]])

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
	checkEvents()
	render()
	clock.tick(60)

kill()