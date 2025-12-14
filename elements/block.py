import pygame
import json

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, tile, pixel, debug):
        super().__init__()
        self.rect = pygame.Rect(x, y, pixel, pixel)
        self.image = self.rect

        self.tile = tile

        self.pixel = pixel

        with open('assets/blocks.json') as b:
            self.blocks_data = json.load(b)
        self.block_tileset = pygame.image.load("assets/images/background tiles1.png").convert_alpha()

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
        self.sprite = pygame.transform.scale(self.sprite, (self.pixel, self.pixel))
        window.blit(self.sprite, camera.apply(self.rect))