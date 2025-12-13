import pygame
from elements.player import Player
from elements.block import Block

class World:
    def __init__(self, pixel):
        self.pixel = pixel

        self.tiles = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()

        self.player = Player(64, 128, pixel)
        self.entities.add(self.player)

        # Example blocks
        for i in range(20):
            self.tiles.add(Block(i * pixel, pixel*10, pixel))

    def update(self, keys, dt):
        for entity in self.entities:
            entity.update(keys, dt)
