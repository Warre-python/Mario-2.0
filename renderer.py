import pygame

class Renderer:
    def __init__(self):
        pass

    def render(self, world, gui, dt, camera, scene, window):
        window.fill((135, 206, 235))  # sky blue

        for tile in world.tiles:
            tile.draw(camera, window)

        for entity in world.entities:
            entity.draw(camera, dt, window)

        for element in gui:
            element.draw(window)
        
        world.player.draw(camera, dt, window)

        pygame.draw.line(window, (255, 0, 0), (0, world.death_y - camera.y), (window.get_width(), world.death_y - camera.y))