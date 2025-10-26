import pygame

class TextBox:
    def __init__(self, text, color, font, size, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.font  = pygame.font.SysFont(font, size)
        self.text = self.font.render(text, True, self.color)
        self.textRect = self.text.get_rect()

    def setText(self, text, color):
        self.color = color
        self.text = self.font.render(text, True, self.color)
        self.textRect = self.text.get_rect()

    def setPos(self, x, y):
        self.x = x
        self.y = y
        self.textRect = self.text.get_rect()

    def draw(self, window):
        window.blit(self.text, self.textRect)