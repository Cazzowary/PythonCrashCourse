#invasion

import pygame
from settings import Settings
from ship import Ship
import game_functions as gf



def run_game():
#initialize pygame, settings, and screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    ship = Ship(ai_settings, screen)
    pygame.display.set_caption("Jeff's Game")

    while True:
        gf.check_events(ship)
        gf.update_screen(ai_settings, screen, ship)
        ship.update()


run_game()
