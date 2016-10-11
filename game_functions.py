import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
        bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #reset game settings
        ai_settings.initialize_dynamic_settings()
        #make the mouse invisible
        pygame.mouse.set_visible(False)
        #reset game stats
        stats.reset_stats()
        stats.game_active = True

        #reset score images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    #lose a ship on impact w alien
    if stats.ships_remaining > 0:
            stats.ships_remaining -= 1

            #update scoreboard
            sb.prep_score()

            #erase bullets and current fleet from screen
            aliens.empty()
            bullets.empty()
            #create a new fleet and recenter the players ship
            create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()
            #pause the game for a moment to give player time to regroup
            sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def get_number_aliens_x(ai_settings, alien_width):
    #determine number of aliens that fit on a row
    available_space_x = ai_settings.screen_width - 2 *alien_width #fleet covers all of screen width minus two alien widths
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    #determine num rows of aliens that fit on screen
    available_space_y = (ai_settings.screen_height -
                                        (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    #create an alien and place it on the row
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.y = alien_height + 2 * alien_height * row_number
    alien.rect.x = alien.x
    alien.rect.y = alien.y

    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    #create full fleet of aliens
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    #increase alien speed whenever fleet is erased
    if len(aliens) == 0:
        ai_settings.alien_speed_factor += .2

    for row_number in range(number_rows):
        for alien_number in range (number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_keydown_events(event, ai_settings, screen, ship, bullets):
        if event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            ship.moving_left = True
#        elif event.key == pygame.K_UP:
#            ship.moving_up == True
#        elif event.key == pygame.K_DOWN:
#            ship.moving_down == True
        elif event.key == pygame.K_SPACE:
            fire_bullet(ai_settings, screen, ship, bullets)
        elif event.key == pygame.K_q:
            sys.exit()
        """elif event.key == pygame.K_p:
            #reset game settings
            ai_settings.initialize_dynamic_settings()
            #make the mouse invisible
            pygame.mouse.set_visible(False)
            #reset game stats
            stats.reset_stats()
            stats.game_active = True

            #empty the list of aliens and bullets
            aliens.empty()
            bullets.empty()

            #create a new fleet and center the ship
            create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()"""

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:#check the num of bullets on screen and keep it in allowed range
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            ship.moving_left = False
#        elif event.key == pygame.K_UP:
#                ship.moving_up == False
#        elif event.key == pygame.K_DOWN:
#                ship.moving_down == False

def check_high_score(stats, sb):
    """check to see if there's a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    #respond to kepyresses and mouse click

    for event in pygame.event.get():  #respond to events
        if event.type == pygame.QUIT:   #if player hit's 'x' it will close window
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

        elif event.type == pygame.KEYDOWN:   #if a key is pressed down, check keydown events
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:  #if a key is released, check keyup events
            check_keyup_events(event, ship)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    #update images and flip to new screen
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    #handle bullets
    bullets.update()
    #get rid of off-screen bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <=0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)#check for collisions
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()

        #increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    if len(aliens) == 0:
        ai_settings.fleet_drop_speed += 2
