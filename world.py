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

    def handle_element_placement(self, mouse_pos, camera, selected_element):
        if mouse_pos[1] > 60:
            # Convert screen coordinates to world coordinates and snap to grid
            grid_x = (mouse_pos[0] + camera.x) // self.pixel * self.pixel
            grid_y = (mouse_pos[1] + camera.y) // self.pixel * self.pixel
            
            # Check for existing blocks at this position and remove them
            for block in self.tiles:
                if block.rect.collidepoint(grid_x, grid_y):
                    block.kill()
                    break
            
            # Check for existing entities at this position and remove them
            for entity in self.entities:
                if entity.rect.collidepoint(grid_x, grid_y):
                    entity.kill()
                    break
            
            if selected_element == "coin":
                self.entities.add(Coin(grid_x, grid_y, self.pixel, self.debug))
            else:
                self.tiles.add(Block(grid_x, grid_y, selected_element, self.pixel, self.debug))

    def update(self, keys, mouse_pos, camera, dt):
        self.player.update(keys, self.tiles, camera, dt)
        for entity in self.entities:
            entity.update(dt, self.player_group, self.entities)

        # Remove element with right click
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[2]:
            grid_x = (mouse_pos[0] + camera.x) // self.pixel * self.pixel
            grid_y = (mouse_pos[1] + camera.y) // self.pixel * self.pixel
            for block in self.tiles:
                if block.rect.collidepoint(grid_x, grid_y):
                    block.kill()
                    break
            for entity in self.entities:
                if entity.rect.collidepoint(grid_x, grid_y):
                    entity.kill()
                    break
            
    