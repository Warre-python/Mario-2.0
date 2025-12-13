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

        self.left_pressed = False
        self.right_pressed = False

        # Level layout
        # Ground
        for i in range(10):
            self.tiles.add(Block(i * pixel, pixel * 10, pixel))
        
        # Some platforms
        self.tiles.add(Block(pixel * 3, pixel * 8, pixel))
        self.tiles.add(Block(pixel * 4, pixel * 8, pixel))
        self.tiles.add(Block(pixel * 6, pixel * 6, pixel))
        self.tiles.add(Block(pixel * 7, pixel * 6, pixel))
        self.tiles.add(Block(pixel * 8, pixel * 6, pixel))
        self.tiles.add(Block(pixel * 11, pixel * 4, pixel))
        self.tiles.add(Block(pixel * 12, pixel * 4, pixel))

    def update(self, keys, mouse_buttons, mouse_pos, camera, dt):
        self.player.update(keys, self.tiles, camera, dt)

        # Add block with left click
        if mouse_buttons[0] and not self.left_pressed:
            self.left_pressed = True
            # Convert screen coordinates to world coordinates and snap to grid
            grid_x = (mouse_pos[0] + camera.x) // self.pixel * self.pixel
            grid_y = (mouse_pos[1] + camera.y) // self.pixel * self.pixel
            self.tiles.add(Block(grid_x, grid_y, self.pixel))
        
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
            
    