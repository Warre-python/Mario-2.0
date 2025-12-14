import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, pixel):
        super().__init__()
        self.rect = pygame.Rect(x, y, pixel, pixel)
        self.image = self.rect
    def update():
        pass
    def draw(self, camera, dt, window):
        pygame.draw.rect(window, (255, 255, 0), camera.apply(self.rect))