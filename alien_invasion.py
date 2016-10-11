#invasion

import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from alien import Alien
import game_functions as gf
from pygame.sprite import Group
from button import Button

def run_game():
#initialize pygame, settings, and screen object
    pygame.init()
#    bg = pygame.image.load("starfield4.png")   #curses! foiled!
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    ship = Ship(ai_settings, screen)
    pygame.display.set_caption("KILL ALL HUMANS")

    #make play button
    play_button = Button(ai_settings, screen, "KILL ALL HUMANS")
    #create xtats for scoreboard etc
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    #make a group of bullets and a group of aliens
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    while True:
#        gameDisplay.blit(bg, (0, 0))
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()
########comment!    !!
