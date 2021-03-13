import pygame as pg
from copy import copy
import game_functions as gf
from settings import Settings
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
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.ship_image = pg.image.load('images/ship.bmp')
        self.alien_image = pg.image.load('images/alien10.png')
        self.ship_image = pg.transform.rotozoom(self.ship_image, 0, 0.8)
        self.alien_image = pg.transform.rotozoom(self.alien_image, 0, 0.75)

        self.ship_rect = self.ship_image.get_rect()
        self.alien_rect = self.alien_image.get_rect()

#updates movement  every frame
    def update(self, event, ship):
        # TODO:  update position
        r = self.screen_rect
        self.ship_rect.centerx, self.ship_rect.bottom = r.centerx, r.bottom - 50
        self.alien_rect.centerx, self.alien_rect.centery = r.centerx, r.centery + 45

        if event.key == pg.K_RIGHT: ship.moving_right = True
        self.ship_rect.centerx, self.ship_rect.bottom = r.centerx, r.bottom - 50

        self.draw()

    def draw(self):
        self.screen.blit(self.ship_image, self.ship_rect)
        self.screen.blit(self.alien_image, self.alien_rect)

# creates all the variables for the game
class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode(size=(self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("PacMan Portal")
        self.font = pg.font.SysFont(None, 48)
        self.maze = Maze(game=self)
        self.characters = Characters(game=self)
        self.grid = self.create_grid()
        self.finished = False

    def to_pixel(self, grid):
        pixels = []

# creates the grid in a theoretical sense, the grid points havent been create yet

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


# play function calls the events to update the maze and characters
    def play(self):
        while not self.finished:
            gf.check_events(game=self)
            # self.screen.fill(self.settings.bg_color)
            self.maze.update()
            self.characters.update()

            pg.display.flip()


# main game function
def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()

