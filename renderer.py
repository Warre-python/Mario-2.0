import pygame

class Renderer:
    def __init__(self, window):
        self.window = window

    def render(self, world, camera):
        self.window.fill((135, 206, 235))  # sky blue

        for tile in world.tiles:
            pygame.draw.rect(self.window, (150, 75, 0), camera.apply(tile.rect))

        for entity in world.entities:
            pygame.draw.rect(self.window, (255, 0, 0), camera.apply(entity.rect))
