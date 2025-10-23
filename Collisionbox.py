from Vector import Vector
import pygame

class CollisionBox:
    def __init__(self, pos, dim):
        self.pos = pos  # Vector(x, y)
        self.dim = dim  # Vector(width, height)

        self.rect = pygame.Rect(self.pos.getX(), self.pos.getY(), self.dim.getX(), self.dim.getY())
    
    



