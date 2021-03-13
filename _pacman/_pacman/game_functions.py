import sys
import pygame as pg

#checks for key down events
def check_keydown_events(event, ship, sound):
    if event.key == pg.K_RIGHT: ship.moving_right = True
    elif event.key == pg.K_LEFT: ship.moving_left = True
    # elif event.key == pg.K_SPACE: ship.shooting_bullets = True

#checks for key up events
def check_keyup_events(event, ship):
    if event.key == pg.K_RIGHT: ship.moving_right = False
    elif event.key == pg.K_LEFT: ship.moving_left = False
    # if event.key == pg.K_q: ship.shooting_bullets = False

# def check_play_button(stats, play_button, mouse_x, mouse_y):
#     if play_button.rect.collidepoint(mouse_x, mouse_y):
#         stats.game_active = True

def check_events(game):
    # Watch for keyboard and mouse events.
    for event in pg.event.get():
        if event.type == pg.QUIT: game.finished = True
        # elif event.type == pg.MOUSEBUTTONDOWN:
        #     mouse_x, mouse_y = pg.mouse.get_pos()
        #     # check_play_button(stats=game.stats, play_button=game.play_button, mouse_x=mouse_x, mouse_y=mouse_y)
        # elif event.type == pg.KEYDOWN: check_keydown_events(event=event, ship=game.ship, sound=game.sound)
        # elif event.type == pg.KEYUP: check_keyup_events(event=event, ship=game.ship)

