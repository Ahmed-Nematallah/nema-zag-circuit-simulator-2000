# !/usr/bin/python3
from tkinter import *

root = Tk()
w = Canvas(root, width = 1000, height = 400)
frame = Frame(root,width = 30,height = 30)
w.grid(row =0,column = 0)
def ddrag(event):
    print("catch")
    #print(w.find_closest(event.x, event.y)[0])
    #if (w.find_closest(event.x, event.y)[0] != cd) :
    global cd
    cd = w.find_closest(event.x, event.y)[0]
    #print("cd is ",cd)
    #print(current_drag[0])
def connecting():
    global con 
    con = 1
def ddrop(event):
    print("relase")
    global cd
    cd =0
def pos_comp(event):
    x, y = event.x, event.y
    #print('{}, {}'.format(x, y))
    print("cd is ",cd)
    if cd != 0:
        w.coords(items[cd],event.x, event.y,event.x+(w.coords(items[cd])[2]-w.coords(items[cd])[0]), event.y+(w.coords(items[cd])[2]-w.coords(items[cd])[0]))
        #print(w.coords(rect1))
    #if con != 0:
    #  wire = w.create_line(event.x,event.y,w.coords(slave11)[0],w.coords(slave11)[2])
        
    #print((w.coords(items[cd])[0]-w.coords(items[cd])[2]))
    w.coords(slave11,w.coords(rect1)[0]-50,w.coords(rect1)[1],w.coords(rect1)[2]-50,w.coords(rect1)[3])
    w.coords(slave12,w.coords(rect1)[0]+50,w.coords(rect1)[1],w.coords(rect1)[2]+50,w.coords(rect1)[3])
    #slave12=w.create_rectangle(w.coords(rect1)-5, fill = "orange")
    #w.coords(res,event.x+0, event.y+0)
    

#line = canvas.create_line(0,0,100,50,fill = "red", dash=(6, 4))
#photo = PhotoImage(file = "res.png")
#res = w.create_image(700,700,image = photo)
#label = Label(frame, image = photo)
#label.pack(side = LEFT)
#canvas.delete(line)
#objs = list()
#for i in range(300):
 #   objs.append(w.create_rectangle(0,0,i*5,200, fill = "red",width = 5))
#lines = [w.create_line(0,0,i,200, fill = "red",width = 5) for i in range(500)]
rect1=w.create_rectangle(100,100,120,120, fill = "red",tag = "8")
rect2=w.create_rectangle(50,50,70,70, fill = "blue",tag = "2")
slave11=w.create_rectangle(w.coords(rect1)[0]+50,w.coords(rect1)[1],w.coords(rect1)[2]+50,w.coords(rect1)[3], fill = "orange",tag = "5")
slave12=w.create_rectangle(w.coords(rect1)[0]-50,w.coords(rect1)[1],w.coords(rect1)[2]-50,w.coords(rect1)[3], fill = "orange",tag = "7")
#slave12=w.create_rectangle(0,0,20,20, fill = "blue",tag = "2")
wire = w.create_line(0,0,w.coords(rect1)[0],w.coords(rect1)[1])
w.tag_bind(rect1,'<Button-1>', ddrag)
w.tag_bind(rect2,'<Button-1>', ddrag )
w.tag_bind(rect1,"<ButtonRelease-1>", ddrop)
w.tag_bind(rect2,"<ButtonRelease-1>", ddrop)
w.tag_bind(slave11,'<Button-1>',connecting)
w.tag_bind(slave12,'<Button-1>',connecting)
#w.coords(items[cd],event.x-20, event.y-20,event.x+20, event.y+20)
items = {1:rect1,2:rect2,3:slave11,4:slave12}

root.bind("<Motion>",pos_comp)
#current_drag = items[2]
#rect1.bind("<Button-1>",ddrag)
#rect1.bind("<Button-1>",ddrag)
#rect1.bind("<Button-1>",ddrag)
#line2=w.create_line(40,40,40,40, fill = "blue")
#line3=w.create_line(150,150,150,450,fill = "red")
root.mainloop()