import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, pixel):
        super().__init__()
        self.x, self.y = x, y
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
        
        self.rect = pygame.Rect(x, y, self.pixel, self.pixel*2)

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
    
    def update(self, keys, dt):
        self.handle_input(keys)
        self.velY += self.gravity * dt
        self.x += self.velX
        self.y += self.velY
        self.rect.topleft = self.x, self.y
        