from elements.entity import Entity
from util.animation import Animation
import pygame

class Coin(Entity):
    def __init__(self, x, y, width, height, can_collide, debug):
        super().__init__(x, y, width, height, can_collide, debug)
        self.color = (255, 223, 0)  # Gold color for the coin
        self.animation = Animation(["0", "1", "2", "3", "4", "5"], 0.1)
        self.current_frame = "0"
    
    def update(self, dt):
        # Animation returns a name string (e.g. "0")
        
        self.current_frame = self.animation.nextFrame(dt)

            

    def draw(self, window, coin_data, coin_tileset, pixel_size):
        if self.debug:
            pygame.draw.rect(window, (255, 255, 0), self.rect, 5)

        frame_key = str(self.current_frame)
        # guard if key missing
        if frame_key not in coin_data:
            return

        tile_x = int(coin_data[frame_key][0]["x"])
        tile_y = int(coin_data[frame_key][1]["y"])
        tile_width = int(coin_data[frame_key][2]["w"])
        tile_height = int(coin_data[frame_key][3]["h"])
        sprite = coin_tileset.subsurface(tile_x, tile_y, tile_width, tile_height)

        # scale to the coin's rect size so it matches collision box and is visible
        target_size = (self.rect.width, self.rect.height)
        sprite = pygame.transform.scale(sprite, target_size)
        window.blit(sprite, (self.rect.x, self.rect.y))
