from tkinter import *
from PIL import Image, ImageTk
import random

WIDTH = 800
HEIGHT = 800
BODYSIZE = 25
STARTTIME = 200
MINTIME = 100
STEPTIME = 5
LENGTH = 3

countBodyW = WIDTH / BODYSIZE
countBodyH = HEIGHT / BODYSIZE
#x = [0] * int(countBodyW)
#y = [0] * int(countBodyH)

class Snake(Canvas):

    x = False
    y = False
    headImage = False
    head = False
    body = False
    apple = False
    delay = 0
    direction = "Right"
    tempdirection = "Right"
    loss = False

    def __init__(self):
        Canvas.__init__(self, width=WIDTH, height=HEIGHT, background="white")
        self.focus_get()
        self.bind_all("<Key>", self.onKeyPressed)
        self.loadResurces()
        self.startgame()
        self.pack()

    def loadResurces(self):
        self.headImage = Image.open("images/голова 2.jpg")

        self.head = ImageTk.PhotoImage(self.headImage.resize((BODYSIZE, BODYSIZE), Image.ANTIALIAS))
        self.body = ImageTk.PhotoImage(Image.open("images/тело.png").resize((BODYSIZE, BODYSIZE), Image.ANTIALIAS))
        self.apple = ImageTk.PhotoImage(Image.open("images/яблоко.png").resize((BODYSIZE, BODYSIZE), Image.ANTIALIAS))

    def startgame(self):
        self.delay = STARTTIME
        self.direction = "Right"
        self.tempdirection = "Right"
        self.loss = False

        self.x = [0] * int(countBodyW)
        self.y = [0] * int(countBodyH)
        x = [0] * int(countBodyW)
        y = [0] * int(countBodyH)

        self.delete(ALL)
        self.spawnActors()
        self.after(self.delay, self.timer)

    def spawnActors(self):

        self.spawnApple()

        self.x[0] = int(countBodyW / 2) * BODYSIZE
        self.y[0] = int(countBodyH / 2) * BODYSIZE
        for i in range(1, LENGTH):
            self.x[i] = self.x[0] - BODYSIZE * i
            self.y[i] = self.y[0]
        self.create_image(self.x[0], self.y[0], image=self.head, anchor="nw", tag="head")
        for i in range(LENGTH - 1, 0, -1):
            self.create_image(self.x[i], self.y[i], image=self.body, anchor="nw", tag="body")

    def spawnApple(self):
        apple = self.find_withtag("apple")
        if apple:
            self.delete(apple[0])
        rx = random.randint(0, countBodyW - 1)
        ry = random.randint(0, countBodyH - 1)
        self.create_image(rx * BODYSIZE, ry * BODYSIZE, anchor="nw", image=self.apple, tag="apple")

    def checkApple(self):
        apple = self.find_withtag("apple")[0]
        head = self.find_withtag("head")
        body = self.find_withtag("body")[-1]
        x1, y1, x2, y2 = self.bbox(head)
        overlaps = self.find_overlapping(x1, y1, x2, y2)
        for actor in overlaps:
            if actor == apple:
                tempx, tempy = self.coords(body)
                self.spawnApple()
                self.create_image(tempx, tempy, image=self.body, anchor="nw", tag="body")
                if self.delay > MINTIME:
                    self.delay -= STEPTIME

    def checkCollision(self):
        head = self.find_withtag("head")
        body = self.find_withtag("body")
        x1, y1, x2, y2 = self.bbox(head)
        overlaps = self.find_overlapping(x1, y1, x2, y2)
        for b in body:
            for actor in overlaps:
                if actor == b:
                    self.loss = True

        if x1 < 0:
            self.loss = True
        if x2 > WIDTH:
            self.loss = True
        if y1 < 0:
            self.loss = True
        if y2 > HEIGHT:
            self.loss = True


    def onKeyPressed(self, event):
        key = event.keysym
        if key == "Left" and self.tempdirection != "Right":
            self.tempdirection = key
        elif key == "Right" and self.tempdirection != "Left":
            self.tempdirection = key
        elif key == "Up" and self.tempdirection != "Down":
            self.tempdirection = key
        elif key == "Down" and self.tempdirection != "Up":
            self.tempdirection = key
        elif key == "space" and self.loss:
            self.startgame()

    def updateDirection(self):
        self.direction = self.tempdirection
        head = self.find_withtag("head")
        headx, heady = self.coords(head)
        self.delete(head)
        if self.direction == "Left":
            self.head = ImageTk.PhotoImage(self.headImage.transpose(Image.FLIP_LEFT_RIGHT).resize((BODYSIZE, BODYSIZE), Image.ANTIALIAS))
        else:
            rotates = {'Right': 0, 'Up': 90, 'Down': -90}
            self.head = ImageTk.PhotoImage(self.headImage.rotate(rotates[self.direction]).resize((BODYSIZE, BODYSIZE),
                                           Image.ANTIALIAS))
        self.create_image(headx, heady, image=self.head, anchor="nw", tag="head")

    def timer(self):
        self.checkCollision()
        if not self.loss:
            self.checkApple()
            self.updateDirection()
            self.moveSnake()
            self.after(self.delay, self.timer)
        else:
            self.gameOver()

    def moveSnake(self):
        head = self.find_withtag("head")
        body = self.find_withtag("body")
        items = body + head
        for i in range(len(items) - 1):
            currentxy = self.coords(items[i])
            nextxy = self.coords(items[i + 1])
            self.move(items[i], nextxy[0] - currentxy[0], nextxy[1] - currentxy[1])
        if self.direction == "Left":
            self.move(head, -BODYSIZE, 0)
        elif self.direction == "Right":
            self.move(head, BODYSIZE, 0)
        elif self.direction == "Up":
            self.move(head, 0, -BODYSIZE)
        elif self.direction == "Down":
            self.move(head, 0, BODYSIZE)

    def gameOver(self):
        body = self.find_withtag("body")
        self.delete(ALL)
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2 - 60, text="Game over!", fill="black", font="Tahoma 40", tag="text")
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2, text="Длина змейки: " + str(len(body) + 1), fill="black", font="Tahoma 40", tag="text")
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2 + 60, text="Нажмите пробел для новой игры", fill="black", font="Tahoma 40", tag="text")

root = Tk()
root.title("Змейка")
root.board = Snake()
root.resizable(False, False)




ws = root.winfo_screenwidth()
wh = root.winfo_screenheight()

x = int(ws/2 - WIDTH/2)
y = int(wh/2 - HEIGHT/2)

root.geometry("+{0}+{1}".format(x, y))

root.mainloop()