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

def redrawWindow(win, player1, player2):
    win.fill((255,255,255))
    pygame.draw.line(win, (255, 0, 0), (0, height/2), (width, height/2), width=2)
    player1.draw(win)
    player2.draw(win)
    
    for bullet in player1.bullets:
        bullet.draw(win)

    for bullet in player2.bullets:
        bullet.draw(win)
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

    while run:
        clock.tick(60)
        p2 = n.send(p1)

        if p2 is None:  # Check if connection was lost
            print("Connection lost")
            break

        print(f'opp_health : {p1.opp_health}')
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()          

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and p1.can_shoot:
                # Space key is pressed
                s = pygame.time.get_ticks()  # Record the start time
                print("Space pressed")
                    
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                # Space key is released
                e = pygame.time.get_ticks()  # Record the end time
                time_held = e - s  # Calculate the duration of the key press
                print(time_held)
                    
                if time_held < 1000:  # Short press
                    # Do something for short press
                    
                    p1.bullets.append(Projectile(round(p1.x + p1.width // 2), round(p1.y + p1.height // 2), 6, (0, 0, 0)))             
                    p1.can_shoot = False
                    p1.shoot_timer = pygame.time.get_ticks()
                        
                elif time_held > 1000:
                    p1.bullets.append(Projectile(round(p1.x + p1.width // 2), round(p1.y + p1.height // 2), 20, (0, 0, 0))) 

                if not p1.can_shoot and pygame.time.get_ticks() - p1.shoot_timer >= p1.shoot_delay:
                    p1.can_shoot = True

        if p1.name == "player1":
            for bullet in p1.bullets:     
                if bullet.y < height and bullet.y > 0:
                    bullet.y += bullet.vel
                else:
                    p1.bullets.remove(bullet)

        if p1.name == "player2":
            for bullet in p1.bullets:     
                if bullet.y < height and bullet.y > 0:
                    bullet.y -= bullet.vel
                else:
                    p1.bullets.remove(bullet)

        for bullet in p1.bullets:
            # Create a bounding rectangle for the circle projectile
            bullet_rect = pygame.Rect(bullet.x - bullet.radius, bullet.y - bullet.radius, bullet.radius * 2, bullet.radius * 2)
            p2_rect = pygame.Rect(p2.x, p2.y, p2.width, p2.height)
            if p2_rect.colliderect(bullet_rect):
                p1.bullets.remove(bullet)
                if p1.opp_health < 0:
                    state = 0
                    p1.opp_win_state = False
                else:
                    if bullet.radius == 20:
                        p1.opp_health -= 20
                    else:                        
                        p1.opp_health -= 10

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
            redrawWindow(win, p1, p2)

main()
