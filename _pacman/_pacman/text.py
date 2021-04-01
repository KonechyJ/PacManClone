import pygame
from vector import Vector2
from constants import *

#this class object will handle the creation of the texts
class Text(object):
    def __init__(self, text, color, x, y, size, show=True):
        self.text = text
        self.color = color
        self.size = size
        self.position = Vector2(x, y)
        self.show = show
        self.label = None
        self.font = None
        self.totalTime = 0
        self.lifespan = 0
        self.setupFont("PressStart2P-Regular.ttf")
        self.createLabel()

    #sets up the font to be used for the text in the game
    def setupFont(self, fontpath):
        self.font = pygame.font.Font(fontpath, self.size)

    #creates the object the that will display the text font
    def createLabel(self):
        self.label = self.font.render(self.text, 1, self.color)

    #creates the text object and calls createlabel
    def setText(self, newtext):
        self.text = newtext
        self.createLabel()

    #updates the screen every second to change the text as needed, like score
    def update(self, dt):
        if self.lifespan > 0:
            self.totalTime += dt
            if self.totalTime >= self.lifespan:
                self.totalTime = 0
                self.show = False
                self.lifespan = 0

    #draws the text the text to the screen
    def render(self, screen):
        if self.show:
            x, y = self.position.asTuple()
            screen.blit(self.label, (x, y))

#this class will group the texts together into one collection and then display them as needed
class TextGroup(object):
    def __init__(self):
        self.textlist = {}
        self.setupText()
        self.tempText = []

    #creates the specifics for each of the texts we will be using
    def setupText(self):
        self.textlist["score_label"] = Text("SCORE", WHITE, 0, 0, 16)
        self.textlist["level_label"] = Text("LEVEL", WHITE, 368, 0, 16)
        self.textlist["score"] = Text("0".zfill(8), WHITE, 0, 16, 16)
        self.textlist["level"] = Text("0".zfill(3), WHITE, 368, 16, 16)
        self.textlist["ready"] = Text("READY!", YELLOW, 180, 320, 16, False)
        self.textlist["paused"] = Text("PAUSED!", YELLOW, 170, 320, 16, False)
        self.textlist["gameover"] = Text("GAMEOVER!", RED, 160, 320, 16, False)

    # updates the screen every second to change the text as needed, like score
    def update(self, dt):
        if len(self.tempText) > 0:
            tempText = []
            for text in self.tempText:
                text.update(dt)
                if text.show:
                    tempText.append(text)
            self.tempText = tempText

    #updates the score visually as pellets are eaten
    def updateScore(self, score):
        self.textlist["score"].setText(str(score).zfill(8))

    #updates the level text as needed
    def updateLevel(self, level):
        self.textlist["level"].setText(str(level).zfill(3))

    #function to set each bool to true or false, depending on which text is needed when this specific function is called
    def showReady(self):
        self.textlist["ready"].show = True
        self.textlist["paused"].show = False
        self.textlist["gameover"].show = False

    # function to set each bool to true or false, depending on which text is needed when this specific function is called
    def showPause(self):
        self.textlist["ready"].show = False
        self.textlist["paused"].show = True
        self.textlist["gameover"].show = False

    # function to set each bool to true or false, depending on which text is needed when this specific function is called
    def showGameOver(self):
        self.textlist["ready"].show = False
        self.textlist["paused"].show = False
        self.textlist["gameover"].show = True

    #hides all the messages
    def hideMessages(self):
        self.textlist["ready"].show = False
        self.textlist["paused"].show = False
        self.textlist["gameover"].show = False

    #creates a temp object to be used when needed to quickly display something
    def createTemp(self, value, position):
        x, y = position.asTuple()
        text = Text(str(value), WHITE, x, y, 8)
        text.lifespan = 1
        self.tempText.append(text)

    #draws all the texts objects to the screen
    def render(self, screen):
        for key in self.textlist.keys():
            self.textlist[key].render(screen)

        for item in self.tempText:
            item.render(screen)