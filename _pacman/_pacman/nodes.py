import pygame
from vector import Vector2
from constants import *

#The node class to handle all the functionality for each node
class Node(object):
    #these below take in row and col and assign them to tile height and length
    def __init__(self, row, column):
        self.row, self.column = row, column
        self.position = Vector2(column*tileWidth, row*tileHeight)
        #this dictionary is to store the next nodes pacman can go to
        self.neighbors = {UP: None, DOWN: None, LEFT: None, RIGHT: None}

    #this render will draw the nodes to the screen
    def render(self, screen):
        #for the number of neighbors and if there are neighbor nodes,
        #then draw them as red dots and connect them with white lines
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.asInt(), 12)

#This class simple creates an object to hold all the nodes
class NodeGroup(object):
    def __init__(self):
        self.nodeList = []

    #defines the nodes and there positions
    def setupTestNodes(self):
        nodeA = Node(5, 5)
        nodeB = Node(5, 10)
        nodeC = Node(10, 5)
        nodeD = Node(10, 10)
        nodeE = Node(10, 13)
        nodeF = Node(20, 5)
        nodeG = Node(20, 13)

        #declares all the neighbors to the nodes and adds all nodes to nodeList
        nodeA.neighbors[RIGHT] = nodeB
        nodeA.neighbors[DOWN] = nodeC
        nodeB.neighbors[LEFT] = nodeA
        nodeB.neighbors[DOWN] = nodeD
        nodeC.neighbors[UP] = nodeA
        nodeC.neighbors[RIGHT] = nodeD
        nodeC.neighbors[DOWN] = nodeF
        nodeD.neighbors[UP] = nodeB
        nodeD.neighbors[LEFT] = nodeD
        nodeD.neighbors[RIGHT] = nodeE
        nodeE.neighbors[LEFT] = nodeD
        nodeE.neighbors[DOWN] = nodeG
        nodeF.neighbors[UP] = nodeC
        nodeF.neighbors[RIGHT] = nodeG
        nodeG.neighbors[UP] = nodeE
        nodeG.neighbors[LEFT] = nodeF
        self.nodeList = [nodeA, nodeB, nodeC, nodeD, nodeE, nodeF, nodeG]

     #renders the nodes to the screen
    def render(self, screen):
        for node in self.nodeList:
            node.render(screen)