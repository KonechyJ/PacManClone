import pygame
from constants import *

#This class will handle taking and implementing the sprites from the .png
class Spritesheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("spritesheet.png").convert()
        self.sheet.set_colorkey(TRANSPARENT)

    #Gets the specific images from the sprite sheet
    def getImage(self, x, y, width, height):
        x *= width
        y *= height
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())