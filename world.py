import json
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
    
    def loadWorld(self):
        blocks = []

        # Loop through each block in the level data
        for block_id, block_info in self.world_data.items():
            x = block_info[0]["x"] * 16 * self.pixel_size - 500
            y = block_info[1]["y"] * 16 * self.pixel_size - 500
            tile = block_info[2]["tile"] 
            width = self.blocks_data[tile][2]["w"]
            height = self.blocks_data[tile][3]["h"]

            

            # Create a Block instance (assuming Block class exists)
            blocks.append(Block(x, y, width* self.pixel_size, height * self.pixel_size, tile))
        return blocks