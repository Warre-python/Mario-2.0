import pygame
from animation import Animation

class Mario:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.velX = 0
        self.velY = 0
        self.speed = 300
        self.jump_power = 1000
        self.gravity = 2000

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (255, 0, 255)
        self.on_ground = False

        self.animation = Animation(["run1", "run2", "run3", "run4"], 0.1)
        self.animation_state = "idle"
        self.direction = True


    def handle_input(self, keys):
        self.velX = 0
        self.animation_state = "idle"
        if keys[pygame.K_LEFT]:
            self.velX = -self.speed
            self.animation_state = "run"
            self.direction = False
        elif keys[pygame.K_RIGHT]:
            self.velX = self.speed
            self.animation_state = "run"
            self.direction = True

        if keys[pygame.K_UP] and self.on_ground:
            self.velY = -self.jump_power
            self.on_ground = False
            self.animation_state = "jump"
        
        elif keys[pygame.K_DOWN]:
            self.animation_state = "crouch"

    def update(self, keys, blocks, dt, window):
        self.handle_input(keys)

        # Apply gravity
        self.velY += self.gravity * dt

        # Horizontal movement
        self.rect.x += self.velX * dt
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if self.velX > 0:  # moving right
                    self.rect.right = block.rect.left
                elif self.velX < 0:  # moving left
                    self.rect.left = block.rect.right

        # Vertical movement
        self.rect.y += self.velY * dt
        self.on_ground = False
        for block in blocks:
            if self.rect.colliderect(block.rect):
                if self.velY > 0:  # falling
                    self.rect.bottom = block.rect.top
                    self.velY = 0
                    self.on_ground = True
                elif self.velY < 0:  # hitting ceiling
                    self.rect.top = block.rect.bottom
                    self.velY = 0

        # Update position variables
        self.x, self.y = self.rect.topleft

    def draw(self, dt, window, mario_data, mario_tileset, pixel_size):
        #pygame.draw.rect(window, (255, 0, 0), self.rect)
        

        if self.animation_state == "run":
            self.animation_state = self.animation.nextFrame(dt)
            
            
        self.tile_x = mario_data[self.animation_state][0]["x"]
        self.tile_y = mario_data[self.animation_state][1]["y"]
        self.sprite = mario_tileset.subsurface(self.tile_x, self.tile_y, 16, 32)
        self.sprite = pygame.transform.flip(self.sprite, self.direction, False)
        self.sprite = pygame.transform.scale(self.sprite, (16 * pixel_size,32 * pixel_size))
        window.blit(self.sprite, (self.rect.x, self.rect.y + pixel_size))
