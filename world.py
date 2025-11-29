import json

from elements.mario import Mario
import pygame
from elements.block import Block
from elements.coin import Coin

class World:
    def __init__(self, pathToWorld, pixel_size, debug):
        self.pathToWorld = pathToWorld
        self.world_data = None
        self.pixel_size = pixel_size
        self.debug = debug
    
    def loadWorld(self):
        with open(self.pathToWorld) as w:
            self.world_data = json.load(w)
        
        with open('assets/blocks.json') as b:
            blocks_data = json.load(b)
        
        blocks = pygame.sprite.Group()
        coins = pygame.sprite.Group()
        mario = None
        
        for el in self.world_data["elements"]:
            t = el["type"]
            if t == "mario":
                x = int(el["x"])
                y = int(el["y"])
                mario = Mario(x, y, 16 * self.pixel_size, 32 * self.pixel_size, self.debug)
            elif t == "block":
                x = int(el["x"])
                y = int(el["y"])
                tile = el["name"]
                block = self.createBlock(x, y, tile, blocks_data, self.pixel_size, self.debug)
                blocks.add(block)
            elif t == "entity":
                if el["name"] == "coin":
                    x = int(el["x"])
                    y = int(el["y"])
                    
                    coin = Coin(x, y, 16 * self.pixel_size, 16 * self.pixel_size)
                    coins.add(coin)

        return blocks, mario, coins

    def saveWorld(self, blocks, mario, entities, level):
        elements = []

        # Mario element first
        mario_element = {
            "type": "mario",
            "x": mario.rect.x,
            "y": mario.rect.y
        }
        elements.append(mario_element)

        # Block elements
        for block in blocks:
            block_element = {
                "type": "block",
                "name": block.tile,
                "x": block.rect.x,
                "y": block.rect.y,
            }
            elements.append(block_element)
        # Coin elements
        for coin in entities:
            coin_element = {
                "type": "entity",
                "name": "coin",
                "x": coin.rect.x,
                "y": coin.rect.y,
            }
            elements.append(coin_element)
        world_data = {
            "elements": elements
        }

        with open(level, 'w') as l:
            json.dump(world_data, l, indent=4)
            
        
    def createBlock(self, x, y, tile, blocks_data, pixel_size, debug):
        width = blocks_data[tile][2]["w"] * pixel_size
        height = blocks_data[tile][3]["h"] * pixel_size
        return Block(x, y, width, height, tile, debug)
        