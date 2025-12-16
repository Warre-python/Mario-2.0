import pygame

class InputText(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, bColor, tColor, font, size, borderColor):
        super().__init__()
        self.bColor = bColor
        self.tColor = tColor
        self.borderColor = borderColor
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect = pygame.Rect(x, y, width, height)

        self.font  = pygame.font.SysFont(font, size)
        self.text = ""
        self.txt_surface = self.font.render(self.text, True, self.tColor)
        self.image = self.txt_surface # Add this line
        self.active = False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    # self.text = "" # Keep text after pressing enter
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.tColor)
                self.image = self.txt_surface # Add this line
    
    def draw(self, window):
        # Draw the background of the input box
        pygame.draw.rect(window, self.bColor, self.rect)
        # Blit the text.
        window.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(window, self.borderColor, self.rect, 2)
        
        
