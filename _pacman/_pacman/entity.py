#just a carbon copy of the pacman code that we can use for base ghost and pacman class
import pygame
from vector import Vector2
from constants import *

#class declaration for any object that will inherit from this class
class Entity(object):
    def __init__(self, nodes, spritesheet):
        # all the variables used in either pacman or ghost
        self.name = ""
        self.direction = STOP
        self.speed = 100
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
        self.nodes = nodes
        self.node = nodes.nodeList[0]
        self.target = self.node
        self.setPosition()
        self.visible = True
        self.image = None
        self.spritesheet = spritesheet

    # this method copys the nodes position to pacmans/ghost position
    def setPosition(self):
        self.position = self.node.position.copy()

    def update(self, dt):
        self.position += self.direction*self.speed*dt
        self.moveBySelf()

    # This function first checks to see if pacman/ghost has stopped
    # if he is moving, then we check to see if he overshot his node,
    # Then will check when he reaches next node if there is a neighbor is same direction, so as to keep going
    # If he cant, then he finally stops
    def moveBySelf(self):
        if self.direction is not STOP:
            if self.overshotTarget():
                self.node = self.target
                self.portal()
                if self.node.neighbors[self.direction] is not None:
                    self.target = self.node.neighbors[self.direction]
                else:
                    self.setPosition()
                    self.direction = STOP

    # this function is designed to stop pacman/ghost from over shooting nodes
    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False

    # This function allows pacman/ghost to change dirtection at any time. Sets pacmans/ghost target to a temp for direction change
    def reverseDirection(self):
        if self.direction is UP: self.direction = DOWN
        elif self.direction is DOWN: self.direction = UP
        elif self.direction is LEFT: self.direction = RIGHT
        elif self.direction is RIGHT: self.direction = LEFT
        temp = self.node
        self.node = self.target
        self.target = temp

    # Simple function to tell pacman what to do on a portal on node
    def portal(self):
        if self.node.portalNode:
            self.node = self.node.portalNode
            self.setPosition()

    # Draws pacman/ghost to the screen
    def render(self, screen):
        if self.visible:
            if self.image is not None:
                p = self.position.asTuple()
                p = (p[0] - tileWidth / 2, p[1] - tileWidth / 2)
                screen.blit(self.image, p)
            else:
                p = self.position.asInt()
                pygame.draw.circle(screen, self.color, p, self.radius)

