import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, tile, debug):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.tile = tile

        self.debug = debug
    
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.x, self.y = self.rect.topleft

    def draw(self, window, block_data, block_tileset, pixel_size):
        if self.debug:
            pygame.draw.rect(window, (0, 255, 0), self.rect, 5)

        self.rect.topleft = (self.rect.x, self.rect.y)
        
        self.tile_x = block_data[self.tile][0]["x"]
        self.tile_y = block_data[self.tile][1]["y"]
        self.tile_width = block_data[self.tile][2]["w"]
        self.tile_height = block_data[self.tile][3]["h"]
        self.sprite = block_tileset.subsurface(self.tile_x, self.tile_y, self.tile_width, self.tile_height)
        self.sprite = pygame.transform.scale(self.sprite, (self.tile_width * pixel_size, self.tile_height* pixel_size))
        window.blit(self.sprite, (self.rect.x, self.rect.y))