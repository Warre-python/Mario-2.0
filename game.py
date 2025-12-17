import pygame
import json
import os
from world import World
from renderer import Renderer
from gui.textBox import TextBox
from gui.elementButton import ElementButton
from gui.menu import Menu
from gui.inGameMenu import inGameMenu

class Game:
    def __init__(self, window, clock, pixel, fps, debug):
        self.pixel_size = pixel
        self.fps = fps
        self.debug = debug

        self.window = window
        self.clock = clock

        self.level_name = None
        self.pathToWorld = None

        self.scene = "menu"

        self.running = True
        self.world = None
        self.camera = None
        
        self.renderer = Renderer()
        
        self.gui = pygame.sprite.Group()

        with open('assets/blocks.json') as m: 
            self.blocks_data = json.load(m)
        self.blocks_tileset = pygame.image.load("assets/images/background tiles1.png").convert_alpha()

        with open('assets/coin.json') as m: 
            self.coins_data = json.load(m)
        self.coins_tileset = pygame.image.load("assets/images/coin.png").convert_alpha()

        for i in range(len(self.blocks_data)):
            tile = list(self.blocks_data.keys())[i]
            element_button = ElementButton(20 + i * 100, 100, 50, self.pixel_size, tile, self.blocks_tileset, self.blocks_data)
            self.gui.add(element_button)

        element_button = ElementButton(20 + len(self.blocks_data)* 100 + 100, 100, 50, self.pixel_size, "coin", self.coins_tileset, self.coins_data)
        
        self.gui.add(element_button)

        self.fpsText = TextBox("Fps: ", (255, 255, 255), 'Arial', 20, 10, 10)
        self.gui.add(self.fpsText)

        self.selected_element = "grass"

        self.coinsVar = TextBox("Coins: ", (255, 255, 255), 'Arial', 50, 10, 40)
        self.gui.add(self.coinsVar)

        self.money = 0

        self.death_y = 900
        
        self.menu = Menu(self)
        self.update_gui()

        self.inGameMenu = inGameMenu(self)


    def update_gui(self):
        self.gui.empty()
        
        for i in range(len(self.blocks_data)):
            tile = list(self.blocks_data.keys())[i]
            element_button = ElementButton(20 + i * 100, 100, 50, self.pixel_size, tile, self.blocks_tileset, self.blocks_data)
            self.gui.add(element_button)

        element_button = ElementButton(20 + len(self.blocks_data)* 100 + 100, 100, 50, self.pixel_size, "coin", self.coins_tileset, self.coins_data)
        self.gui.add(element_button)
        
        self.gui.add(self.fpsText)
        self.gui.add(self.coinsVar)

    def load_level(self, new=False):
        if not self.level_name:
            return

        self.pathToWorld = f"levels/{self.level_name}.json"
        
        if new and not os.path.exists(self.pathToWorld):
            new_level_data = {
                "elements": [
                    {
                        "type": "mario",
                        "x": 100,
                        "y": 36
                    },
                    {
                        "type": "camera",
                        "name": "camera",
                        "x": 0,
                        "y": 0
                    },
                    {
                        "type": "block",
                        "name": "grass",
                        "x": 100,
                        "y": 100
                    }
                ]
            }
            with open(self.pathToWorld, 'w') as f:
                json.dump(new_level_data, f, indent=4)
        
        self.world = World(self.pathToWorld, self.pixel_size, self.debug)
        self.camera = self.world.loadWorld(self.window, self.death_y)
        self.scene = "game"
        

    def run(self):
        while self.running:
            if self.scene == "menu":
                self.menu.run()
            elif self.scene == "in-game-menu":
                self.inGameMenu.run()
            elif self.scene == "game":
                if self.world is None:
                    print("Error: No level loaded!")
                    self.scene = "menu"
                    continue
                
                dt = 0
                if self.fps > 0:
                    dt = self.clock.tick(self.fps) / 1000
                
                if dt == 0: continue
                self.handle_events()
                self.update(dt)
                self.render(dt)

        if self.world:
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
                    if not clicked_on_gui and self.world:
                        self.world.handle_element_placement(event.pos, self.camera, self.selected_element)
            
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE] and self.world == None:
            if self.world:
                self.world.saveWorld(self.camera)
            self.scene = "menu"
            return
        elif keys[pygame.K_ESCAPE] and self.world:
            self.scene = "in-game-menu"
        
        elif keys[pygame.K_s] and keys[pygame.K_LCTRL] and self.world:
            self.world.saveWorld(self.camera)

    def update(self, dt):
        if not self.world:
            return
            
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        coins_collected = self.world.update(keys, mouse_pos, self.camera, self.window, dt)
        if coins_collected > 0:
            self.money += coins_collected
            self.coinsVar.setText("Coins: " + str(self.money), (255, 255, 255))

        self.camera.follow(self.world.player)

        if dt > 0:
            self.fpsText.setText("Fps: " + str(int(1/dt)), (255, 255, 255))


        
            

    def render(self, dt):
        if not self.world:
            return
        self.renderer.render(self.world, self.gui, dt, self.camera, self.scene, self.window)
        
        
        pygame.display.flip()
