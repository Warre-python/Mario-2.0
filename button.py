import pygame

class Button():
    def __init__(self, x, y, size, width, heigth, colorBox, colorText, text, font):
        self.colorBox = colorBox
        self.colorText = colorText
        self.x = x
        self.y = y
        self.width = width
        self.heigth = heigth
        self.font  = pygame.font.SysFont(font, size)
        self.text = self.font.render(text, True, self.colorText)
        self.text_surface = self.font.render(text, True, self.colorText)
        self.button = pygame.Rect(self.x, self.y, self.width, self.heigth)

    def setText(self, text, color):
        self.color = color
        self.text = self.font.render(text, True, self.color)
        self.textRect = self.text.get_rect()

    def setPos(self, x, y):
        self.x = x
        self.y = y
        self.textRect = self.text.get_rect()

    def isPressed(self):
        pos = pygame.mouse.get_pos()
        self.button = pygame.Rect(self.x, self.y, self.width, self.heigth)  # <-- update every frame
        if self.button.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True
        return False
    
    def draw(self, window):
        pygame.draw.rect(window, self.colorBox, self.button)
        window.blit(self.text_surface, self.button)
        