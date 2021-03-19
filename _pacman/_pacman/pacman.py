import pygame
from pygame.locals import*
from vector import Vector2
from constants import *


#Pacman class
class Pacman(object):
    def __init__(self):
        #variables to set his name, color, speed, size, and location
        self.name = "Pacman"
        self.position = Vector2(200, 400)
        self.direction = STOP
        self.speed = 100
        self.radius = 10
        self.color = YELLOW

    #This update function we calculate Pacman's postion
    def update(self, dt):
        self.position += self.direction*self.speed*dt
        direction = self.getValidKey()
        if direction:
            self.moveByKey(direction)
        else:
            self.direction = STOP

    #this Function checks to see if any of the keys are being pressed
    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return None

    #function to apply direction to movement
    def moveByKey(self, direction):
        self.direction = direction

     #Draws pacman to the screen
    def render(self, screen):
        p = self.position.asInt()
        pygame.draw.circle(screen, self.color, p, self.radius)