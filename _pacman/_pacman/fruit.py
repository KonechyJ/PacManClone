import pygame
from entity import MazeRunner
from constants import *

#this class is for handling the different functionality of the fruit pick up
class Fruit(MazeRunner):
    def __init__(self, nodes, spritesheet, ftype="cherry"):
        MazeRunner.__init__(self, nodes, spritesheet)
        self.name = "fruit"
        self.color = (0, 200, 0)
        self.setStartPosition()
        self.lifespan = 5
        self.timer = 0
        self.destroy = False
        self.setFruit(ftype)

    # this method runs every second to check for the life span
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True

    # this start position method places the fruit between two starting nodes
    def setStartPosition(self):
        self.node = self.findStartNode()
        self.target = self.node.neighbors[LEFT]
        self.setPosition()
        self.position.x -= (self.node.position.x - self.target.position.x) / 2

    # simply returns the fruit start node
    def findStartNode(self):
        for node in self.nodes.nodeList:
            if node.fruitStart:
                return node
        return None

    # function defines fruit varieties
    def setFruit(self, ftype):
        if ftype == "cherry":
            self.image = self.spritesheet.getImage(8, 2, 32, 32)
            self.points = 100
        elif ftype == "banana":
            self.image = self.spritesheet.getImage(9, 2, 32, 32)
            self.points = 200
        elif ftype == "apple":
            self.image = self.spritesheet.getImage(10, 2, 32, 32)
            self.points = 400
        elif ftype == "strawberry":
            self.image = self.spritesheet.getImage(8, 3, 32, 32)
            self.points = 600
        elif ftype == "orange":
            self.image = self.spritesheet.getImage(9, 3, 32, 32)
            self.points = 1000
        elif ftype == "watermelon":
            self.image = self.spritesheet.getImage(10, 3, 32, 32)
            self.points = 1200
