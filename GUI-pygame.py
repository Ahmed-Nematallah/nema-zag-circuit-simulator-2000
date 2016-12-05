import pygame
'''
def snapToGrid(x,y,gridspace):
    #x = (x//50)*50
    #y = (y//50)*50
    #x = x +min(abs(x-(x//50)*50),abs(x-((x//50)*50+50)))
    #y = y +min(abs(x-(y//50)*50),abs(y-((y//50)*50+50))
    if abs(x-(x//gridspace)*gridspace) < abs(x-((x//gridspace)*gridspace+gridspace)):
        x = x- abs(x-(x//gridspace)*gridspace)
    if abs(x-(x//gridspace)*gridspace) > abs(x-((x//gridspace)*gridspace+gridspace)):
        x = x+ abs(x-((x//gridspace)*gridspace+gridspace))
    if abs(y-(y//gridspace)*gridspace) < abs(y-((y//gridspace)*gridspace+gridspace)):
        y = y- abs(y-(y//gridspace)*gridspace)
    if abs(y-(y//gridspace)*gridspace) > abs(y-((y//gridspace)*gridspace+gridspace)):
        y = y+ abs(y-((y//gridspace)*gridspace+gridspace))
    return x,y
    '''
def snapToGrid(x,y,gridspace):
    #x = (x//50)*50
    #y = (y//50)*50
    #x = x +min(abs(x-(x//50)*50),abs(x-((x//50)*50+50)))
    #y = y +min(abs(x-(y//50)*50),abs(y-((y//50)*50+50))
    if abs(x-(x//gridspace)*gridspace) < abs(x-((x//gridspace)*gridspace+gridspace)):
        x = x- abs(x-(x//gridspace)*gridspace)
    if abs(x-(x//gridspace)*gridspace) > abs(x-((x//gridspace)*gridspace+gridspace)):
        x = x+ abs(x-((x//gridspace)*gridspace+gridspace))
    if abs(y-(y//gridspace)*gridspace) < abs(y-((y//gridspace)*gridspace+gridspace)):
        y = y- abs(y-(y//gridspace)*gridspace)
    if abs(y-(y//gridspace)*gridspace) > abs(y-((y//gridspace)*gridspace+gridspace)):
        y = y+ abs(y-((y//gridspace)*gridspace+gridspace))
    return x,y
pygame.init ()
gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption("circuit sim")
gameExit =False
drawing = False
drawcursx =0
drawcursy = 0
cursx = 0
cursy = 0
while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.MOUSEMOTION:
            cursx,cursy = snapToGrid(event.pos[0],event.pos[1],30)
            print([cursx,cursy,cursx+10,cursy+10])
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing == False:
                drawing = True
            if drawing == True:
                drawing = False
    gameDisplay.fill((150,150,150))
    pygame.draw.rect(gameDisplay, (0,255,255), [cursx-10,cursy-10,25,25])
    #pygame.draw.rect(gameDisplay, (0,255,255), [320,130,280,170])
    pygame.draw.line(gameDisplay, (0,255,255), [0,0], [cursx,cursy])
    pygame.display.update()
pygame.quit()