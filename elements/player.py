import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, pixel):
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
        self.direction = False

        self.on_ground = False
        self.jump = False
        
        self.rect = pygame.Rect(x, y, self.pixel * 0.95, self.pixel*2)

        self.image = self.rect

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

    def update(self, keys, tiles, camera, dt):
        self.handle_input(keys)
        self.velY += self.gravity * dt

        if self.y > 800:
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
        