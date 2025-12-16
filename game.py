import pygame
import json
from world import World
from renderer import Renderer
from gui.textBox import TextBox
from gui.elementButton import ElementButton

class Game:
    def __init__(self, window, clock, pixel, fps, debug):
        self.pixel = pixel
        self.fps = fps
        self.debug = debug

        self.window = window
        self.clock = clock

        self.running = True
        self.world = World("levels\level5.json",self.pixel, self.debug)
        self.camera = self.world.loadWorld(self.window)
        
        self.renderer = Renderer(self.window)
        
        self.gui = pygame.sprite.Group()

        with open('assets/blocks.json') as m: 
            self.blocks_data = json.load(m)
        self.blocks_tileset = pygame.image.load("assets/images/background tiles1.png").convert_alpha()

        with open('assets/coin.json') as m: 
            self.coins_data = json.load(m)
        self.coins_tileset = pygame.image.load("assets/images/coin.png").convert_alpha()

        for i in range(len(self.blocks_data)):
            tile = list(self.blocks_data.keys())[i]
            element_button = ElementButton(20 + i * 100, 100, 50, self.pixel, tile, self.blocks_tileset, self.blocks_data)
            self.gui.add(element_button)

        element_button = ElementButton(20 + len(self.blocks_data)* 100 + 100, 100, 50, self.pixel, "coin", self.coins_tileset, self.coins_data)
        
        self.gui.add(element_button)

        self.fpsText = TextBox("Fps: ", (255, 255, 255), 'Arial', 20, 10, 10)
        self.gui.add(self.fpsText)

        self.selected_element = "grass"

        self.coinsVar = TextBox("Coins: ", (255, 255, 255), 'Arial', 50, 10, 40)
        self.gui.add(self.coinsVar)

        self.money = 0
        

    def run(self):
        while self.running:
            dt = self.clock.tick(self.fps) / 1000
            if dt == 0: continue
            self.handle_events()
            self.update(dt)
            self.render(dt)
        self.world.saveWorld(self.camera)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked_on_gui = False
                    for element in self.gui:
                        if isinstance(element, ElementButton) and element.isPressed(event.pos):
                            self.selected_element = element.name
                            clicked_on_gui = True
                            break
                    if not clicked_on_gui:
                        self.world.handle_element_placement(event.pos, self.camera, self.selected_element)
            
    def update(self, dt):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        coins_collected = self.world.update(keys, mouse_pos, self.camera, self.window, dt)
        if coins_collected > 0:
            self.money += coins_collected
            self.coinsVar.setText("Coins: " + str(self.money), (255, 255, 255))

        self.camera.follow(self.world.player)

        self.fpsText.setText("Fps: " + str(int(1/dt)), (255, 255, 255))


        
            

    def render(self, dt):
        self.renderer.render(self.world, self.gui, dt, self.camera)
        
        
        pygame.display.flip()
