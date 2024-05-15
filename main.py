import pygame
from player1 import Player1
from projectile import Projectile
from player2 import Player2

pygame.font.init()

width = 1000
height = 1000
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
font = pygame.font.Font(None, 36)

clientNumber = 0

def redrawWindow(win,player1,player2,bullets1,bullets2):
    win.fill((255,255,255))
    pygame.draw.line(win, (255, 0, 0), (0, height/2), (width, height/2), width=2)
    player1.draw(win)
    player2.draw(win)
    for bullet in bullets1:
        bullet.draw(win)

    for bullet in bullets2:
        bullet.draw(win)
    pygame.display.update()


def display_popup(message):
    popup_text = font.render(message, True, (255, 255, 255))
    popup_rect = popup_text.get_rect(center=(width // 2, height // 2))
    
    # Draw background for the popup
    pygame.draw.rect(win, (0, 0, 0), (popup_rect.x - 10, popup_rect.y - 10, popup_rect.width + 20, popup_rect.height + 20))
    
    # Draw the popup text
    win.blit(popup_text, popup_rect)
    
    pygame.display.update()





def main():
    run = True
    bullets1 = []
    bullets2 = []
    clock = pygame.time.Clock()
    p1 = Player1(10, 10, 50, 50, 'red')
    p2 = Player2(0,height-100,50,50,'blue')
    can_shoot1 = True
    can_shoot2 = True
    shoot_delay = 90 # Adjust this value to control the firing rate (in milliseconds)
    shoot_timer1 = 0
    shoot_timer2 = 0
    state = 1

    while run:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        

        for bullet in bullets1:     
            if bullet.y < height and bullet.y > 0:
                bullet.y += bullet.vel
            else:
                bullets1.remove(bullet)

        for bullet in bullets2:     
            if bullet.y < height and bullet.y > 0:
                bullet.y -= bullet.vel
            else:
                bullets2.remove(bullet)

       
        for bullet in bullets1:
            # Create a bounding rectangle for the circle projectile
            bullet_rect = pygame.Rect(bullet.x - bullet.radius, bullet.y - bullet.radius, bullet.radius * 2, bullet.radius * 2)
            
            p2_rect = pygame.Rect(p2.x,p2.y,p2.width,p2.height)
            if p2_rect.colliderect(bullet_rect):
                bullets1.remove(bullet)
                if(p2.health < 0):   
                    state = 0
                    w = "p1"                
                    
                else:
                    p2.health -= 10

      
        for bullet in bullets2:
            # Create a bounding rectangle for the circle projectile
            bullet_rect = pygame.Rect(bullet.x - bullet.radius, bullet.y - bullet.radius, bullet.radius * 2, bullet.radius * 2)
            
            p1_rect = pygame.Rect(p1.x,p1.y,p1.width,p1.height)
            if p1_rect.colliderect(bullet_rect):
                bullets2.remove(bullet)
                if(p1.health < 0):
                    state = 0
                    w = "p2"
                else:
                    p1.health -= 10
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and can_shoot1:  
            bullets1.append(Projectile(round(p1.x + p1.width // 2), round(p1.y + p1.height // 2), 6, (0, 0, 0)))             
            can_shoot1 = False
            shoot_timer1 = pygame.time.get_ticks()

        if keys[pygame.K_v] and can_shoot2:  
            bullets2.append(Projectile(round(p2.x + p2.width // 2), round(p2.y + p2.height // 2), 6, (0, 0, 0)))             
            can_shoot2 = False
            shoot_timer2 = pygame.time.get_ticks()

        if not can_shoot1 and pygame.time.get_ticks() - shoot_timer1 >= shoot_delay:
            can_shoot1 = True

        if not can_shoot2 and pygame.time.get_ticks() - shoot_timer2 >= shoot_delay:
            can_shoot2 = True


        if(state == 0):
            display_popup(f"{w} won the game \n Press q to quit or r to restart")
         
            if keys[pygame.K_q]:
                
                pygame.quit()
            if keys[pygame.K_r]:
                p1 = Player1(10, 10, 50, 50, 'red')
                p2 = Player2(0,height-100,50,50,'blue')
                bullets1.clear()
                bullets2.clear()
                state = 1
                
        else:
            p1.move()
            p2.move()
            redrawWindow(win, p1,p2, bullets1,bullets2)

       


        

main()


