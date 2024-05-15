import pygame

width = 1000
height = 1000

health_bar_height = 5

class Player1():
    def __init__(self, x, y, width, height, color):
        self.name = "player1"
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 10
        self.health = 100
        self.bullets = []
        self.can_shoot = True
        self.shoot_timer = 0
        self.shoot_delay = 90
        self.win_state = False

    def draw(self, win):
        pygame.draw.rect(win, 'red', (0, 0, width, health_bar_height))
        # Calculate the width of the green health bar based on the player's health
        health_bar_width = (self.health / 100) * width
        pygame.draw.rect(win, 'green', (0,0, health_bar_width, health_bar_height))
        pygame.draw.rect(win, self.color, self.rect)

        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.x > 0:
                self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            if self.x + self.width < width:
                self.x += self.vel

        if keys[pygame.K_UP]:
            if self.y - health_bar_height -5 > 0:
                self.y -= self.vel

        if keys[pygame.K_DOWN]:
            if self.y + self.height < height / 2:
                self.y += self.vel


        

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)