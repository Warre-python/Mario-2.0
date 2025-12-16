import pygame

class TextBox(pygame.sprite.Sprite):
    def __init__(self, text, color, font, size, x, y):
        super().__init__()
        self.color = color
        self.x = x
        self.y = y
        self.font  = pygame.font.SysFont(font, size)
        
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def setText(self, text, color):
        self.color = color
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def setPos(self, x, y):
        self.x = x
        self.y = y
        # Update rect position based on new x, y. The rect size should remain the same.
        self.rect.topleft = (self.x, self.y)
    def draw(self, window):
        window.blit(self.image, self.rect)