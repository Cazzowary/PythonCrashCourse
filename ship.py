import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        #initialize ship and starting position
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #load ship image and get its rect (lol)
        self.image = pygame.image.load('images/ufo.bmp')
        self.rect = self.image.get_rect() #lmaooooo
        self.screen_rect = screen.get_rect()

        #start new ships at the bottom of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #set decimal value for ships center to make movement by non-ints easier
        self.center = float(self.rect.centerx)
#        self.centery = float(self.rect.centery)
        #Movement flag
        self.moving_right = False
        self.moving_left = False
#        self.moving_up = False
#        self.moving_down = False

    def update(self):
        #update ship's position based on movement flag
#        self.y -= self.ship_speed_factor
#        self.rect.y = self.y
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
#        if self.moving_up and self.rect.up < self.screen_rect.up:
#            self.centery += self.ai_settings.ship_speed_factor
#        if self.moving_down and self.rect.down > 0:
#            self.centery -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center



    def blitme(self):
        #draw ship
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        #center the ship after collisions
        self.center = self.screen_rect.centerx
