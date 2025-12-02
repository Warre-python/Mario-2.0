from elements.block import Block
import pygame

class Pipe(Block):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, "pijp_boven", debug=False)
        self.tile = "pijp_boven"

    def update(self, dt, mario, mario_group):
        collision = pygame.sprite.spritecollide(self, mario_group, False)
        if collision:
            print("Mario collides with pipe")
            # Check if Mario is at the top of the pipe
            if mario.rect.bottom <= self.rect.top + 5:
                print("Mario is on top of the pipe")
                mario.x = self.rect.x
                mario.y = self.rect.y - mario.rect.height
                mario.rect.x = mario.x
                mario.rect.y = mario.y