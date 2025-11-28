import pygame
from entity import Entity

class Coin(Entity):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = (255, 223, 0)  # Gold color for the coin
        