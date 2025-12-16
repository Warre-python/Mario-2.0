import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, callback):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.text = text
        self.callback = callback
        self.font = pygame.font.Font(None, 36)
        self.hovered = False
        self.render()

    def render(self):
        self.image.fill((200, 200, 200) if not self.hovered else (170, 170, 170))
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.image.get_rect().center)
        self.image.blit(text_surf, text_rect)

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            if not self.hovered:
                self.hovered = True
                self.render()
        else:
            if self.hovered:
                self.hovered = False
                self.render()