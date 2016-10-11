#bullet class
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    #this class manages the bullets
    def __init__(self, ai_settings, screen, ship):
        #create bullet object at ship's location
        super(Bullet, self).__init__()
        self.screen = screen

        #create a bullet rect at (0, 0) and then set correct position.
        """not sure what the 'R' does, but it fucks this game uppppp if you make it an 'r'!"""
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx  #this moves the bullet to the ship's location
        self.rect.top = ship.rect.top

        #store bullet location as a decimal
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        #move bullet up the screen
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
