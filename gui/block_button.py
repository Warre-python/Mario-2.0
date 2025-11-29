import pygame

class BlockButton:
    def __init__(self, x, y, width, height, tile):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tile = tile
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.is_pressed = False
    
    def isPressed(self):
        pos = pygame.mouse.get_pos()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  # <-- update every frame
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.is_pressed = True
                return True
        self.is_pressed = False
        return False
    
    
    def draw(self, window, block_data, block_tileset, pixel_size):
        

        self.rect.topleft = (self.rect.x, self.rect.y)
        
        self.tile_x = block_data[self.tile][0]["x"]
        self.tile_y = block_data[self.tile][1]["y"]
        self.tile_width = block_data[self.tile][2]["w"]
        self.tile_height = block_data[self.tile][3]["h"]
        self.sprite = block_tileset.subsurface(self.tile_x, self.tile_y, self.tile_width, self.tile_height)
        self.sprite = pygame.transform.scale(self.sprite, (self.tile_width * pixel_size, self.tile_height* pixel_size))
        window.blit(self.sprite, (self.rect.x, self.rect.y))