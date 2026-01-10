import pygame
import json
import os
from elements.player import Player
from elements.block import Block

from elements.entities.coin import Coin
from camera import Camera

class World:
    def __init__(self, pathToWorld, pixel, debug):
        self.pixel = pixel
        self.debug = debug
        self.pathToWorld = pathToWorld
        self.level_name = pathToWorld.split('/')[-1].replace('.json', '')

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
            
            element_width = 0
            element_height = 0

            if selected_element == "coin":
                element_width = self.pixel
                element_height = self.pixel
            else:
                element_width = self.blocks_data[selected_element][2]["w"] * self.pixel / 16
                element_height = self.blocks_data[selected_element][3]["h"] * self.pixel / 16

            centered_x = grid_x + (self.pixel / 2) - (element_width / 2)
            centered_y = grid_y + (self.pixel / 2) - (element_height / 2)
            
            if selected_element == "coin":
                self.entities.add(Coin(centered_x, centered_y, self.pixel, self.coin_data, self.coin_tileset, self.debug))
            else:
                self.tiles.add(Block(centered_x, centered_y, selected_element, self.pixel, self.blocks_data, self.block_tileset, self.debug))

    def loadWorld(self, window, death_y):
        with open(self.pathToWorld) as w:
            self.world_data = json.load(w)

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
        
        self.death_y = death_y

        camera = Camera(0, 0, window.width, window.height)

        self.player = Player(100, 100, self.pixel, self.mario_data, self.mario_tileset, self.debug)
        self.player_group.add(self.player)
        
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

    def setCheckpoint(self, camera):
        print("Setting checkpoint...")
        checkpoint_data = {
            "player_x": self.player.rect.x,
            "player_y": self.player.rect.y,
            "camera_x": camera.x,
            "camera_y": camera.y
        }
        with open(f"levels/{self.level_name}_checkpoint.json", 'w') as f:
            json.dump(checkpoint_data, f, indent=4)
        print("Checkpoint set.")

    def loadCheckpoint(self, camera):
        checkpoint_path = f"levels/{self.level_name}_checkpoint.json"
        if not os.path.exists(checkpoint_path):
            print(f"No checkpoint found for level {self.level_name}")
            return False
        
        with open(checkpoint_path, 'r') as f:
            checkpoint_data = json.load(f)
        
        self.player.rect.x = checkpoint_data["player_x"]
        self.player.rect.y = checkpoint_data["player_y"]
        camera.x = checkpoint_data["camera_x"]
        camera.y = checkpoint_data["camera_y"]
        
        print(f"Checkpoint loaded for level {self.level_name}")
        return True

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

    