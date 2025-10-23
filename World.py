import json
from Block import Block

class World:
    def __init__(self, pathToWorld, pixel_size):
        self.pathToWorld = pathToWorld
        self.world_data = None
        self.pixel_size = pixel_size
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

            # Create a Block instance (assuming Block class exists)
            blocks.append(Block(x, y, 16, 16, tile))
        return blocks