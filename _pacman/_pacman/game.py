#this is the main game file
import pygame
from pygame.locls import *
from constants import *

#class to control the game
class GameController(object):
    def __int__(self):
        #This lines simple set up the game window for the game
        pygame.init()
        self.screen = pygame.display.set_mode(sceenSize, 0, 32)
        self.background = None
        self.setBackground()

    #this function fills the background with black
    def setBackground(self):
        self.background = pygame.surface.Surface(sceenSize).convert()
        self.background.fill(BLACK)

    #This functions starts the game
    def startGame(self):
        pass
    #update is called once per frame, so it will act as our game loop
    def upadte(self):
        self.checkEvents()
        self.render()

    #This functions checks for specific events to trigger something
    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    #this function will be used to draw images to the screen
    def render(self):
        pygame.display.update()

if __name__ == "__main__":
    game =GameController()
    game.startGame()
    while True:
        game.upadte()