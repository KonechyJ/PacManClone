import pygame
from pygame.locals import*
from vector import Vector2
from constants import *
from entity import Entity
from animation import Animation


#Pacman class
class Pacman(Entity):
    def __init__(self, nodes, spritesheet):
        #variables to set his name, color
        Entity.__init__(self, nodes, spritesheet)
        self.name = "pacman"
        self.color = YELLOW
        self.setStartPosition()
        self.lives = 5
        self.startImage = self.spritesheet.getImage(4, 0, 32, 32)
        self.image = self.startImage
        self.animation = None
        self.animations = {}
        self.defineAnimations()
        self.lifeicons = self.spritesheet.getImage(0, 1, 32, 32)

    #Checks the nodes in node list, and when it finds pacmans start node, it returns it
    def findStartNode(self):
        for node in self.nodes.nodeList:
            if node.pacmanStartNode:
                return node

    #resets pacman starting position
    def reset(self):
        self.setStartPosition()
        self.image = self.startImage

    #DEcreases the number of lives after death
    def loseLife(self):
        self.lives -= 1

    #This function draws little pacmans at the bottom to represent lives
    def renderLives(self, screen):
        for i in range(self.lives - 1):
            x = 10 + 42 * i
            y = tileHeight * nRows - 32
            screen.blit(self.lifeicons, (x, y))

    #sets all of pacmans starting features (IE his staring direction, his starting node, his next immediate target, etc..)
    def setStartPosition(self):
        self.direction = LEFT
        self.node = self.findStartNode()
        self.target = self.node.neighbors[self.direction]
        self.setPosition()
        self.position.x -= (self.node.position.x - self.target.position.x) / 2

    #This update function we calculate Pacman's postion
    def update(self, dt):
        self.visible = True
        self.position += self.direction*self.speed*dt
        self.updateAnimation(dt)
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


    #Uses the same collisson tatics to check and see if pacman has eaten the fruit
    def eatFruit(self, fruit):
        d = self.position - fruit.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + fruit.collideRadius) ** 2
        if dSquared <= rSquared:
            return True
        return False

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

    #this function simple defines all the frames we will use the the specific animations, and puts them into easy to use categories
    def defineAnimations(self):
        anim = Animation("loop")
        anim.speed = 30
        anim.addFrame(self.spritesheet.getImage(4, 0, 32, 32))
        anim.addFrame(self.spritesheet.getImage(0, 0, 32, 32))
        anim.addFrame(self.spritesheet.getImage(0, 1, 32, 32))
        anim.addFrame(self.spritesheet.getImage(0, 0, 32, 32))
        self.animations["left"] = anim

        anim = Animation("loop")
        anim.speed = 30
        anim.addFrame(self.spritesheet.getImage(4, 0, 32, 32))
        anim.addFrame(self.spritesheet.getImage(1, 0, 32, 32))
        anim.addFrame(self.spritesheet.getImage(1, 1, 32, 32))
        anim.addFrame(self.spritesheet.getImage(1, 0, 32, 32))
        self.animations["right"] = anim

        anim = Animation("loop")
        anim.speed = 30
        anim.addFrame(self.spritesheet.getImage(4, 0, 32, 32))
        anim.addFrame(self.spritesheet.getImage(2, 0, 32, 32))
        anim.addFrame(self.spritesheet.getImage(2, 1, 32, 32))
        anim.addFrame(self.spritesheet.getImage(2, 0, 32, 32))
        self.animations["down"] = anim

        anim = Animation("loop")
        anim.speed = 30
        anim.addFrame(self.spritesheet.getImage(4, 0, 32, 32))
        anim.addFrame(self.spritesheet.getImage(3, 0, 32, 32))
        anim.addFrame(self.spritesheet.getImage(3, 1, 32, 32))
        anim.addFrame(self.spritesheet.getImage(3, 0, 32, 32))
        self.animations["up"] = anim

        anim = Animation("once")
        anim.speed = 10
        anim.addFrame(self.spritesheet.getImage(0, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(1, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(2, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(3, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(4, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(5, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(6, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(7, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(8, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(9, 7, 32, 32))
        anim.addFrame(self.spritesheet.getImage(10, 7, 32, 32))
        self.animations["death"] = anim

        anim = Animation("static")
        anim.addFrame(self.spritesheet.getImage(4, 0, 32, 32))
        self.animations["idle"] = anim

    #applies the animations defined above to the various movements
    #TODO possibly could add the moveement sounds here
    def updateAnimation(self, dt):
        if self.direction == UP:
            self.animation = self.animations["up"]
        elif self.direction == DOWN:
            self.animation = self.animations["down"]
        elif self.direction == LEFT:
            self.animation = self.animations["left"]
        elif self.direction == RIGHT:
            self.animation = self.animations["right"]
        elif self.direction == STOP:
            self.animation = self.animations["idle"]
        self.image = self.animation.update(dt)

