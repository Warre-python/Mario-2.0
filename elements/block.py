import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, pixel):
        super().__init__()
        self.rect = pygame.Rect(x, y, pixel, pixel)
        self.image = self.rect