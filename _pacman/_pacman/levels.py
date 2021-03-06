
#this class will handle the functionality of chhanging levels once a level is complete
class LevelController(object):
    def __init__(self):
        # current level below and all its components in a dictionary
        self.level = 0
        self.levelmaps = {0: {"name": "maze1.txt", "row": 0, "fruit": "cherry"},
                          1: {"name": "maze2.txt", "row": 1, "fruit": "banana"},
                          2: {"name": "maze3.txt", "row": 2, "fruit": "apple"}}

    # this function helps us keep track of what level we are on
    def nextLevel(self):
        self.level += 1

    #function used to reset to level 1 whenever needed (DEATH, etc...)
    def reset(self):
        self.level = 0

    # functions tells what map to use in which level
    def getLevel(self):
        return self.levelmaps[self.level % len(self.levelmaps)]
