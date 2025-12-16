import pygame
import json
from elements.player import Player
from elements.block import Block

from elements.entities.coin import Coin
from camera import Camera

class World:
    def __init__(self, pathToWorld, pixel, debug):
        self.pixel = pixel
        self.debug = debug
        self.pathToWorld = pathToWorld

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
                self.entities.add(Coin(grid_x, grid_y, self.pixel, self.coin_data, self.coin_tileset, self.debug))
            else:
                self.tiles.add(Block(grid_x, grid_y, selected_element, self.pixel, self.blocks_data, self.block_tileset, self.debug))

    def loadWorld(self, window):
        with open(self.pathToWorld) as w:
            self.world_data = json.load(w)

        if "elements" not in self.world_data:
            new_elements = []
            for key, value in self.world_data.items():
                try:
                    x = value[0]["x"]
                    y = value[1]["y"]
                    tile = value[2]["tile"]
                    new_elements.append({
                        "type": "block",
                        "name": tile,
                        "x": x * self.pixel,
                        "y": y * self.pixel
                    })
                except (IndexError, KeyError):
                    print(f"Warning: Could not parse element '{key}' in old format level '{self.pathToWorld}'. Skipping.")

            new_elements.append({"type": "mario", "x": 100, "y": 100})
            new_elements.append({"type": "camera", "name": "camera", "x": 0, "y": 0})
            
            self.world_data = {"elements": new_elements}
            
            with open(self.pathToWorld, 'w') as f:
                json.dump(self.world_data, f, indent=4)
        
        with open('assets/blocks.json') as b:
            self.blocks_data = json.load(b)
        
        with open('assets/coin.json') as c:
            self.coin_data = json.load(c)
        
        with open('assets/mario.json') as m: 
            self.mario_data = json.load(m)

        self.mario_tileset = pygame.image.load("assets/images/mario tiles.png").convert_alpha()
        self.coin_tileset = pygame.image.load("assets/images/coin.png").convert_alpha()
        self.block_tileset = pygame.image.load("assets/images/background tiles1.png").convert_alpha()
        
        self.tiles = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        
        self.death_y = 900
        
        for el in self.world_data["elements"]:
            t = el["type"]
            if t == "mario":
                x = int(el["x"])
                y = int(el["y"])
                self.player = Player(x, y, self.pixel, self.mario_data, self.mario_tileset, self.debug)
                self.player_group.add(self.player)
            elif t == "block":

                x = int(el["x"])
                y = int(el["y"])
                tile = el["name"] 
                block = Block(x, y, tile, self.pixel, self.blocks_data, self.block_tileset, self.debug)
                self.tiles.add(block)

            elif t == "entity":
                if el["name"] == "coin":
                    x = int(el["x"])
                    y = int(el["y"])
                    
                    coin = Coin(x, y, self.pixel, self.coin_data, self.coin_tileset, self.debug)
                    self.entities.add(coin)
            elif t == "camera":
                x = int(el["x"])
                y = int(el["y"])
                camera = Camera(x, y, window.width, window.height)

        return camera

    def saveWorld(self, camera):
        elements = []

        # Mario element first
        mario_element = {
            "type": "mario",
            "x": self.player.rect.x,
            "y": self.player.rect.y
        }
        elements.append(mario_element)

        # Block elements
        for block in self.tiles:
            block_element = {
                "type": "block",
                "name": block.tile,
                "x": block.rect.x,
                "y": block.rect.y,
            }
            elements.append(block_element)
        # Coin elements
        for coin in self.entities:
            if isinstance(coin, Coin):
                coin_element = {
                    "type": "entity",
                    "name": "coin",
                    "x": coin.rect.x,
                    "y": coin.rect.y,
                }
            elements.append(coin_element)
        camera_element = {
            "type": "camera",
            "name": "camera",
            "x": camera.x,
            "y": camera.y,

        }
        elements.append(camera_element)
        world_data = {
            "elements": elements
        }

        with open(self.pathToWorld, 'w') as l:
            json.dump(world_data, l, indent=4)

    def update(self, keys, mouse_pos, camera, window, dt):
        self.player.update(keys, self.tiles, camera, window, dt, self.death_y)
        
        coins_collected = 0
        for entity in self.entities:
            coins_collected += entity.update(dt, self.player_group, self.entities)

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
        
        return coins_collected
            
    