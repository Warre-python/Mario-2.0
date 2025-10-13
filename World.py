import json


class World:
    def __init__(self, pathToWorld):
        self.pathToWorld = pathToWorld
        self.world_data = None
        self.yBlocks = []
    def loadWorldData(self):
        with open(self.pathToWorld) as l:
            self.world_data = json.load(l)
    
    def loadWorld(self):
        self.yBlocks.append()