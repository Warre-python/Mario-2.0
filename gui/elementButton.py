import pygame

class ElementButton(pygame.sprite.Sprite):
    def __init__(self, x, y, size, pixel, name, image, data):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.pixel = pixel

        self.name = name
        self.image = image
        self.data = data
    
    def isPressed(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return self.name
        return 0
    
    def draw(self, window):
        
        self.tile_x = self.data[self.name][0]["x"]
        self.tile_y = self.data[self.name][1]["y"]
        self.tile_width = self.data[self.name][2]["w"]
        self.tile_height = self.data[self.name][3]["h"]
        self.sprite = self.image.subsurface(self.tile_x, self.tile_y, self.tile_width, self.tile_height)
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))
        window.blit(self.sprite, self.rect)
        