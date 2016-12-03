from tkinter import *
import tkinter.messagebox

'''
funclist=[[ Open , Save , Saveas , Print ,  Close ]
,[ Redo , Undo , Copy , Cut , Paste , Delete , Deselect , Text , Netname ] 
,[ Zoomin , Zoomout , Zoomfit , Results ]
,[ DCOppoint , ACOppoint , DCSweep , ACsweep , DCTransferfunction , ACTransferfunction ]
,[ Wire , Resistor , Capacitor , Inductor , Ground , Voltagesouce , Currentsouce , Opamp ]
,[ Preferences ]
,[ About]]
'''

root = Tk()
itemlist=[]
# minimum window size
root.minsize(width=500, height=500)
#Canvas
c = Canvas(root,height = 400,width = 500)
saveicon = PhotoImage(file="Resources/Icons/save.png")
newicon = PhotoImage(file="Resources/Icons/new.png")
resicon = PhotoImage(file="Resources/Icons/Res(2).png")
ressym = PhotoImage(file = "Resources/Icons/Res.png")
#command functions
def Close():
    print("Close")
    root.destroy()
def About():
    print("help yourself")
def donothing():
    rect1 = c.create_rectangle(0,0,50,50, fill = "blue")
    itemlist.append(rect1)
    print("nothing")
def resistor():
    rect2 = c.create_rectangle(0,0,500,400, fill = "blue")
    
def motion(event):
    global status
    x, y = event.x, event.y
    #print('{}, {}'.format(x, y))
    #status = ('{}, {}'.format(x, y))
    
#Toolbar
toolbar = Frame(root,bd =2,relief = RAISED)
new = Button(toolbar,command = donothing,compound=CENTER,image=newicon)
save = Button(toolbar,command = donothing,compound=CENTER,image=saveicon)
resistor = Button(toolbar,command = donothing,compound=CENTER,image=resicon)
new.pack(side = LEFT,padx = 2,pady =2)
save.pack(side = LEFT,padx = 2,pady =2)
resistor.pack(side = LEFT,padx = 2,pady =2)
toolbar.pack(side=TOP,fill = X)
c.pack(fill = X)
#Status bar
statusbar = Label (root , text =("status"),bd = 1, relief = SUNKEN,anchor = W)
statusbar.pack(side = BOTTOM,fill = X)
#command functions list
funclist=[[ donothing , donothing , donothing , donothing , Close ]
,[ donothing , donothing , donothing , donothing , donothing , donothing , donothing , donothing , donothing ] 
,[ donothing , donothing , donothing , donothing ]
,[ donothing , donothing , donothing , donothing , donothing , donothing ]
,[ donothing , resistor , donothing , donothing , donothing , donothing , donothing , donothing ]
,[ donothing ]
,[ About]]

#create menu bar
menu = Menu(root)
root.config(menu=menu)
l = []
menu_commands = [["Open","Save","Save as","Print","Close"]
,["Redo","Undo","Copy","Cut","Paste","Delete","Deselect","Text","Net name"] 
,["Zoom in","Zoom out","Zoom fit","Results"]
,["DC Op point","AC Op point","DC Sweep","AC sweep","DC Transfer function","AC Transfer function"]
,["Wire","Resistor","Capacitor","Inductor","Ground","Voltage souce","Current souce","Opamp"]
,["Preferences"]
,["About"]]

menulist=["File","Edit","View","Simulate","Components","Tools","Help"]
#create menus
for i in range(len(menulist)):
    submenu = Menu(menu)
    l.append(submenu)
#create menu commands
g =0
for i in l:
    menu.add_cascade(label = menulist[g],menu = i)
    m = 0
    for n in menu_commands[g]:
        i.add_command(label=n,command = funclist[g][m] )
        m+=1
    g+=1
root.bind('<Motion>', motion)
root.mainloop()