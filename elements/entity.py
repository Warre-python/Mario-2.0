import pygame
from elements.element import Element

class Entity(Element):
    def __init__(self, x, y, width, height, can_collide, debug):
        super().__init__(x, y, width, height, can_collide, debug)
        
        self.color = (255, 0, 255)
    
    def collision(self, other):
        return pygame.sprite.spritecollide(self, other, False, False)
    

    def update(self, dt):
        pass

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        