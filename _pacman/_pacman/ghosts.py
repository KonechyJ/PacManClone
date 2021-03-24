import pygame
from entity import Entity
from constants import *
from vector import Vector2
from random import randint
from modes import Mode
from stack import Stack

#This class will handle all ghost funtionality and will inherit from entity
class Ghost(Entity):
    def __init__(self, nodes):
        Entity.__init__(self, nodes)
        self.name = "ghost"
        self.goal = Vector2()
        self.points = 200
        self.modeStack = self.setupModeStack()
        self.mode = self.modeStack.pop()
        self.modeTimer = 0

    # This functions builds a list of valid directions for the ghost to use
    # then uses a for loop to fill the list below
    def getValidDirections(self):
        validDirections = []
        for key in self.node.neighbors.keys():
            if self.node.neighbors[key] is not None:
                if key != self.direction * -1:
                    validDirections.append(key)
        if len(validDirections) == 0:
            validDirections.append(self.forceBacktrack())
        return validDirections

    # this function will get a list of random directions by calling the previously made function
    def randomDirection(self, validDirections):
        index = randint(0, len(validDirections) - 1)
        return validDirections[index]

    # This functions will take in the list of directions and calculate which will get it closest to its current goal
    def getClosestDirection(self, validDirections):
        distances = []
        for direction in validDirections:
            diffVec = self.node.position + direction * tileWidth - self.goal
            distances.append(diffVec.magnitudeSquared())
        index = distances.index(min(distances))
        return validDirections[index]

    # This moveByself function will need to overwrite the one in entity which is why it is here
    # this one will handle the movement differently than the pacman class
    def moveBySelf(self):
        if self.overshotTarget():
            self.node = self.target
            self.portal()
            validDirections = self.getValidDirections()
            self.direction = self.getClosestDirection(validDirections)
            self.target = self.node.neighbors[self.direction]
            self.setPosition()

    # this function will help the ghost incase it comes to a deadend by checking the directions at a node.
    #
    def forceBacktrack(self):
        if self.direction * -1 == UP:
            return UP
        if self.direction * -1 == DOWN:
            return DOWN
        if self.direction * -1 == LEFT:
            return LEFT
        if self.direction * -1 == RIGHT:
            return RIGHT

    # This function is here to slow down a ghost incase a ghost corners pacman near a portal
    def portalSlowdown(self):
        self.speed = 100
        if self.node.portalNode or self.target.portalNode:
            self.speed = 50

    #This function is simplely setting up the stack with a "random" amount of modes for the ghost
    def setupModeStack(self):
        modes = Stack()
        modes.push(Mode(name="CHASE"))
        modes.push(Mode(name="SCATTER", time=5))
        modes.push(Mode(name="CHASE", time=20))
        modes.push(Mode(name="SCATTER", time=7))
        modes.push(Mode(name="CHASE", time=20))
        modes.push(Mode(name="SCATTER", time=7))
        modes.push(Mode(name="CHASE", time=20))
        modes.push(Mode(name="SCATTER", time=7))
        return modes

    #This function tells the ghost what to do in the SCATTER mode
    def scatterGoal(self):
        self.goal = Vector2(sceenSize[0], 0)

    #this function tells the ghost what to do in the CHASE function
    def chaseGoal(self, pacman, blinky=None):
        self.goal = pacman.position

    #THis update will handle the mode the ghost is in by constantly checking the time and poppping modes off the stack when prompted
    #it also changes direction when a mode changes
    def modeUpdate(self, dt):
        self.modeTimer += dt
        if self.modeTimer is not None:
            if self.modeTimer >= self.mode.time:
                self.reverseDirection()
                self.mode = self.modeStack.pop()
                self.modeTimer = 0

    #This update is here to overwrite the one in entity, it is passed pacman so that ghost can get his position in CHASE mode
    #depending on the current mode, the goal of pacman will be set to either pacman or a distance point
    def update(self, dt, pacman, blinky=None):
        self.visible = True
        self.portalSlowdown()
        speedMod = self.speed * self.mode.speedMult
        self.position += self.direction*speedMod*dt
        self.modeUpdate(dt)
        if self.mode.name == "CHASE":
            self.chaseGoal(pacman, blinky)
        elif self.mode.name == "SCATTER":
            self.scatterGoal()
        self.moveBySelf()

