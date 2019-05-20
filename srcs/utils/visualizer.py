from tkinter import *  
from PIL import ImageTk,Image, ImageDraw
import time
import numpy as np
import os

class Visualizer(object):
    def __init__(self, states, puzzleSize):
        self.states = states
        self.puzzleSize = puzzleSize
        if puzzleSize > 3:
            self.img = Image.open('images/cat.jpg')
        else:
            self.img = Image.open('images/AKAMARUUUU.jpg')
        self.root = Tk()
        self.root.title("N-Puzzle")
        # Display canvas as front page
        os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
        self.images = self.__initImages__()  
        self.canvas = Canvas(self.root, width = self.img.width + 20, height = self.img.height + 20)
        self.canvas.pack()
        self.__initialStateDisplay__()
        self.__process__()
        self.root.mainloop()
        

    def __initImages__(self):
        images = {}

        if self.puzzleSize == 3:
            images[0] = ImageTk.PhotoImage(Image.open("images/AKAMARUUUU_02_02.png"))
            images[1] = ImageTk.PhotoImage(Image.open("images/AKAMARUUUU_01_01.png"))
            images[2] = ImageTk.PhotoImage(Image.open("images/AKAMARUUUU_01_02.png"))
            images[3] = ImageTk.PhotoImage(Image.open("images/AKAMARUUUU_01_03.png"))
            images[4] = ImageTk.PhotoImage(Image.open("images/AKAMARUUUU_02_03.png"))
            images[5] = ImageTk.PhotoImage(Image.open("images/AKAMARUUUU_03_03.png"))
            images[6] = ImageTk.PhotoImage(Image.open("images/AKAMARUUUU_03_02.png"))
            images[7] = ImageTk.PhotoImage(Image.open("images/AKAMARUUUU_03_01.png"))
            images[8] = ImageTk.PhotoImage(Image.open("images/AKAMARUUUU_02_01.png"))
        elif self.puzzleSize == 4:
            images[0] = ImageTk.PhotoImage(Image.open("images/cat_03_02.png"))
            images[1] = ImageTk.PhotoImage(Image.open("images/cat_01_01.png"))
            images[2] = ImageTk.PhotoImage(Image.open("images/cat_01_02.png"))
            images[3] = ImageTk.PhotoImage(Image.open("images/cat_01_03.png"))
            images[4] = ImageTk.PhotoImage(Image.open("images/cat_01_04.png"))
            images[5] = ImageTk.PhotoImage(Image.open("images/cat_02_04.png"))
            images[6] = ImageTk.PhotoImage(Image.open("images/cat_03_04.png"))
            images[7] = ImageTk.PhotoImage(Image.open("images/cat_04_04.png"))
            images[8] = ImageTk.PhotoImage(Image.open("images/cat_04_03.png"))
            images[9] = ImageTk.PhotoImage(Image.open("images/cat_04_02.png"))
            images[10] = ImageTk.PhotoImage(Image.open("images/cat_04_01.png"))
            images[11] = ImageTk.PhotoImage(Image.open("images/cat_03_01.png"))
            images[12] = ImageTk.PhotoImage(Image.open("images/cat_02_01.png"))
            images[13] = ImageTk.PhotoImage(Image.open("images/cat_02_02.png"))
            images[14] = ImageTk.PhotoImage(Image.open("images/cat_02_03.png"))
            images[15] = ImageTk.PhotoImage(Image.open("images/cat_03_03.png"))
        return images

    def __initialStateDisplay__(self):
        currentState = self.states[len(self.states) - 1]
        self.initialState = currentState
        self.canvasImages = np.empty([self.puzzleSize, self.puzzleSize], np.int32)
        y = 0
        x = 0
        imageX = 10
        imageY = 10
        while y < self.puzzleSize:
            x = 0
            imageX = 10
            while x < self.puzzleSize:
                currentImg = self.images[currentState[y][x]]
                self.canvasImages[y][x] = self.canvas.create_image(imageX, imageY, anchor=NW, image=currentImg)
                if (currentState[y][x] == 0):
                    self.canvas.itemconfigure(self.canvasImages[y][x], state='hidden')
                x += 1
                imageX += currentImg.width()
            y += 1
            imageY += currentImg.height()

    def __displayNone__(self, currentState):
        emptyTileCoordinates = np.where(currentState == 0)
        emptyImgId = self.canvasImages[emptyTileCoordinates[0][0]][emptyTileCoordinates[1][0]]
        self.canvas.itemconfigure(emptyImgId, state='normal')

    def __process__(self):
        if self.puzzleSize > 3:
            time = 200
        else:
            time = 500
        i = len(self.states) - 2
        currentState = self.initialState
        while i >= 0:
            prevState = currentState
            currentState = self.states[i]
            diffState = prevState - currentState
            emptyTileCoordinates = np.where(diffState < 0)
            filledTileCoordinates = np.where(diffState > 0)
            filledImgId = self.canvasImages[filledTileCoordinates[0][0]][filledTileCoordinates[1][0]]
            emptyImgId = self.canvasImages[emptyTileCoordinates[0][0]][emptyTileCoordinates[1][0]]
            self.canvasImages[filledTileCoordinates[0][0]][filledTileCoordinates[1][0]], self.canvasImages[emptyTileCoordinates[0][0]][emptyTileCoordinates[1][0]] = self.canvasImages[emptyTileCoordinates[0][0]][emptyTileCoordinates[1][0]], self.canvasImages[filledTileCoordinates[0][0]][filledTileCoordinates[1][0]]
            filledCoords = self.canvas.coords(filledImgId)
            emptyCoords = self.canvas.coords(emptyImgId)
            self.__move__(emptyImgId, emptyCoords, filledImgId, filledCoords)
            i -= 1
            self.canvas.after(time)
            self.root.update()
        self.canvas.after(time, self.__displayNone__(currentState))
        
    

    def __move__(self, emptyImgId, emptyCoords, filledImgId, filledCoords):
        filledImageXOffset = filledCoords[0] - emptyCoords[0]
        filledImageYOffset = filledCoords[1] - emptyCoords[1]
        emptyImageXOffset = emptyCoords[0] - filledCoords[0]
        emptyImageYOffset = emptyCoords[1] - filledCoords[1]
        self.canvas.move(emptyImgId, -emptyImageXOffset, -emptyImageYOffset)
        self.canvas.move(filledImgId, -filledImageXOffset, -filledImageYOffset)