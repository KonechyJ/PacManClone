

#this class will handle all the functionality for pausing the game
class Pauser(object):
    def __init__(self, paused=False):
        self.paused = paused
        self.timer = 0
        self.pauseTime = 0
        self.playerPaused = paused
        self.pauseType = None  # (clear, die, ghost)

    #this method keeps tracks of how much time has passed while paused, then unpauses game after time is up
    def update(self, dt):
        if not self.playerPaused:
            if self.paused:
                self.timer += dt
                if self.timer >= self.pauseTime:
                    self.timer = 0
                    self.paused = False

    #starts the timer for a specified amount of seconds when told to do so
    def startTimer(self, pauseTime, pauseType=None):
        self.pauseTime = pauseTime
        self.pauseType = pauseType
        self.timer = 0
        self.paused = True

    #this is player pause, so it is unaffected by update. unlimited pause
    def player(self):
        self.playerPaused = not self.playerPaused
        if self.playerPaused:
            self.paused = True
        else:
            self.paused = False

    #this  method forces us to pause at any time (mostly testing purposes)
    def force(self, pause):
        self.paused = pause
        self.playerPaused = pause
        self.timer = 0
        self.pauseTime = 0

    #this pause method is specifically going to check for a die or complete condition
    def settlePause(self, gamecontroller):
        if self.pauseType == "die":
            gamecontroller.resolveDeath()
        elif self.pauseType == "clear":
            gamecontroller.resolveLevelClear()

