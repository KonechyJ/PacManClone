import pygame
from pygame.locals import*
from vector import Vector2
from constants import *
from entity import Entity


#Pacman class
class Pacman(Entity):
    def __init__(self, nodes):
        #variables to set his name, color
        Entity.__init__(self, nodes)
        self.name = "pacman"
        self.color = YELLOW

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
                self.portal()
                if self.node.neighbors[direction] is not None:
                    if self.node.homeEntrance:
                        if self.node.neighbors[self.direction] is not None:
                            self.target = self.node.neighbors[self.direction]
                        else:
                            self.setPosition()
                            self.direction = STOP
                    else:
                        self.target = self.node.neighbors[direction]
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

    #This method lets us know if we have collided with a ghost
    #it does this by checking the distance is less than the radius of the ghost
    def eatGhost(self, ghosts):
        for ghost in ghosts:
            d = self.position - ghost.position
            dSquared = d.magnitudeSquared()
            rSquared = (self.collideRadius + ghost.collideRadius) **2
            if dSquared <= rSquared:
                return ghost
        return None


    #THis method will handle the funtionality for eating pellets
    def eatPellets(self, pelletList):
        #runs a for loop that checks each pellet unitl it finds on that pacman is colliding with
        #If he is not colliding with the pellet, then it returns none
        for pellet in pelletList:
            d = self.position - pellet.position
            dSquared = d.magnitudeSquared()
            rSquared = (pellet.radius+self.collideRadius)**2
            if dSquared <= rSquared:
                return pellet
        return None

    