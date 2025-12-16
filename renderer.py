import pygame

class Renderer:
    def __init__(self, window):
        self.window = window

    def render(self, world, gui, dt, camera):
        self.window.fill((135, 206, 235))  # sky blue

        for tile in world.tiles:
            tile.draw(camera, self.window)

        for entity in world.entities:
            entity.draw(camera, dt, self.window)

        for element in gui:
            element.draw(self.window)
        
        world.player.draw(camera, dt, self.window)

        pygame.draw.line(self.window, (255, 0, 0), (0, world.death_y - camera.y), (self.window.get_width(), world.death_y - camera.y))
