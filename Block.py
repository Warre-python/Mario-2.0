import pygame
import json
from Vector import Vector
from Collisionbox import CollisionBox

class Block:
    def __init__(self, x, y, width, height, block):
        self.pos = Vector(x, y)
        self.dim = Vector(width, height)
        self.rect = pygame.Rect(self.pos.getX(), self.pos.getY(), self.dim.getX(), self.dim.getY())

        self.block = block

    
    def draw(self, window, block_data, block_tileset, pixel_size):
        self.tile_x = block_data[self.block][0]["x"]
        self.tile_y = block_data[self.block][1]["y"]
        self.sprite = block_tileset.subsurface(self.tile_x, self.tile_y, 16, 16)
        self.sprite = pygame.transform.scale(self.sprite, (16 * pixel_size, 16 * pixel_size))
        window.blit(self.sprite, self.pos.get())