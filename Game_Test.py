import turtle, time, threading, random

turtle.setup(400,500)                # Determine the window size
wn = turtle.Screen()                 # Get a reference to the window
wn.title("Handling keypresses!")     # Change the window title
wn.bgcolor("lightgreen")


#Registering shapes
turtle.register_shape("Char.gif")
turtle.register_shape("grass.gif")
turtle.register_shape("dirt.gif")
turtle.register_shape("shoveling.gif")
turtle.register_shape("yellow.gif")
turtle.register_shape("red.gif")

grlist = ["grass.gif", "grass.gif", "grass.gif", "grass.gif", "yellow.gif", "red.gif"]

class loading(threading.Thread):
    grass = []
    def __init__(self):
        self.drawMap()
        

    def drawMap(self):
        k=0
        i = -5
        while(i < 5):
            j = -5
            while(j<5):
                t = threading.Thread(target=self.addObj, args = (i,j))
                t.daemon = True
                t.start()
                k += 1
                if (k > 10):
                    t.join()
                    k = 0
                j += 1
            i+=1
        

    def addObj(self, i, j):
        ye = turtle.Turtle(shape=random.choice(grlist), visible=False)
        ye._position = (i*10,j*10)
        ye.showturtle()
        if (ye.shape() == "grass.gif"):
            ye.loot = {'dirt':2}
        elif (ye.shape() == "yellow.gif"):
            ye.loot = {'dirt':2, 'yellow_flower':1}
        else:
            ye.loot = {'dirt':2, 'red_flower':1}
        ye.passable = True
        self.grass.append(ye)

    def getFromCoord(x, y):
        for grass in loading.grass:
            if(grass.pos() == (x, y)):
                return grass
        return -1

    def dig(grass):
        for grasss in loading.grass:
            if (grasss == grass):
                loading.getLoot(grasss)
                grasss.shape("dirt.gif")

    def getLoot(grass):
        loot = grass.loot
        inv = char._inventory
        for item in loot:
            inv[item] += loot[item]
            loot[item] = 0


class char(threading.Thread):
    tess = turtle.Turtle()
    name = ""

    _inventory = {'dirt':0, 'yellow_flower':0, 'red_flower':0}

    
        
    def __init__(self):
        tess = self.tess
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
        
        wn.onkey(self.dig, "e")
        wn.onclick(self.go, 1, True)
        wn.listen()

    def dig(self):
        self.tess.shape("shoveling.gif")
        pos = self.tess.pos()
        obj = loading.getFromCoord(pos[0], pos[1])
        loading.dig(obj)
        char = "Char.gif"
        t = threading.Timer(0.2, self.toChar)
        t.start()

    def toChar(self):
        self.tess.shape("Char.gif")
        

    def go(self, x, y):
        tess = self.tess
        x = round(x, -1)
        while (tess.pos()[0] != x):
            k = self.moveX(x - tess.pos()[0])
            if (k == False):
                break
        y = round(y, -1)
        while (tess.pos()[1] != y):
            t = self.moveY(y - tess.pos()[1])
            if (t == False):
                break

    def moveX(self, d):
        tess = self.tess
        if (d >= 0):
            d = 1
        else:
            d = -1
        grass = loading.getFromCoord((tess.pos()[0] + (10 * d)), tess.pos()[1])
        if (grass != -1):
            if (grass.passable == True):
                tess.setx(tess.pos()[0] + (10 * d))
                return True
            else:
                return False
        else:
            return False
            
    def moveY(self, d):
        tess = self.tess
        if (d >= 0):
            d = 1
        else:
            d = -1
        grass = loading.getFromCoord((tess.pos()[0]), tess.pos()[1] + (10 * d))
        if (grass != -1):
            if (grass.passable == True):
                tess.sety(tess.pos()[1] + (10 * d))
                return True
            else:
                return False
        else:
            return False

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
