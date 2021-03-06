import pygame
from entity import MazeRunner
from constants import *
from vector import Vector2
from random import randint
from modes import Mode
from stack import Stack
from animation import Animation

#This class will handle all ghost funtionality and will inherit from entity
class Ghost(MazeRunner):
    def __init__(self, nodes, spritesheet):
        MazeRunner.__init__(self, nodes, spritesheet)
        self.name = "ghost"
        self.goal = Vector2()
        self.modeStack = self.setupModeStack()
        self.mode = self.modeStack.pop()
        self.modeTimer = 0
        self.spawnNode = self.findSpawnNode()
        self.setGuideStack()
        self.pelletsForRelease = 0
        self.released = True
        self.bannedDirections = []
        self.setStartPosition()
        self.points = 200
        self.animation = None
        self.animations = {}

    def findStartNode(self):
        for node in self.nodes.homeList:
            if node.homeEntrance:
                return node
        return node

    # This method wont change for each ghost but in each ghost class, we will customize the findStartNode() method
    def setStartPosition(self):
        self.node = self.findStartNode()
        self.target = self.node
        self.setPosition()

    # This functions will take in the list of directions and calculate which will get it closest to its current goal
    def getClosestDirection(self, validDirections):
        distances = []
        for direction in validDirections:
            diffVec = self.node.position + direction * TILEWIDTH - self.goal
            distances.append(diffVec.magnitudeSquared())
        index = distances.index(min(distances))
        return validDirections[index]

    # This functions builds a list of valid directions for the ghost to use
    # then uses a for loop to fill the list below
    # if statements added to make sure the ghost can only enter the spawn room in SPAWN MODE
    def getValidDirections(self):
        validDirections = []
        for key in self.node.neighbors.keys():
            if self.node.neighbors[key] is not None:
                if key != self.direction * -1:
                    if not self.mode.name == "SPAWN":
                        if not self.node.homeEntrance:
                            if key not in self.bannedDirections:
                                validDirections.append(key)
                        else:
                            if key != DOWN:
                                validDirections.append(key)
                    else:
                        validDirections.append(key)
        if len(validDirections) == 0:
            validDirections.append(self.forceBacktrack())
        return validDirections

    # this function will get a list of random directions by calling the previously made function
    def randomDirection(self, validDirections):
        index = randint(0, len(validDirections) - 1)
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
            # if spawn mode is reached, then goal is set to the new position and the mode is popped off the stack
            # so that it doesn't repeat
            if self.mode.name == "SPAWN":
                if self.position == self.goal:  # reached the spawn goal
                    self.mode = self.modeStack.pop()  # should be the first GUIDE mode
                    self.direction = self.mode.direction
                    self.target = self.node.neighbors[self.direction]
                    self.setPosition()
            # here  we want to make sure that all the modes created by a ghost going into fright mood are popped off
            # so that the ghost can return to normal after SPAWN AND GUIDE have done their part
            elif self.mode.name == "GUIDE":
                self.mode = self.modeStack.pop()
                if self.mode.name == "GUIDE":  # We're still guiding
                    self.direction = self.mode.direction
                    self.target = self.node.neighbors[self.direction]
                    self.setPosition()

    # This fuicntion we are overwriting entity's reverse direction function in the case of ghost bing in SPAWN or GUIDE MODE
    def reverseDirection(self):
        if self.mode.name != "GUIDE" and self.mode.name != "SPAWN":
            MazeRunner.reverseDirection(self)

    # This function is simplely setting up the stack with a "random" amount of modes for the ghost
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

    # This function tells the ghost what to do in the SCATTER mode
    def scatterGoal(self):
        self.goal = Vector2(SCREENSIZE[0], 0)

    # this function tells the ghost what to do in the CHASE function
    def chaseGoal(self, pacman, blinky=None):
        self.goal = pacman.position

    # THis update will handle the mode the ghost is in by constantly checking the time and poppping modes off the stack when prompted
    # it also changes direction when a mode changes
    def modeUpdate(self, dt):
        self.modeTimer += dt
        if self.mode.time is not None:
            if self.modeTimer >= self.mode.time:
                self.reverseDirection()
                self.mode = self.modeStack.pop()
                self.modeTimer = 0

    # This update is here to overwrite the one in entity, it is passed pacman so that ghost can get his position in CHASE mode
    # depending on the current mode, the goal of pacman will be set to either pacman or a distance point
    def update(self, dt, pacman, blinky):
        self.visible = True
        self.portalSlowdown()
        speedMod = self.speed * self.mode.speedMult
        self.position += self.direction * speedMod * dt
        self.modeUpdate(dt)
        if self.mode.name == "CHASE":
            self.chaseGoal(pacman, blinky)
        elif self.mode.name == "SCATTER":
            self.scatterGoal()
        elif self.mode.name == "FREIGHT":
            self.randomGoal()
        elif self.mode.name == "SPAWN":
            self.spawnGoal()
        self.moveBySelf()
        self.updateAnimation(dt)

    # This function is here to slow down a ghost incase a ghost corners pacman near a portal
    def portalSlowdown(self):
        self.speed = 100
        if self.node.portalNode or self.target.portalNode:
            self.speed = 50

    # This method checls to see if the mode is not spawn and then intiaties fright mode
    def freightMode(self):
        if self.mode.name != "SPAWN" and self.mode.name != "GUIDE":
            if self.mode.name != "FREIGHT":
                if self.mode.time is not None:
                    dt = self.mode.time - self.modeTimer
                    self.modeStack.push(Mode(name=self.mode.name, time=dt))
                else:
                    self.modeStack.push(Mode(name=self.mode.name))
                self.mode = Mode("FREIGHT", time=7, speedMult=0.5)
                self.modeTimer = 0
            else:
                self.mode = Mode("FREIGHT", time=7, speedMult=0.5)
                self.modeTimer = 0
            self.reverseDirection()

    # a function to give the ghost random movement during fright mode
    def randomGoal(self):
        x = randint(0, NCOLS * TILEWIDTH)
        y = randint(0, NROWS * TILEHEIGHT)
        self.goal = Vector2(x, y)

    # Called when the ghost goes into SPAWN mode, sends him/her back to spawn quickly
    def spawnMode(self, speed=1):
        self.mode = Mode("SPAWN", speedMult=speed)
        self.modeTimer = 0
        for d in self.guide:
            self.modeStack.push(Mode("GUIDE", speedMult=0.5, direction=d))

    # This function will run when ghost is created so we have an easy reference to where spawn is
    def findSpawnNode(self):
        for node in self.nodes.homeList:
            if node.spawnNode:
                break
        return node

    # simply sets the ghost goal to spawn node
    def spawnGoal(self):
        self.goal = self.spawnNode.position

    #Sets up a stack of directions needed to be follow after return home fuicntion is called for ghost
    #to prevent them from getting trapped
    def setGuideStack(self):
        self.guide = [UP]

    # this function will help the ghost incase it comes to a deadend by checking the directions at a node.
    def forceBacktrack(self):
        if self.direction * -1 == UP:
            return UP
        if self.direction * -1 == DOWN:
            return DOWN
        if self.direction * -1 == LEFT:
            return LEFT
        if self.direction * -1 == RIGHT:
            return RIGHT

    ##this function simple defines all the frames we will use the the specific animations, and puts them into easy to use categories
    def defineAnimations(self, row):
        anim = Animation("loop")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(0, row, TILEWIDTH * 2, TILEHEIGHT * 2))
        anim.addFrame(self.spritesheet.getImage(1, row, TILEWIDTH * 2, TILEHEIGHT * 2))
        self.animations["up"] = anim

        anim = Animation("loop")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(2, row, TILEWIDTH * 2, TILEHEIGHT * 2))
        anim.addFrame(self.spritesheet.getImage(3, row, TILEWIDTH * 2, TILEHEIGHT * 2))
        self.animations["down"] = anim

        anim = Animation("loop")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(4, row, TILEWIDTH * 2, TILEHEIGHT * 2))
        anim.addFrame(self.spritesheet.getImage(5, row, TILEWIDTH * 2, TILEHEIGHT * 2))
        self.animations["left"] = anim

        anim = Animation("loop")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(6, row, TILEWIDTH * 2, TILEHEIGHT * 2))
        anim.addFrame(self.spritesheet.getImage(7, row, TILEWIDTH * 2, TILEHEIGHT * 2))
        self.animations["right"] = anim

        anim = Animation("loop")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(0, 6, TILEWIDTH * 2, TILEHEIGHT * 2))
        anim.addFrame(self.spritesheet.getImage(1, 6, TILEWIDTH * 2, TILEHEIGHT * 2))
        self.animations["freight"] = anim

        anim = Animation("loop")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(0, 6, TILEWIDTH * 2, TILEHEIGHT * 2))
        anim.addFrame(self.spritesheet.getImage(2, 6, TILEWIDTH * 2, TILEHEIGHT * 2))
        anim.addFrame(self.spritesheet.getImage(1, 6, TILEWIDTH * 2, TILEHEIGHT * 2))
        anim.addFrame(self.spritesheet.getImage(3, 6, TILEWIDTH * 2, TILEHEIGHT * 2))
        self.animations["flash"] = anim

        anim = Animation("static")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(4, 6, TILEWIDTH * 2, TILEHEIGHT * 2))
        self.animations["spawnup"] = anim

        anim = Animation("static")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(5, 6, TILEWIDTH * 2, TILEHEIGHT * 2))
        self.animations["spawndown"] = anim

        anim = Animation("static")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(6, 6, TILEWIDTH * 2, TILEHEIGHT * 2))
        self.animations["spawnleft"] = anim

        anim = Animation("static")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(7, 6, TILEWIDTH * 2, TILEHEIGHT * 2))
        self.animations["spawnright"] = anim

    # applies the animations defined above to the various movements and moods
    def updateAnimation(self, dt):
        if self.mode.name == "SPAWN":
            if self.direction == UP:
                self.animation = self.animations["spawnup"]
            elif self.direction == DOWN:
                self.animation = self.animations["spawndown"]
            elif self.direction == LEFT:
                self.animation = self.animations["spawnleft"]
            elif self.direction == RIGHT:
                self.animation = self.animations["spawnright"]

        if self.mode.name in ["CHASE", "SCATTER"]:
            if self.direction == UP:
                self.animation = self.animations["up"]
            elif self.direction == DOWN:
                self.animation = self.animations["down"]
            elif self.direction == LEFT:
                self.animation = self.animations["left"]
            elif self.direction == RIGHT:
                self.animation = self.animations["right"]

        if self.mode.name == "FREIGHT":
            if self.modeTimer >= (self.mode.time * 0.7):
                self.animation = self.animations["flash"]
            else:
                self.animation = self.animations["freight"]
        self.image = self.animation.update(dt)

# class that inherits from ghost for Blinky (Red ghost) and the most simple of them all
class Blinky(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet)
        self.name = "blinky"
        self.color = RED
        self.image = self.spritesheet.getImage(4, 2, TILEWIDTH * 2, TILEHEIGHT * 2)
        self.defineAnimations(2)
        self.animation = self.animations["left"]

#Pink ghost class that inherits from ghost, slightly different scatter and chase goal
class Pinky(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet)
        self.name = "pinky"
        self.color = PINK
        self.image = self.spritesheet.getImage(0, 3, TILEWIDTH * 2, TILEHEIGHT * 2)
        self.defineAnimations(3)
        self.animation = self.animations["up"]

    # her scatter goal is different than blinky, upper left corner of maze
    def scatterGoal(self):
        self.goal = Vector2()

    # her chase method hunts 4 titles ahead of pacman
    def chaseGoal(self, pacman, blinky=None):
        self.goal = pacman.position + pacman.direction * TILEWIDTH * 4

    # this method finds pinkys start node and returns it
    def setStartPosition(self):
        startNode = self.findStartNode()
        self.node = startNode.neighbors[DOWN]
        self.target = self.node
        self.setPosition()

#cyan ghost class that inherits from ghost class
class Inky(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet)
        self.name = "inky"
        self.color = TEAL
        self.pelletsForRelease = 30
        self.released = False
        self.image = self.spritesheet.getImage(2, 4, TILEWIDTH * 2, TILEHEIGHT * 2)
        self.defineAnimations(4)
        self.animation = self.animations["down"]

    # her scatter goal is to the bottom right corner of the maze
    def scatterGoal(self):
        self.goal = Vector2(TILEWIDTH * NCOLS, TILEHEIGHT * NROWS)

    # her chase goal is to find 2 tiles ahead of pacman man, while subtracting Blinkys postion and multiplying by 2. then adding it to blinky's postion
    def chaseGoal(self, pacman, blinky=None):
        vec1 = pacman.position + pacman.direction * TILEWIDTH * 2
        vec2 = (vec1 - blinky.position) * 2
        self.goal = blinky.position + vec2

    def setStartPosition(self):
        self.bannedDirections = [RIGHT]
        startNode = self.findStartNode()
        pinkyNode = startNode.neighbors[DOWN]
        self.node = pinkyNode.neighbors[LEFT]
        self.target = self.node
        self.spawnNode = pinkyNode.neighbors[LEFT]
        self.setPosition()

    #we are overwriting this method from ghost(or entity) with specific instructions for inky
    def setGuideStack(self):
        self.guide = [UP, RIGHT]

#last ghost class (orange) to inherit fro Ghost
class Clyde(Ghost):
    def __init__(self, nodes, spritesheet):
        Ghost.__init__(self, nodes, spritesheet)
        self.name = "clyde"
        self.color = ORANGE
        self.pelletsForRelease = 60
        self.released = False
        self.image = self.spritesheet.getImage(2, 5, TILEWIDTH * 2, TILEHEIGHT * 2)
        self.defineAnimations(5)
        self.animation = self.animations["down"]

    # scatters to the bottom left of the mazee
    def scatterGoal(self):
        self.goal = Vector2(0, TILEHEIGHT * NROWS)

    # his chase goal is determined by how close he is to pacman
    # if he is < 8 spaces away, then he scatters.
    # when he is >8 spaces away, he acts like pinky
    def chaseGoal(self, pacman, blinky=None):
        d = pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (TILEWIDTH * 8) ** 2:
            self.scatterGoal()
        else:
            self.goal = pacman.position + pacman.direction * TILEWIDTH * 4

    def setStartPosition(self):
        self.bannedDirections = [LEFT]
        startNode = self.findStartNode()
        pinkyNode = startNode.neighbors[DOWN]
        self.node = pinkyNode.neighbors[RIGHT]
        self.spawnNode = pinkyNode.neighbors[RIGHT]
        self.target = self.node
        self.setPosition()

    # this method finds inkys start node and returns it
    def setGuideStack(self):
        self.guide = [UP, LEFT]

#class for storing all the ghosts as a group
class GhostGroup(object):
    def __init__(self, nodes, spritesheet):
        self.nodes = nodes
        self.ghosts = [Blinky(nodes, spritesheet),
                       Pinky(nodes, spritesheet),
                       Inky(nodes, spritesheet),
                       Clyde(nodes, spritesheet)]

    # function to let us loop through all the ghosts in the list
    def __iter__(self):
        return iter(self.ghosts)

    # runs update for all the ghosts
    def update(self, dt, pacman):
        for ghost in self:
            ghost.update(dt, pacman, self.ghosts[0])

    # runs frieght mode for all the ghosts
    def freightMode(self):
        for ghost in self:
            ghost.freightMode()

    # this method loops through all the ghost and releases them after their conditions have been met
    def release(self, numPelletsEaten):
        for ghost in self:
            if not ghost.released:
                if numPelletsEaten >= ghost.pelletsForRelease:
                    ghost.bannedDirections = []
                    ghost.spawnMode()
                    ghost.released = True

    # this one updates point values everytime he eats a ghost
    def updatePoints(self):
        for ghost in self:
            ghost.points *= 2

    # resets the points for ghost
    def resetPoints(self):
        for ghost in self:
            ghost.points = 200

    # runs hides for all the ghosts
    def hide(self):
        for ghost in self:
            ghost.visible = False

    # draws them to screen
    def render(self, screen):
        for ghost in self:
            ghost.render(screen)
