import pygame

class Renderer:
    def __init__(self, window):
        self.window = window

    def render(self, world, dt, camera):
        self.window.fill((135, 206, 235))  # sky blue

        for tile in world.tiles:
            tile.draw(camera, self.window)

        for entity in world.entities:
            entity.draw(camera, dt, self.window)
