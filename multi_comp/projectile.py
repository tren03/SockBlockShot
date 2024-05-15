import pygame
class Projectile(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.vel = 8

    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)
