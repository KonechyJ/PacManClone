
#class to handle the animation for anything that deals with frames
class Animation(object):
    def __init__(self, animType):
        self.animType = animType
        self.frames = []
        self.current_frame = 0
        self.finished = False
        self.speed = 0
        self.dt = 0

    #this function we reset the animation loop once a non looping animation has finsihed
    def reset(self):
        self.current_frame = 0
        self.finished = False

    #adds a frame to the animation loop
    def addFrame(self, frame):
        self.frames.append(frame)

    #uses if statements to check with animation is being called, then applies the appropirtate loop
    def update(self, dt):
        if self.animType == "loop":
            self.loop(dt)
        elif self.animType == "once":
            self.once(dt)
        elif self.animType == "static":
            self.current_frame = 0
        return self.frames[self.current_frame]

    #method used to loop to the next frame at the speed of 1 frame a second
    def nextFrame(self, dt):
        self.dt += dt
        if self.dt >= (1.0 / self.speed):
            self.current_frame += 1
            self.dt = 0

    #loops the animations
    def loop(self, dt):
        self.nextFrame(dt)
        if self.current_frame == len(self.frames):
            self.current_frame = 0

    #loops the frames in animation once (like in the death frames)
    def once(self, dt):
        if not self.finished:
            self.nextFrame(dt)
            if self.current_frame == len(self.frames) - 1:
                self.finished = True
