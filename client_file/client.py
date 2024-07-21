import pygame
import atexit
from network import Network
from projectile import Projectile

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
pygame.font.init()
font = pygame.font.Font(None, 36)

def display_popup(message):
    popup_text = font.render(message, True, (255, 255, 255))
    popup_rect = popup_text.get_rect(center=(width // 2, height // 2))
    
    # Draw background for the popup
    pygame.draw.rect(win, (0, 0, 0), (popup_rect.x - 10, popup_rect.y - 10, popup_rect.width + 20, popup_rect.height + 20))
    
    # Draw the popup text
    win.blit(popup_text, popup_rect)
    
    pygame.display.update()

def draw_large_bullet_indicator(win, ready, player1):
    if player1.color == 'red':
        indicator_color = (0, 255, 0) if ready else (255, 0, 0)
        pygame.draw.circle(win, indicator_color, (width - 30, 30), 7)
        pygame.draw.circle(win, (0, 0, 0), (width - 30, 30), 7, 2)  # Border for the indicator
    else:
        indicator_color = (0, 255, 0) if ready else (255, 0, 0)
        pygame.draw.circle(win, indicator_color, (30, height - 30), 7)
        pygame.draw.circle(win, (0, 0, 0), (30, height - 30), 7, 2)  # Border for the indicator

def redrawWindow(win, player1, player2, ready_for_large_bullet):
    win.fill((255, 255, 255))
    pygame.draw.line(win, (255, 0, 0), (0, height / 2), (width, height / 2), width=2)
    player1.draw(win)
    player2.draw(win)
    
    for bullet in player1.bullets:
        bullet.draw(win)

    for bullet in player2.bullets:
        bullet.draw(win)

    draw_large_bullet_indicator(win, ready_for_large_bullet, player1)
    pygame.display.update()

def cleanup():
    pygame.quit()
    if n:
        n.close()

atexit.register(cleanup)

def main():
    run = True
    global n  # Make the Network instance global so it can be accessed in cleanup
    n = Network()
    p1 = n.getP()
    w = None

    clock = pygame.time.Clock()

    shooting_interval = 500  # Interval between bullets in milliseconds
    large_bullet_interval = 5000  # Interval for large bullets in milliseconds
    last_bullet_time = pygame.time.get_ticks()  # Time when the last bullet was shot
    last_large_bullet_time = pygame.time.get_ticks()  # Time when the last large bullet was shot
    key_press_start = None  # To track when space key was first pressed

    while run:
        clock.tick(60)
        p2 = n.send(p1)

        if p2 is None:  # Check if connection was lost
            print("Connection lost")
            break

        print(f'opp_health : {p1.opp_health}')

        current_time = pygame.time.get_ticks()

        # Check if it's time to allow shooting a large bullet
        can_shoot_large_bullet = current_time - last_large_bullet_time >= large_bullet_interval

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and p1.can_shoot:
                    if key_press_start is None:
                        key_press_start = pygame.time.get_ticks()  # Record the start time of space key press
                    print("Space pressed")
                
                if event.key == pygame.K_k:  # Check for K key press
                    if can_shoot_large_bullet:
                        p1.bullets.append(Projectile(round(p1.x + p1.width // 2), round(p1.y + p1.height // 2), 12, (255, 0, 0), damage=30))  # Large bullet
                        last_large_bullet_time = current_time

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if key_press_start is not None:
                        key_press_end = pygame.time.get_ticks()  # Record the end time of space key release
                        time_held = key_press_end - key_press_start  # Calculate the duration of the key press
                        print(time_held)
                        key_press_start = None  # Reset the key press start time

                        bullet_count = max(1, int(time_held / 1000))  # Calculate number of bullets to fire
                        for _ in range(bullet_count):
                            if current_time - last_bullet_time >= shooting_interval:
                                p1.bullets.append(Projectile(round(p1.x + p1.width // 2), round(p1.y + p1.height // 2), 6, (0, 0, 0)))  # Normal bullet
                                last_bullet_time = current_time

        # Update bullet positions and check for collisions
        for bullet in p1.bullets:
            if bullet.y < height and bullet.y > 0:
                bullet.y += bullet.vel if p1.name == "player1" else -bullet.vel
            else:
                p1.bullets.remove(bullet)

        for bullet in p1.bullets:
            bullet_rect = pygame.Rect(bullet.x - bullet.radius, bullet.y - bullet.radius, bullet.radius * 2, bullet.radius * 2)
            p2_rect = pygame.Rect(p2.x, p2.y, p2.width, p2.height)
            if p2_rect.colliderect(bullet_rect):
                p1.bullets.remove(bullet)
                p1.opp_health -= bullet.damage  # Reduce health by the bullet's damage
                if p1.opp_health <= 0:
                    p1.opp_health = 0
                    p1.opp_win_state = False

        keys = pygame.key.get_pressed()

        if p1.opp_win_state == False:
            w = p1
        elif p2.opp_win_state == False:
            w = p2
        else:
            w = None

        if w:  
            display_popup(f"{w.color} won the game \n Press q to quit")
         
            if keys[pygame.K_q]:
                pygame.quit()
        else:
            p1.move()
            redrawWindow(win, p1, p2, can_shoot_large_bullet)

main()
