import json

from mario import Mario
import pygame
from block import Block

class World:
    def __init__(self, pathToWorld, pixel_size, blocks_data):
        self.pathToWorld = pathToWorld
        self.world_data = None
        self.pixel_size = pixel_size
        self.blocks_data = blocks_data
    def loadWorldData(self):
        with open(self.pathToWorld) as l:
            self.world_data = json.load(l)
    
    def loadWorld(self, debug):
        blocks = pygame.sprite.Group()

        # Loop through each block in the level data
        for block_id, block_info in self.world_data.items():
            if block_id == "mario_spawn":
                continue  # Skip mario spawn point
            x = block_info[0]["x"] * 16 * self.pixel_size 
            y = block_info[1]["y"] * 16 * self.pixel_size 
            tile = block_info[2]["tile"] 
            width = self.blocks_data[tile][2]["w"]
            height = self.blocks_data[tile][3]["h"]

            

            # Create a Block instance (assuming Block class exists)
            blocks.add(Block(x, y, width* self.pixel_size, height * self.pixel_size, tile, debug))

        x = self.world_data["mario_spawn"][0]["x"] * 16 * self.pixel_size
        y = self.world_data["mario_spawn"][1]["y"] * 16 * self.pixel_size     
        mario = Mario(x, y, 16 * self.pixel_size,32 * self.pixel_size, debug)

        return blocks, mario
    
    def createBlock(self, x, y, tile, blocks_data, pixel_size, debug):
        x = x
        y = y
        width = blocks_data[tile][2]["w"]
        height = blocks_data[tile][3]["h"]
        return Block(x, y, width * pixel_size, height * pixel_size, tile, debug)
    
    
    def saveWorld(self, blocks, mario):
        world_data = {}

        # Save block data
        for i, block in enumerate(blocks):
            block_info = [
                {"x": block.rect.x // (16 * self.pixel_size)},
                {"y": block.rect.y // (16 * self.pixel_size)},
                {"tile": block.tile}
            ]
            world_data[i] = block_info

        # Save Mario spawn point
        mario_spawn_info = [
            {"x": mario.spawnX // (16 * self.pixel_size)},
            {"y": mario.spawnY // (16 * self.pixel_size)}
        ]
        world_data["mario_spawn"] = mario_spawn_info

        # Write to JSON file
        with open("level4.json", 'w') as f:
            json.dump(world_data, f, indent=4)