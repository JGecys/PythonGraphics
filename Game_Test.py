import turtle, time, threading

turtle.setup(400,500)                # Determine the window size
wn = turtle.Screen()                 # Get a reference to the window
wn.title("Handling keypresses!")     # Change the window title
wn.bgcolor("lightgreen")

#Registering shapes
turtle.register_shape("Char.gif")
turtle.register_shape("grass.gif")
turtle.register_shape("dirt.gif")

class loading(threading.Thread):
    grass = []
    def __init__(self):
        self.drawMap()
        

    def drawMap(self):
        i = -10
        while(i < 10):
            j = -10
            while(j<10):
                t = threading.Thread(target=self.addObj, args = (i,j))
                t.daemon = True
                t.start()
                if (j == 9) and (i % 2 == 0):
                    t.join()
                j += 1
            i+=1

    def addObj(self, i, j):
        ye = turtle.Turtle(shape="grass.gif", visible=False)
        ye._position = (i*10,j*10)
        ye.showturtle()
        ye.loot = {'dirt':2}
        self.grass.append(ye)

    def getFromCoord(x, y):
        for grass in loading.grass:
            if(grass.pos() == (x, y)):
                return grass
        return -1

    def dig(grass):
        for grasss in loading.grass:
            if (grasss == grass):
                grasss.shape("dirt.gif")


class arrow(threading.Thread):
    def __init__(self, tess):
        self.add(tess)
        
    def add(self, tess):
        i = True
        while (i):
            arrow = turtle.Turtle()
            arrow.penup()
            arrow.hideturtle()
            arrow.setpos(tess.pos())
            arrow.showturtle()
            i = not i
        arrow.speed(2)
        arrow.forward(300)
        arrow.hideturtle()

class char(threading.Thread):
    tess = turtle.Turtle()
    name = ""

    
        
    def __init__(self):
        tess = self.tess             # Create our favorite turtle
        tess.degrees()
        tess.speed(1)
        tess.shape("Char.gif")
        tess.shapesize(10, 10)
        tess.penup()
        while(self.name == ""):
            self.name = turtle.textinput("Name", "Type in your name")
        tess.write("Welcome, "+self.name, True, align="right", font=("Arial", 13, "bold"))
        tess.goto(0,0)
        time.sleep(1)
        tess.clear()
        
        wn.onkey(self.shootArrow, "z")
        wn.onkey(self.dig, "e")
        wn.onclick(self.go, 1, True)
        wn.listen()

    def dig(self):
        pos = self.tess.pos()
        obj = loading.getFromCoord(pos[0], pos[1])
        loading.dig(obj)
        

    def go(self, x, y):
        tess = self.tess
        x = round(x, -1)
        tess.setx(x)
        y = round(y, -1)
        tess.sety(y)

    def shootArrow(self):
        arrow(self.tess)

loadingScreen = loading()
char = char()

# The next four functions are our "event handlers".

    
def quit():
    wn.bye()                        # Close down the turtle window



# These lines "wire up" keypresses to the handlers we've defined.

wn.onkey(quit, "q")


# Now we need to tell the window to start listening for events,
# If any of the keys that we're monitoring is pressed, its
# handler will be called.
wn.listen()
wn.mainloop()
