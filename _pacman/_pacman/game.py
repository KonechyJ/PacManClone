import pygame as pg
from copy import copy
import game_functions as gf
from settings import Settings
from vector import Vector
from math import atan2
from timer import Timer
import time

 # class for the maze

class Maze:
    def __init__(self, game):
        self.screen = game.screen
        self.image = pg.image.load('images/maze.png')
        self.image = pg.transform.rotozoom(self.image, 0, 0.6)
        self.rect = self.image.get_rect()

    def update(self): self.draw()
    def draw(self): self.screen.blit(self.image, self.rect)

# class for the character
class Characters:
    def __init__(self, game, name, filename, scale, v, pt, pt_next, pt_prev):
        self.screen, self.screen_rect = game.screen, game.screen.get_rect()
        self.name = name
        self.pt, self.pt_next, self.pt_prev = pt, pt_next, pt_prev
        self.image = pg.image.load('images/' + filename)
        self.scale = scale
        self.origimage = self.image
        self.scale_factor = 1.0
        self.v = v
        self.prev_angle = 90.0
        curr_angle = self.angle()
        delta_angle = curr_angle - self.prev_angle
        self.prev_angle = curr_angle
        print(f'>>>>>>>>>>>>>>>>>>>>>>>> PREV ANGLE is {self.prev_angle}')
        self.last = self.pt
        if self.pt_prev is None: print("PT_PREV IS NONE NONE NONE NONE NONE")
        self.image = pg.transform.rotozoom(self.image, delta_angle, scale)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pt.x, pt.y


    def clamp(self):
        screen = self.screen_rect
        self.pt.x = max(0, min(self.pt.x, screen.width))
        self.pt.y = max(0, min(self.pt.y, screen.height))

    def enterPortal(self): pass

    def angle(self):
        return round((atan2(self.v.x, self.v.y) * 180.0 / 3.1415 - 90) % 360, 0)
        # return atan2(self.v.x, self.v.y) * 180.0 / 3.1415 + 180.0

    def update_angle(self):
        curr_angle = self.angle(self.v)
        delta_angle = curr_angle - self.prev_angle
        # self.image = pg.transform.rotozoom(self.image, delta_angle, 1.0)
        self.image = pg.transform.rotozoom(self.origimage, curr_angle - 90.0, self.scale)
        self.prev_angle = curr_angle


#updates movement  every frame
    def update(self):
       delta = self.pt - self.pt_next
       if delta.magnitude() > 2:
            self.prev_angle = self.pt
            self.pt += self.scale_factor * self.v
       self.clamp()
       if self.pt != self.last:
           print(f'{self.name}@{self.pt}')
           self.last = self.pt
       self.rect.centerx, self.rect.centery = self.pt.x, self.pt.y
       self.draw()

    def draw(self): self.screen.blit(self.image, self.rect)

class GridPoint:
    def __inti__(self, game,filename="star.png", scale=0.7, pt=(70,931), index=0, adj_list=[]):
        self.game = game
        self.screen = game.screen
        self.ptx, self.pty = pt[0], pt[1]
        image0 = pg.image.load('images/' + filename)
        image0 = pg.transform.rotorzoom(image0, 0, scale)
        image1 = pg.transform.rotorzoom(image0, 0, 1.1)
        image2 = pg.transform.rotorzoom(image0, 0, 1.2)
        image3 = pg.transform.rotorzoom(image0, 0, 1.3)
        images = [image0, image1, image2, image3]
        self.timer = Timer(images, wait=100)

    def update(self): self.draw()

    def draw(self):
        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.centerx, rect.centery = self.ptx, self.pty
        self.screen.blit(image, rect)

class Pacman(Characters):
    def __init__(self, game, name="Pacman", filename="ship.bmp", scale=0.55,
                 v=Vector(-1,0), pt=Vector(450,931), pt_next=Vector(70, 931),
                 pt_prev=Vector(900,931)):
        super().__init__(game=game, name=name, filename=filename, scale=scale,
                         v=v, pt=pt, pt_next=pt_next, pt_prev=pt_prev)

    def killGhost(self): pass
    def eatPoint(self): pass
    def eatFruit(self): pass
    def eatPowerPill(self): pass
    def firePortalGun(self, color): pass
    # def update(self):  self.draw()

    # def draw(): pass


class Ghost(Characters):
    def __init__(self, game, name="Pinky", filename="alien10.png", scale=0.8, v=Vector(-5,0), pt=Vector(450,400),
                 pt_next=Vector(450, 300), pt_prev=Vector(900,931)):
        super().__init__(game, name=name, filename=filename, scale=scale, v=v, pt=pt, pt_next=pt_next,
                         pt_prev=pt_prev)

    def switchToChase(self): pass
    def switchToRun(self): pass
    def switchToFlicker(self): pass
    def switchToIdle(self): pass
    def die(self): pass
    def killPacman(self): pass
    # def update(self):  self.draw()

    # def draw(): pass


# creates all the variables for the game
class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode(size=(self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("PacMan Portal")
        self.font = pg.font.SysFont(None, 48)
        self.maze = Maze(game=self)
        self.pacman = Pacman(game=self)
        # self.ghost = Ghost(game=self)
        self.stars = [GridPoint(game=self, pt=(x, 925)) for x in [70, 400, 500, 830]]
        self.stars1 = [GridPoint(game=self, pt=(x, 831)) for x in [70, 120, 210, 310, 400, 500, 590, 690, 780, 830]]
        self.stars2 = [GridPoint(game=self, pt=(x, 735)) for x in [70, 120, 210, 310, 400, 500, 590, 690, 780, 830]]
        self.stars3 = [GridPoint(game=self, pt=(x, 641)) for x in [70, 210, 310, 400, 500, 590, 690, 830]]
        self.stars4 = [GridPoint(game=self, pt=(x, 541)) for x in [210, 310, 400, 450, 500, 590, 690]]
        self.stars5 = [GridPoint(game=self, pt=(x, 445)) for x in [70, 210, 310, 400, 450, 500, 590, 690, 830]]
        self.stars6 = [GridPoint(game=self, pt=(x, 350)) for x in [210, 310, 400, 450, 500, 590, 690]]
        self.stars7 = [GridPoint(game=self, pt=(x, 255)) for x in [70, 210, 310, 400, 500, 590, 690, 830]]
        self.stars8 = [GridPoint(game=self, pt=(x, 160)) for x in [70, 210, 310, 400, 500, 590, 690, 830]]
        self.stars9 = [GridPoint(game=self, pt=(x, 70)) for x in [70, 210, 400, 500, 690, 830]]
        self.stars_stars = [self.stars, self.stars1, self.stars2, self.stars3,
                              self.stars4, self.stars5, self.stars6, self.stars7, self.stars8,
                              self.stars9]
        self.grid = self.create_grid()
        self.finished = False

    def to_pixel(self, grid):
        pixels = []

    def create_grid(self):
        row0 = [0, 4, 6, 10]
        row1 = [x for x in range(11) if x != 5]
        row2 = copy(row1)
        row3 = [x for x in range(11) if x not in [1, 5, 9]]
        row4 = [2, 3, 5, 7, 8]
        row5 = [x for x in range(11) if x not in [4, 5, 6]]
        row6 = [x for x in range(3, 8, 1)]
        row7 = copy(row3)
        row8 = [x for x in range(11) if x not in [1, 5, 9]]
        row9 = copy(row3)
        rows = [row0, row1, row2, row3, row4, row5, row6, row7, row8, row8]

        i = 0
        for row in rows:
            print(f'row {i} = {row}');
            i += 1
        return rows

    def play(self):
        while not self.finished:
            gf.check_events(game=self)
            # self.screen.fill(self.settings.bg_color)
            self.maze.update()
            self.pacman.update()
            for stars in self.stars_stars:
                for star in stars:
                    star.update()
            # self.ghost.update()

            pg.display.flip()

# main game function
def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()

