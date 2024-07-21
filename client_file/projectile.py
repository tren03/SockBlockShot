import pygame

class Projectile(object):
    def __init__(self, x, y, radius, color, damage=10):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.vel = 8
        self.damage = damage  # Add damage attribute

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
