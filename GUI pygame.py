import pygame


def snapToGrid(x,y,gridspace):
    if (x % gridspace < gridspace / 2):
        x = x - (x % gridspace)
    else:
        x = (x + gridspace)  - (x % gridspace)
    if (y % gridspace < gridspace / 2):
        y = y - (y % gridspace)
    else:
        y = (y + gridspace) - (y % gridspace)
    return x,y

pygame.init ()
gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption("circuit sim")
gameExit =False
drawing = False
drawgridX =0
drawgridY = 0
gridX = 0
gridY = 0
lines=[]
verticalWire = False
#main loop
while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.MOUSEMOTION:
            gridX,gridY = snapToGrid(event.pos[0],event.pos[1],30)
            print(gridX,gridY)
        if event.type == pygame.MOUSEBUTTONUP:
            print("mouse down")
            if drawing == False:
                drawgridX = gridX
                drawgridY = gridY
                drawing = True
            elif drawing == True:
                if (verticalWire):
                    lines.append([drawgridX,drawgridY,drawgridX,gridY])
                else:
                    lines.append([drawgridX,drawgridY,gridX,drawgridY])
                drawing = False
    gameDisplay.fill((150,150,150))
    #draw current line
    if drawing:
        if abs(drawgridX - gridX) >= abs(drawgridY - gridY):
            verticalWire = False
            pygame.draw.line(gameDisplay, (0,255,255), [drawgridX,drawgridY], [gridX,drawgridY],3)
        else:
            verticalWire = True
            pygame.draw.line(gameDisplay, (0,255,255), [drawgridX,drawgridY], [drawgridX,gridY],3)
    #render drawn lines
    if len(lines)>0:
        for l in lines :
            pygame.draw.line(gameDisplay, (0,255,255), [l[0],l[1]],[l[2],l[3]],3)
    # render drawn components
    if len(components)>0:
        for c in components:
            pygame.draw.rect(gameDisplay, (0,255,255), [c[0],c[1],c[2],c[3]])
    #pygame.draw.rect(gameDisplay, (0,255,255), [gridX-10,gridY-10,25,25])
    #pygame.draw.rect(gameDisplay, (0,255,255), [320,130,280,170])
    #pygame.draw.line(gameDisplay, (0,255,255), [0,0], [gridX,gridY])
    pygame.display.update()
pygame.quit()