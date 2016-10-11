class Settings():
    #a class to store all the Settings
    def __init__(self):
        #initialize the static settings
        #screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #ship settings
        self.ship_limit = 3

        #bullet settings
        self.bullet_speed_factor = 3
        self.bullet_height = 15
        self.bullet_width = 3
        self.bullet_color = (255, 96, 0)
        self.bullets_allowed = 10

        #alien settings
        self.fleet_drop_speed = 10

        #how quickly the game speeds up
        self.speedup_scale = 1.1

        #how quickly the score for each alien increase_speed
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        #init changeable settings
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        #fleet direction 1 = right -1 = left
        self.fleet_direction = 1

        #scoring
        self.alien_points =50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
