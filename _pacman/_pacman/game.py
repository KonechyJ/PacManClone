#this is the main game file
import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit

#class to control the game
class GameController(object):
    def __init__(self):
        #This lines simple set up the game window for the game
        pygame.init()
        self.screen = pygame.display.set_mode(sceenSize, 0, 32)
        self.background = None
        self.setBackground()
        self.clock = pygame.time.Clock()
        self.pelletsEaten = 0
        self.fruit = None

    #this function fills the background with black
    def setBackground(self):
        self.background = pygame.surface.Surface(sceenSize).convert()
        self.background.fill(BLACK)

    #This functions starts the game
    def startGame(self):
        self.nodes = NodeGroup("maze1.txt")
        self.pellets = PelletGroup("pellets1.txt")
        #creates the pacman game object
        self.pacman = Pacman(self.nodes)
        self.ghosts = GhostGroup(self.nodes)


    #update is called once per frame, so it will act as our game loop
    def update(self):
        #line is setting a 30 second value to Dt(delta time)
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        self.ghosts.update(dt, self.pacman)
        if self.fruit is not None:
            self.fruit.update(dt)
        self.pellets.update(dt)
        self.checkPelletEvents()
        self.checkGhostEvents()
        self.checkFruitEvents()
        self.checkEvents()
        self.render()

    #This functions checks for specific events to trigger something
    def checkEvents(self):
        #runs a loop to check every second if the game has exited and if a  key is pressed.
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    #This method will handle will handle all the pellet events
    #we are sending the whole pellet list to pacman and he returns the pellets he collides with
    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pelletsEaten += 1
            if (self.pelletsEaten == 70 or self.pelletsEaten == 140):
                if self.fruit is None:
                    self.fruit = Fruit(self.nodes)
            self.pellets.pelletList.remove(pellet)
            if pellet.name == "powerpellet":
                self.ghosts.freightMode()

    #checks to see if pacman has hit a ghost, and if the ghost is in fright mode, then returns home at double the speed
    def checkGhostEvents(self):
        self.ghosts.release(self.pelletsEaten)
        ghost = self.pacman.eatGhost(self.ghosts)
        if ghost is not None:
            if ghost.mode.name == "FREIGHT":
                ghost.spawnMode(speed=2)

    #Checks if the fruit has been destroyed after pacman eats it or its time runs out
    def checkFruitEvents(self):
        if self.fruit is not None:
            if self.pacman.eatFruit(self.fruit) or self.fruit.destroy:
                self.fruit = None

    #this function will be used to draw images to the screen
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        pygame.display.update()

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()