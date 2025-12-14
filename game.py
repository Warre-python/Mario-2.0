import pygame
from world import World
from camera import Camera
from renderer import Renderer
from gui.textBox import TextBox

class Game:
    def __init__(self, window, clock, pixel, fps, debug):
        self.pixel = pixel
        self.fps = fps
        self.debug = debug

        self.window = window
        self.clock = clock

        self.running = True
        self.world = World(self.pixel, self.debug)
        self.camera = Camera(0, 0, self.window.width, self.window.height)
        self.renderer = Renderer(self.window)
        
        self.fpsText = TextBox("Fps: ", (255, 255, 255), 'Arial', 20, 10, 10)

    def run(self):
        while self.running:
            dt = self.clock.tick(self.fps) / 1000
            if dt == 0: continue
            self.handle_events()
            self.update(dt)
            self.render(dt)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
    def update(self, dt):
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        self.world.update(keys, mouse_buttons, mouse_pos, self.camera, dt)
        self.camera.follow(self.world.player)

    def render(self, dt):
        self.renderer.render(self.world, self.camera)
        self.fpsText.setText("Fps: " + str(int(1/dt)), (255, 255, 255))
        self.fpsText.draw(self.window)
        pygame.display.flip()
