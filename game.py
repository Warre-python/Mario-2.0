import pygame
from world import World
from camera import Camera
from renderer import Renderer

class Game:
    def __init__(self, window, clock, pixel, fps, debug):
        self.pixel = pixel
        self.fps = fps
        self.debug = debug

        self.window = window
        self.clock = clock

        self.running = True
        self.world = World(self.pixel)
        self.camera = Camera(0, 0, self.window.width, self.window.height)
        self.renderer = Renderer(self.window)

    def run(self):
        while self.running:
            dt = self.clock.tick(self.fps) / 1000
            self.handle_events()
            self.update(dt)
            self.render()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.world.update(keys, dt)
        self.camera.follow(self.world.player)

    def render(self):
        self.renderer.render(self.world, self.camera)
        pygame.display.flip()
