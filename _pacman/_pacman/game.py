#this is the main game file
import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from pauser import Pauser
from levels import LevelController
from text import TextGroup
from sprites import Spritesheet
from maze import Maze

#class to control the game
class GameController(object):
    def __init__(self):
        #This lines simple set up the game window for the game
        pygame.init()
        self.screen = pygame.display.set_mode(sceenSize, 0, 32)
        self.background = None
        self.background_flash = None
        self.setBackground()
        self.clock = pygame.time.Clock()
        self.pelletsEaten = 0
        self.fruit = None
        self.pause = Pauser(True)
        self.level = LevelController()
        self.text = TextGroup()
        self.sheet = Spritesheet()
        self.maze = Maze(self.sheet)
        self.flashBackground = False

    #this function fills the background with black
    def setBackground(self):
        self.background = pygame.surface.Surface(sceenSize).convert()
        self.background_flash = pygame.surface.Surface(sceenSize).convert()
        self.background.fill(BLACK)

    #This functions starts the game
    def startGame(self):
        self.level.reset()
        levelmap = self.level.getLevel()
        self.maze.getMaze(levelmap["mazename"].split(".")[0])
        self.maze.constructMaze(self.background, self.background_flash, row=levelmap["row"])
        self.nodes = NodeGroup(levelmap["mazename"])
        self.pellets = PelletGroup(levelmap["pelletname"])
        #creates the pacman game object
        self.pacman = Pacman(self.nodes, self.sheet)
        self.ghosts = GhostGroup(self.nodes, self.sheet)
        self.pelletsEaten = 0
        self.fruit = None
        self.pause.force(True)
        self.gameover = False
        self.score = 0
        self.text.showReady()
        self.text.updateLevel(self.level.level+1)
        self.maze.reset()
        self.flashBackground = False

    #Function called to start a new level only after the player has cleared the current one
    def startLevel(self):
        levelmap = self.level.getLevel()
        self.setBackground()
        self.maze.getMaze(levelmap["mazename"].split(".")[0])
        self.maze.constructMaze(self.background, self.background_flash, row=levelmap["row"])
        self.nodes = NodeGroup(levelmap["mazename"])
        self.pellets = PelletGroup(levelmap["pellet"])
        self.pacman.nodes = self.nodes
        self.pacman.reset()
        self.ghosts = GhostGroup(self.nodes, self.sheet)
        self.pelletsEaten = 0
        self.fruit = None
        self.pause.force(True)
        self.text.showReady()
        self.text.updateLevel(self.level.level + 1)
        self.maze.reset()
        self.flashBackground = False


    #update is called once per frame, so it will act as our game loop
    def update(self):
        #line is setting a 30 second value to Dt(delta time)
        if not self.gameover:
            dt = self.clock.tick(30) / 1000.0
            if not self.pause.paused:
                self.pacman.update(dt)
                self.ghosts.update(dt, self.pacman)
                if self.fruit is not None:
                    self.fruit.update(dt)
                if self.pause.pauseType != None:
                    self.pause.settlePause(self)
                self.checkPelletEvents()
                self.checkGhostEvents()
                self.checkFruitEvents()
            #condition checks to see if pacman is dead for death animation
            else:
                if self.pacman.animateDeath:
                    self.pacman.updateDeath(dt)
                if self.flashBackground:
                    self.maze.flash(dt)

            self.pause.update(dt)
            self.pellets.update(dt)
            self.text.update(dt)
        self.checkEvents()
        self.text.updateScore(self.score)
        self.render()

    #This functions checks for specific events to trigger something
    def checkEvents(self):
        #runs a loop to check every second if the game has exited and if a key is pressed.
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.gameover:
                        self.startGame()
                    else:
                        self.pause.player()
                        if self.pause.paused:
                            self.text.showPause()
                        else:
                            self.text.hideMessages()

    #This method will handle will handle all the pellet events
    #we are sending the whole pellet list to pacman and he returns the pellets he collides with
    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pelletsEaten += 1
            self.score += pellet.points
            if (self.pelletsEaten == 70 or self.pelletsEaten == 140):
                if self.fruit is None:
                    levelmap = self.level.getLevel()
                    self.fruit = Fruit(self.nodes, self.sheet, levelmap["fruit"])
            self.pellets.pelletList.remove(pellet)
            if pellet.name == "powerpellet":
                self.ghosts.resetPoints()
                self.ghosts.freightMode()
            if self.pellets.isEmpty():
                self.pacman.visible = False
                self.ghosts.hide()
                self.pause.startTimer(3, "clear")
                self.flashBackground = True

    #checks to see if pacman has hit a ghost, and if the ghost is in fright mode, then returns home at double the speed
    #now also checks to see if pacman has hit a ghost
    def checkGhostEvents(self):
        self.ghosts.release(self.pelletsEaten)
        ghost = self.pacman.eatGhost(self.ghosts)
        if ghost is not None:
            if ghost.mode.name == "FREIGHT":
                self.score += ghost.points
                self.text.createTemp(ghost.points, ghost.position)
                self.ghosts.updatePoints()
                ghost.spawnMode(speed=2)
                self.pause.startTimer(1)
                self.pacman.visible = False
                ghost.visible = False
            elif ghost.mode.name == "CHASE" or ghost.mode.name == "SCATTER":
                self.pacman.loseLife()
                self.ghosts.hide()
                self.pause.startTimer(3, "die")

    #Checks if the fruit has been destroyed after pacman eats it or its time runs out
    def checkFruitEvents(self):
        if self.fruit is not None:
            if self.pacman.eatFruit(self.fruit):
                self.score += self.fruit.points
                self.text.createTemp(self.fruit.points, self.fruit.position)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    # Checks to see if pacman is out of lives and then restarts the game fully
    def resolveDeath(self):
        if self.pacman.lives == 0:
            self.gameover = True
        else:
            self.restartLevel()
        self.pause.pauseType = None

    # this function is called after Pauser does its victory pause then proceeds to set the next level
    def resolveLevelClear(self):
        self.level.nextLevel()
        self.startLevel()
        self.pause.pauseType = None

    #This method will only reset pacman position in death, not the whole game
    def restartLevel(self):
        self.pacman.reset()
        self.ghosts = GhostGroup(self.nodes, self.sheet)
        self.fruit = None
        self.pause.force(True)
        self.text.showReady()
        self.maze.reset()
        self.flashBackground = False

    #this function will be used to draw images to the screen
    def render(self):
        self.screen.blit(self.maze.background, (0, 0))
        #self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.pacman.renderLives(self.screen)
        self.text.render(self.screen)
        pygame.display.update()

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
