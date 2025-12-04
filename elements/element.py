import pygame

class Element(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, debug):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.debug = debug

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.x, self.y = self.rect.topleft

    def update(self, dt, mario, mario_group):
        pass

    def draw(self, window):
        if self.debug:
            pygame.draw.rect(window, (0, 255, 0), self.rect, 5)
