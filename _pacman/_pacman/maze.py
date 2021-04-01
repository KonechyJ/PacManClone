import pygame
from constants import *

#this class will hadnle drawing the various sprites onto the screen from the sprite sheet
#also of note the two files "maze1_sprites.txt and maze1_rotation.txt both handle placing which image from the sprite sheet where
# and how they need to be rotated respectively

#rotation.txt handles as follows:
#0: no rotation
# 1: rotate 90 degrees
# 2: rotate 180 degrees
# 3: rotate 270 degrees

#class handles applying the maze images to the respective numbers and symbols applied in the maze1_sprites text file
class Maze(object):
    def __init__(self, spritesheet):
        self.spritesheet = spritesheet
        self.spriteInfo = None
        self.rotateInfo = None
        self.images = []
        self.flash_images = []
        self.imageRow = 16

    #this method gets the gets the specific images needed to fill in the images of the maze
    def getMazeImages(self, row=0):
        self.images = []
        for i in range(11):
            self.images.append(self.spritesheet.getImage(i, self.imageRow + row, tileWidth, tileHeight))

    #rotates the images as needed according to the rotation.txt
    def rotate(self, image, value):
        return pygame.transform.rotate(image, value * 90)

    #reads the maze file input and turns it into commands
    def readMazeFile(self, textfile):
        f = open(textfile, "r")
        lines = [line.rstrip('\n') for line in f]
        return [line.split(' ') for line in lines]

    #interprets the information on each of the txt files
    def getMaze(self, mazename):
        self.spriteInfo = self.readMazeFile(mazename + "_sprites.txt")
        self.rotateInfo = self.readMazeFile(mazename + "_rotation.txt")

    #this methods actually takes the images, the interpretted information from the textr files, and applies them to the screen
    def constructMaze(self, background, row=0):
        self.getMazeImages(row)
        rows = len(self.spriteInfo)
        cols = len(self.spriteInfo[0])
        for row in range(rows):
            for col in range(cols):
                x = col * tileWidth
                y = row * tileHeight
                val = self.spriteInfo[row][col]
                if val.isdecimal():
                    rotVal = self.rotateInfo[row][col]
                    image = self.rotate(self.images[int(val)], int(rotVal))
                    background.blit(image, (x, y))

                if val == '=':
                    background.blit(self.images[10], (x, y))
