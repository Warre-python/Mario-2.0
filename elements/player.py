import pygame
from util.animation import Animation

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, pixel, mario_data, mario_tileset, debug):
        super().__init__()
        self.x, self.y = x, y

        self.spawnX = self.x
        self.spawnY = self.y

        self.pixel = pixel

        self.velX = 0
        self.velY = 0

        self.speed = 200
        self.jump_power = 1000
        self.gravity = 2000

        self.animation_state = "idle"

        self.animation = Animation(["run1", "run2", "run3", "run4"], 0.1)

        self.direction = False

        self.on_ground = False
        self.jump = False
        
        self.rect = pygame.Rect(x, y, self.pixel * 1, self.pixel*2)

        self.image = self.rect
                

        self.mario_data = mario_data

        self.mario_tileset = mario_tileset

        self.debug = debug

    def handle_input(self, keys):
        self.velX = 0
        self.animation_state = "idle"
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.velX = -self.speed
            self.animation_state = "run"
            self.direction = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velX = self.speed
            self.animation_state = "run"
            self.direction = True

        if (keys[pygame.K_UP] or keys[pygame.K_z]) and self.on_ground:
            self.velY = -self.jump_power
            self.on_ground = False
            self.animation_state = "jump"
            self.jump = True
        
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.animation_state = "crouch"
    
        if self.jump:
            if self.on_ground:
                self.jump = False
            self.animation_state = "jump"
            if not (keys[pygame.K_UP] or keys[pygame.K_z]) and self.velY < 0:
                
                self.velY = 0
                self.jump = False

    def update(self, keys, tiles, camera, window, dt, death_y):
        self.handle_input(keys)
        self.velY += self.gravity * dt

        if self.y > death_y:
            #respawn
            camera.x = 0
            camera.y = 0
            self.x = self.spawnX
            self.y = self.spawnY
            
        # Horizontal movement and collision
        self.x += self.velX * dt
        self.rect.x = int(self.x)
        collided_tiles_x = pygame.sprite.spritecollide(self, tiles, False)
        for tile in collided_tiles_x:
            if self.velX > 0:
                self.rect.right = tile.rect.left
            elif self.velX < 0:
                self.rect.left = tile.rect.right
            self.x = self.rect.x

        # Vertical movement and collision
        self.on_ground = False
        self.y += self.velY * dt
        self.rect.y = int(self.y)
        collided_tiles_y = pygame.sprite.spritecollide(self, tiles, False)
        for tile in collided_tiles_y:
            if self.velY > 0:
                self.rect.bottom = tile.rect.top
                self.on_ground = True
                self.velY = 0
            elif self.velY < 0:
                self.rect.top = tile.rect.bottom
                self.velY = 0
            self.y = self.rect.y
    
    def draw(self, camera, dt, window):

        if self.debug:
            pygame.draw.rect(window, (255, 0, 0), camera.apply(self.rect), 5)
        

        if self.animation_state == "run":
            self.animation_state = self.animation.nextFrame(dt)
            
            
        self.tile_x = self.mario_data[self.animation_state][0]["x"]
        self.tile_y = self.mario_data[self.animation_state][1]["y"]
        self.sprite = self.mario_tileset.subsurface(self.tile_x, self.tile_y, 16, 32)
        self.newRect = (self.rect).move(0, self.pixel/16)
        self.sprite = pygame.transform.flip(self.sprite, self.direction, False)
        self.sprite = pygame.transform.scale(self.sprite, (1 * self.pixel,2* self.pixel))
        window.blit(self.sprite, camera.apply(self.newRect))
        