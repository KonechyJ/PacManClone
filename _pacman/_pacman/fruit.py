import pygame
from entity import Entity
from constants import *

#this class is for handling the different functionality of the fruit pick up
class Fruit(Entity):
    def __init__(self, nodes, spritesheet):
        Entity.__init__(self, nodes, spritesheet)
        self.name = "fruit"
        self.color = (0, 200, 0)
        self.setStartPosition()
        self.lifespan = 5
        self.timer = 0
        self.destroy = False
        self.points = 100
        self.image = self.spritesheet.getImage(8, 2, 32, 32)

    #this method runs every second to check for the life span
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True

    #this start position method places the fruit between two starting nodes
    def setStartPosition(self):
        self.node = self.findStartNode()
        self.target = self.node.neighbors[LEFT]
        self.setPosition()
        self.position.x -= (self.node.position.x - self.target.position.x) / 2

    #simply returns the fruit start node
    def findStartNode(self):
        for node in self.nodes.nodeList:
            if node.fruitStartNode:
                return node
        return None
