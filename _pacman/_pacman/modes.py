
#this class currently handles the different modes that will be used for the ghost;
# IE scatter, frieght, chase, etc..
class Mode(object):
    def __init__(self, name="", time=None, speedMult=1, direction=None):
        self.name = name
        self.time = time
        self.speedMult = speedMult
        self.direction = direction
