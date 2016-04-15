from tkinter import *

def makeLevel(string):
    p = []
    with open(string, 'r') as f:
        for line in f:
            line = line.strip()
            foo = []
            for i in line:
               foo.append(i)
            p.append(foo)
    return p

def findPlayer():
    for i in range(w):
        for j in range(h):
            if(p[j][i] == 'O'):
                return(i,j)

def carre(x, y, couleur):
    canvas.create_rectangle(x, y, x+wid, y+hei, fill=couleur)

def rond(x, y, couleur):
    canvas.create_oval(x, y, x+wid, y+hei, fill=couleur)

def draw():
    canvas.delete("all")
    for i in range(wid, width, wid):
        canvas.create_line(i, 0, i, height)

    for i in range(hei, height, hei):
        canvas.create_line(0, i, width, i)

    for i in range(w):
        for j in range(h):
            if(p[j][i] == '#'):
                carre(i*wid, j*hei, "#252525")
            if(p[j][i] == 'O'):
                rond(i*wid, j*hei, "red")
            if(p[j][i] == '*'):
                carre(i*wid, j*hei, "blue")
            if(p[j][i] == 'X'):
                carre(i*wid, j*hei, "yellow")
            if(p[j][i] == 'A'):
                carre(i*wid, j*hei, "yellow")
                rond(i*wid, j*hei, "red")
            if(p[j][i] == 'R'):
                carre(i*wid, j*hei, "pink")
            
            
def fermer(event):
    root.destroy()

def deviation(x, y):
    #global ply_y, ply_x
    if(p[y][x] == 'O'):
        p[y][x] = ' '
    if(p[y][x] == 'A'):
        p[y][x] = 'X'

def premik_na(x, y):
    if(p[y][x] == 'X'):
        p[y][x] = 'A'
    if(p[y][x] == ' '):
        p[y][x] = 'O'

def deviation_objet(x, y):
    if(p[y][x] == '*'):
        p[y][x] = ' '
    if(p[y][x] == 'R'):
        p[y][x] = 'X'

def personnage(x, y):
#    print("Hej")
    global ply_y, ply_x
    if(p[ply_y + y][ply_x + x] in dovoljeni):
        deviation(ply_x, ply_y)
        ply_y += y
        ply_x += x
        premik_na(ply_x, ply_y)

    elif(p[ply_y + y][ply_x + x] in premikajoci):
        if(p[ply_y + 2*y][ply_x + 2*x] in dovoljeni):
            deviation_objet(ply_x + x, ply_y + y)
            deviation(ply_x, ply_y)
            ply_y += y
            ply_x += x
            premik_na(ply_x, ply_y)
            

def victoire():
    for i in p:
        for j in i:
            if(j == 'X'):
                return False
            elif(j == 'A'):
                return False
    return True

def mouvement(n):
    global ply_x, ply_y

    if(n == 'Up'):
        personnage(0, -1)

    elif(n == 'Down'):
        personnage(0, 1)

    elif(n == 'Left'):
        personnage(-1, 0)

    elif(n == 'Right'):
        personnage(1, 0)

    draw()
    if(victoire()):
        showinfo("Vous avez gagné !", "Félicitations, vous avez gagné !")
        root.destroy()
    

def restart():
    global p
    global ply_x, ply_y
    p = makeLevel(level)
    ply_x, ply_y = findPlayer()
    draw()
    
    
def keyHandler(event):
    foo = event.keysym
    mouvement(foo)
    if(event.char == 'r'):
        restart()


def askLevel():
    top = Tk()
    top.withdraw()
    level = askopenfilename(initialdir = "level", filetypes = [('Level files', '.lvl'), ('All files', '.*')], title = "Veuillez choisir un niveau...")
    top.destroy()

    try:
        return(makeLevel(level))
    except IOError:
        top = Tk()
        top.withdraw()
        if(askretrycancel("Erreur !", "Il semblerait que le fichier que vous tentez d'ouvrir ne soit pas un niveau !")):           
            try:
                return(askLevel())
            finally:
                top.destroy()
        else:
            top.destroy()
            return(False)
    
p = askLevel()
if(not p):
    pass
else:
    w = len(p[0])
    h = len(p)

    dovoljeni = [' ', 'X']
    premikajoci = ['*', 'R']


    max_width = 1000
    max_height = 1000


    wid = hei = 50

    if(wid*w > max_width or hei*h > max_height):
        wid = hei = min(max_width//w, max_height//h)
    width = wid * w
    height = hei * h



    ply_x, ply_y = findPlayer()





    root = Tk()
    root.title("Sokoban Sans Images")
    root.focus_force()

    canvas = Canvas(root, width=width, height=height)
    canvas.pack()
    draw()

    root.bind_all("<Escape>", fermer)
    root.bind_all("<Key>", keyHandler)

    root.mainloop()
