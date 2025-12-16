import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, tile, pixel, blocks_data, block_tileset, debug):
        super().__init__()
        
        self.image = self.rect

        self.tile = tile

        self.pixel = pixel


        self.blocks_data = blocks_data
        self.block_tileset = block_tileset

        self.tile_x = self.blocks_data[self.tile][0]["x"]
        self.tile_y = self.blocks_data[self.tile][1]["y"]
        self.tile_width = self.blocks_data[self.tile][2]["w"]
        self.tile_height = self.blocks_data[self.tile][3]["h"]

        self.rect = pygame.Rect(x, y, self.tile_width * self.pixel/16, self.tile_height * self.pixel/16)

        self.debug = debug
    
    def draw(self, camera, window):
        if self.debug:
            pygame.draw.rect(window, (0, 255, 0), camera.apply(self.rect), 5)

        self.rect.topleft = (self.rect.x, self.rect.y)
        
        self.tile_x = self.blocks_data[self.tile][0]["x"]
        self.tile_y = self.blocks_data[self.tile][1]["y"]
        self.tile_width = self.blocks_data[self.tile][2]["w"]
        self.tile_height = self.blocks_data[self.tile][3]["h"]
        self.sprite = self.block_tileset.subsurface(self.tile_x, self.tile_y, self.tile_width, self.tile_height)
        self.sprite = pygame.transform.scale(self.sprite, (self.tile_width * self.pixel/16, self.tile_height * self.pixel/16))
        window.blit(self.sprite, camera.apply(self.rect))