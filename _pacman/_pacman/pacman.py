import pygame
from pygame.locals import*
from vector import Vector2
from constants import *


#Pacman class
class Pacman(object):
    def __init__(self, nodes):
        #variables to set his name, color, speed, size, and location
        self.name = "Pacman"
        self.direction = STOP
        self.speed = 100
        self.radius = 10
        self.color = YELLOW
        self.nodes = nodes
        self.node = nodes.nodeList[0]
        self.target = self.node
        self.setPosition()

    #this method copys the nodes position to pacmans position
    def setPosition(self):
        self.position = self.node.position.copy()

    #This update function we calculate Pacman's postion
    def update(self, dt):
        self.position += self.direction*self.speed*dt
        direction = self.getValidKey()
        if direction:
            self.moveByKey(direction)
        else:
            self.moveBySelf()

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
       if self.direction is STOP:
            # first checks to see if the direction is not stop,
            # then checks if the direction matches to a neighbor node
            # Then sets that neighbor to the current node
            if self.node.neighbors[direction] is not None:
                self.target = self.node.neighbors[direction]
                self.direction = direction
       else: #checks to see if the direction has reversed
            if direction == self.direction * -1:
                self.reverseDirection()
            # checks to see if the target has overshot
            if self.overshotTarget():
                self.node = self.target
                # sets the current target node along with the direction
                if self.direction != direction:
                    self.setPosition()
                    self.direction = direction
            # sets the next neighbors as current as long as a neighbor exists
            else:
                if self.node.neighbors[self.direction] is not None:
                    self.target = self.node.neighbors[self.direction]
                else:
                    self.setPosition()
                    self.direction = STOP


     #Draws pacman to the screen
    def render(self, screen):
        p = self.position.asInt()
        pygame.draw.circle(screen, self.color, p, self.radius)

    #this function is designed to stop pacman from over shooting nodes
    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False


    #This function allows pacman to change dirtection at any time. Sets pacmans target to a temp for direction change
    def reverseDirection(self):
        if self.direction is UP: self.direction = DOWN
        elif self.direction is DOWN: self.direction = UP
        elif self.direction is LEFT: self.direction = RIGHT
        elif self.direction is RIGHT: self.direction = LEFT
        temp = self.node
        self.node = self.target
        self.target = temp

    #This function first checks to see if pacman has stopped
    #if he is moving, then we check to see if he overshot his node,
    #Then will check when he reaches next node if there is a neighbor is same direction, so as to keep going
    #If he cant, then he finally stops
    def moveBySelf(self):
        if self.direction is not STOP:
            if self.overshotTarget():
                self.node = self.target
                if self.node.neighbors[self.direction] is not None:
                    self.target = self.node.neighbors[self.direction]
                else:
                    self.setPosition()
                    self.direction = STOP