import pygame

width = 1000
height = 1000

health_bar_height = 5

class Player2():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.vel = 10
        self.health = 100

    def draw(self, win):
        pygame.draw.rect(win, 'red', (0, height-health_bar_height, width, health_bar_height))
        # Calculate the width of the green health bar based on the player's health
        health_bar_width = (self.health / 100) * width
        pygame.draw.rect(win, 'green', (0, height-health_bar_height, health_bar_width, health_bar_height))
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and self.x > 0:
            self.x -= self.vel

        if keys[pygame.K_d] and self.x + self.width < width:
            self.x += self.vel

        if keys[pygame.K_w] and self.y > height // 2:
            self.y -= self.vel

        if keys[pygame.K_s] and self.y + self.height+ health_bar_height+5 < height:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
