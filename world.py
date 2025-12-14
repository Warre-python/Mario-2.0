import pygame
from elements.player import Player
from elements.block import Block
from elements.entity import Entity
from elements.entities.coin import Coin

class World:
    def __init__(self, pixel, debug):
        self.pixel = pixel
        self.debug = debug
        self.tiles = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()

        self.player = Player(64, 128, pixel, self.debug)
        self.player_group.add(self.player)
        

        self.left_pressed = False
        self.right_pressed = False

        # Level layout
        # Ground
        for i in range(10):
            self.tiles.add(Block(i * pixel, pixel * 10, "grass", pixel, debug))
        
        # Some platforms
        self.tiles.add(Block(pixel * 3, pixel * 8, "luckyblock",  pixel, debug))
        self.tiles.add(Block(pixel * 4, pixel * 8, "pijp_boven", pixel, debug))
        self.tiles.add(Block(pixel * 6, pixel * 6, "luckyblock", pixel, debug))
        self.tiles.add(Block(pixel * 7, pixel * 6, "luckyblock", pixel, debug))
        self.tiles.add(Block(pixel * 8, pixel * 6, "brug", pixel, debug))
        self.tiles.add(Block(pixel * 11, pixel * 4, "luckyblock", pixel, debug))
        self.tiles.add(Block(pixel * 12, pixel * 4, "luckyblock", pixel, debug))

        self.entities.add(Coin(pixel * 2, pixel * 7, pixel, debug))

    def update(self, keys, mouse_buttons, mouse_pos, camera, dt):
        self.player.update(keys, self.tiles, camera, dt)
        for entity in self.entities:
            entity.update(dt, self.player_group, self.entities)

        # Add block with left click
        if mouse_buttons[0] and not self.left_pressed:
            self.left_pressed = True
            # Convert screen coordinates to world coordinates and snap to grid
            grid_x = (mouse_pos[0] + camera.x) // self.pixel * self.pixel
            grid_y = (mouse_pos[1] + camera.y) // self.pixel * self.pixel
            self.tiles.add(Block(grid_x, grid_y, "grass", self.pixel, self.debug))
        
        if not mouse_buttons[0]:
            self.left_pressed = False
        
        # Remove block with right click
        if mouse_buttons[2] and not self.right_pressed:
            self.right_pressed = True
            grid_x = (mouse_pos[0] + camera.x) // self.pixel * self.pixel
            grid_y = (mouse_pos[1] + camera.y) // self.pixel * self.pixel
            for block in self.tiles:
                if block.rect.collidepoint(grid_x, grid_y):
                    block.kill()
                    break
        
        if not mouse_buttons[2]:
            self.right_pressed = False
            
    