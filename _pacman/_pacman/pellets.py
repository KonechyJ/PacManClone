import pygame
from vector import Vector2
from constants import *

#Class that contains all the information on the pellet objects
class Pellet(object):
    def __init__(self, x, y):
        self.name = "pellet"
        self.position = Vector2(x, y)
        self.color = WHITE
        self.radius = max(int(TILEWIDTH / 8), 1)
        self.points = 10
        self.visible = True

    # function to draw the pellets
    def render(self, screen):
        if self.visible:
            p = self.position.asInt()
            p = (int(p[0] + TILEWIDTH / 2), int(p[1] + TILEWIDTH / 2))
            pygame.draw.circle(screen, self.color, p, self.radius)

#This class defines the variables and functions for the "Power up"  pellets
class PowerPellet(Pellet):
    def __init__(self, x, y):
        Pellet.__init__(self, x, y)
        self.name = "powerpellet"
        self.radius = 8
        self.points = 50
        self.flashTime = 0.2
        self.timer = 0

    # This update functions runs every second and currently handles the flashing for the pellets
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flashTime:
            self.visible = not self.visible
            self.timer = 0

#This class will handle all the pellets in a group
class PelletGroup(object):
    def __init__(self, mazefile):
        self.pelletList = []
        self.powerpellets = []
        self.pelletSymbols = ["p", "n", "Y"]
        self.powerpelletSymbols = ["P", "N"]
        self.createPelletList(mazefile)

    # so for the number of powerpellts in the group, its going to call update to make them flash
    def update(self, dt):
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)

    # this function creates the pellts based on the textfile that has the Pp's listed
    def createPelletList(self, mazefile):
        grid = self.readMazeFile(mazefile)
        rows = len(grid)
        cols = len(grid[0])
        for row in range(rows):
            for col in range(cols):
                if (grid[row][col] in self.pelletSymbols):
                    self.pelletList.append(Pellet(col * TILEWIDTH, row * TILEHEIGHT))
                if (grid[row][col] in self.powerpelletSymbols):
                    pp = PowerPellet(col * TILEWIDTH, row * TILEHEIGHT)
                    self.pelletList.append(pp)
                    self.powerpellets.append(pp)

    # This functions open the pellets file and reads it line for line
    def readMazeFile(self, textfile):
        f = open(textfile, "r")
        lines = [line.rstrip('\n') for line in f]
        return [line.split(' ') for line in lines]

    # Returns bool if the pellet list is empty
    def isEmpty(self):
        if len(self.pelletList) == 0:
            return True
        return False

    # Draws the normal pellets on the screen
    def render(self, screen):
        for pellet in self.pelletList:
            pellet.render(screen)