import turtle, time, threading, random

turtle.setup(400,500)                # Determine the window size
wn = turtle.Screen()                 # Get a reference to the window
wn.title("Flower digger")     # Change the window title
wn.bgcolor("lightgreen")


#Registering shapes
turtle.register_shape("Char.gif")
turtle.register_shape("item_board.gif")
turtle.register_shape("grass.gif")
turtle.register_shape("dirt.gif")
turtle.register_shape("shoveling.gif")
turtle.register_shape("yellow.gif")
turtle.register_shape("red.gif")
turtle.register_shape("tree.gif")
turtle.register_shape("wood.gif")

grlist = ["grass.gif", "grass.gif", "grass.gif", "grass.gif", "yellow.gif", "red.gif", "tree.gif"]

class loading(threading.Thread):
    grass = []
    def __init__(self):
        self.drawMap()
        

    def drawMap(self):
        k=0
        i = 10
        while(i > -10):
            j = 10
            while(j>-10):
                t = threading.Thread(target=self.addObj, args = (i,j))
                t.daemon = True
                t.start()
                k += 1
                if (k > 40):
                    t.join()
                    k = 0
                j -= 1
            i-=1
        

    def addObj(self, i, j):
        shape = random.choice(grlist)
        ye = turtle.Turtle(shape=shape, visible=False)
        ye._position = (i*10,j*10)
        ye.showturtle()
        loading.addLoot(ye, shape) 
        if(ye.shape() == "tree.gif"):
            ye.passable = False
        else:
            ye.passable = True
        self.grass.append(ye)

    def getFromCoord(x, y):
        for grass in loading.grass:
            if(grass.pos() == (x, y)):
                return grass
        return -1

    def addLoot(grass, shape):
        if (shape == "grass.gif"):
            grass.loot = {'dirt':random.randint(1, 2)}
        elif (shape == "yellow.gif"):
            grass.loot = {'dirt':random.randint(1, 2), 'yellow_flower':3}
        elif (shape == "red.gif"):
            grass.loot = {'dirt':random.randint(1, 2), 'red_flower':3}
        else:
            grass.loot = {'wood':random.randint(2, 5)}
    
    def dig(grass):
        loading.getLoot(grass)
        grass.shape("dirt.gif")
        x = grass.pos()[0]
        y = grass.pos()[1]
        t = threading.Timer(120, loading.backToGrass, args = (x, y))
        t.start()

    def cut(tree):
        loading.getLoot(tree)
        shape = tree.shape("grass.gif")
        loading.addLoot(tree, shape)
        tree.passable = True

    def backToGrass(x, y):
        grass = loading.getFromCoord(x, y)
        shape = random.choice(grlist)
        grass.shape(shape)
        loading.addLoot(grass, shape)
        

    def getLoot(grass):
        loot = grass.loot
        inv = char._inventory
        for item in loot:
            inv[item] += loot[item]
            loot[item] = 0


class char(threading.Thread):
    tess = turtle.Turtle()
    name = ""

    _inventory = {'dirt':0, 'yellow_flower':0, 'red_flower':0, 'wood':0}

    
        
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
        wn.onclick(self.go, btn=1, add=True)
        wn.onclick(self.cut, btn=3)
        wn.listen()

    def dig(self):
        self.tess.shape("shoveling.gif")
        pos = self.tess.pos()
        obj = loading.getFromCoord(pos[0], pos[1])
        loading.dig(obj)
        t = threading.Timer(0.2, self.toChar)
        t.start()
        gui.update()

    def toChar(self):
        try:
            self.tess.shape("Char.gif")
        except:
            pass

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

    def cut(self, x, y):
        x = round(x, -1)
        y = round(y, -1)
        tree = loading.getFromCoord(x, y)
        if (tree != -1):
            if (tree.shape() == "tree.gif"):
                if(tree.distance(self.tess.pos()) <= 20):
                    self.tess.shape("shoveling.gif")
                    loading.cut(tree)
                    t = threading.Timer(0.2, self.toChar)
                    t.start()
                    gui.update()

class gui(threading.Thread):
    def __init__(self):
        self.drawGui()
        self.update()

    def drawGui(self):
        self.char = self.createTurtle("Char.gif", -40, -200)
        self.item_board = self.createTurtle("item_board.gif", 0, -200)
        self.dirt = self.createTurtle("dirt.gif", -20, -200)
        self.flower = self.createTurtle("yellow.gif", 0, -200)
        self.redflower = self.createTurtle("red.gif", 20, -200)
        self.tree = self.createTurtle("wood.gif", 40, -200)

    def createTurtle(self, item, x, y):
        this = turtle.Turtle(shape=item, visible=False)
        this._position = (x, y)
        this.showturtle()
        return this

    def update(self):
        self.dirt.clear()
        self.dirt.count = char._inventory["dirt"]
        self.dirt.write(self.dirt.count, move=False, align="right", font=("Arial", 6, "bold"))
        self.flower.clear()
        self.flower.count = char._inventory["yellow_flower"]
        self.flower.write(self.flower.count, move=False, align="right", font=("Arial", 6, "bold"))
        self.redflower.clear()
        self.redflower.count = char._inventory["red_flower"]
        self.redflower.write(self.redflower.count, move=False, align="right", font=("Arial", 6, "bold"))
        self.tree.clear()
        self.tree.count = char._inventory["wood"]
        self.tree.write(self.tree.count, move=False, align="right", font=("Arial", 6, "bold"))
loadingScreen = loading()
char = char()
gui = gui()

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
