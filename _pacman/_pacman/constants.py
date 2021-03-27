# This file is used to store the values that will not change throughout the course of the game
from vector import Vector2

#Directions that pacman and ghostss will use
UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)
STOP = Vector2()


tileWidth = 16
tileHeight = 16
nRows = 36   #rows
nCols = 28   #colums
screenWidth = nCols*tileWidth
screenHeight = nRows*tileHeight
sceenSize = (screenWidth, screenHeight)

#COLORS
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 100, 150)
TEAL = (100, 255, 255)
ORANGE = (230, 190, 40)



