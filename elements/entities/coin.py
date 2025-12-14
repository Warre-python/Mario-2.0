import pygame
import json
from elements.entity import Entity
from util.animation import Animation

class Coin(Entity):
    def __init__(self, x, y, pixel, debug):
        super().__init__(x, y, pixel, debug)
        with open('assets/coin.json') as c:
            self.coin_data = json.load(c)
        self.coin_tileset = pygame.image.load("assets/images/coin.png").convert_alpha()
        self.color = (255, 223, 0)  # Gold color for the coin
        self.animation = Animation(["0", "1", "2", "3", "4", "5"], 0.1)
        self.current_frame = "0"
    
    def update(self, dt, player, entities):
        # Animation returns a name string (e.g. "0")
        
        self.current_frame = self.animation.nextFrame(dt)

        
        collision = pygame.sprite.spritecollide(self, player, False, None)
        if collision:
            entities.remove(self)
            return 1
        return 0

    def draw(self, camera, dt, window):
        if self.debug:
            pygame.draw.rect(window, self.color, camera.apply(self.rect), 5)

        frame_key = str(self.current_frame)
        # guard if key missing
        if frame_key not in self.coin_data:
            return

        tile_x = int(self.coin_data[frame_key][0]["x"])
        tile_y = int(self.coin_data[frame_key][1]["y"])
        tile_width = int(self.coin_data[frame_key][2]["w"])
        tile_height = int(self.coin_data[frame_key][3]["h"])
        sprite = self.coin_tileset.subsurface(tile_x, tile_y, tile_width, tile_height)

        # scale to the coin's rect size so it matches collision box and is visible
        target_size = (self.rect.width, self.rect.height)
        sprite = pygame.transform.scale(sprite, target_size)
        window.blit(sprite, camera.apply(self.rect))