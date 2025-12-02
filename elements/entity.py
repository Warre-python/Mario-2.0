import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (255, 0, 255)
    
    def collision(self, other):
        return pygame.sprite.spritecollide(self, other, False, False)
    
    def scrollScreen(self, offsetX):
        # move both the rect and the stored x position so the entity
        # stays in sync with world shifts performed by Mario.moveX
        self.rect.x += offsetX
        self.x += round(offsetX)

    def update(self, dt):
        pass

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        