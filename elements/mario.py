import pygame
from util.animation import Animation

class Mario(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, debug):
        super().__init__()
        self.x = x
        self.y = y
        self.spawnX = self.x
        self.spawnY = self.y
        self.width = width
        self.height = height

        self.velX = 0
        self.velY = 0
        self.speed = 200
        self.jump_power = 1000
        self.gravity = 2000

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (255, 0, 255)
        self.on_ground = False
        self.jump = False

        self.animation = Animation(["run1", "run2", "run3", "run4"], 0.1)
        self.animation_state = "idle"
        self.direction = True

        self.debug = debug

        self.offsetX = 0


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
            self.jump = True
        
        elif keys[pygame.K_DOWN]:
            self.animation_state = "crouch"
    
        if self.jump:
            if self.on_ground:
                self.jump = False
            self.animation_state = "jump"
            if not keys[pygame.K_UP] and self.velY < 0:
                
                self.velY = 0
                self.jump = False

    def moveX(self, dt, blocks, window):
        
        if self.rect.x < window.get_width() * 0.2 or self.rect.x > window.get_width() * 0.8:
    
            for block in blocks:
                block.x += -self.velX * dt
                block.rect.x = block.x
            self.offsetX += -self.velX * dt
        else:
            self.rect.x += self.velX * dt
        # camera deadzone thresholds
        min_x = window.get_width() * 0.4
        max_x = window.get_width() * 0.6

        # If Mario is moving and outside the deadzone, move blocks opposite to Mario
        if self.velX != 0:
            if self.rect.x < min_x and self.velX < 0:
                # Mario tries to move left past min_x -> keep Mario at min_x and shift world right
                self.rect.x = int(min_x)
                for block in blocks:
                    block.x += -self.velX * dt
                    block.rect.x = round(block.x)
                self.offsetX += -self.velX * dt
                return
            elif self.rect.x > max_x and self.velX > 0:
                # Mario tries to move right past max_x -> keep Mario at max_x and shift world left
                self.rect.x = int(max_x)
                for block in blocks:
                    block.x += -self.velX * dt
                    block.rect.x = round(block.x)
                self.offsetX += -self.velX * dt
                return

        # Default: move Mario normally (inside deadzone or not moving)
        else:
            self.rect.x += self.velX * dt


    def moveY(self, dt, blocks):
        
        self.rect.y += self.velY * dt
        

    def update(self, keys, blocks, dt, window):
        self.handle_input(keys)

        # Apply gravity
        self.velY += self.gravity * dt

        # Horizontal movement
        self.moveX(dt, blocks, window)
        
        
        self.x, self.y = self.rect.topleft

        collision = pygame.sprite.spritecollide(self, blocks, False)
        if collision:
            for block in collision:
                if self.rect.colliderect(block.rect):
                    if self.velX > 0:  # moving right
                        self.rect.right = block.rect.left
                    elif self.velX < 0:  # moving left
                        self.rect.left = block.rect.right

        # Vertical movement (use previous rect to detect direction and avoid tunneling)
        prev_rect = self.rect.copy()
        self.moveY(dt, blocks)

        self.x, self.y = self.rect.topleft
        self.on_ground = False
        collision = pygame.sprite.spritecollide(self, blocks, False)
        if collision:
            for block in collision:
                if not self.rect.colliderect(block.rect):
                    continue
                # landed on top
                if prev_rect.bottom <= block.rect.top and self.rect.bottom > block.rect.top:
                    self.rect.bottom = block.rect.top
                    self.velY = 0
                    self.on_ground = True
                # hit head on underside
                elif prev_rect.top >= block.rect.bottom and self.rect.top < block.rect.bottom:
                    self.rect.top = block.rect.bottom
                    self.velY = 0
                else:
                    # fallback: resolve based on velocity
                    if self.velY > 0:
                        self.rect.bottom = block.rect.top
                        self.velY = 0
                        self.on_ground = True
                    elif self.velY < 0:
                        self.rect.top = block.rect.bottom
                        self.velY = 0
        
        if self.y > window.get_height():
            
            self.x = self.spawnX
            self.y = self.spawnY
            self.rect.x = self.x
            self.rect.y = self.y
            

        # Update position variables
        self.x, self.y = self.rect.topleft

    def draw(self, dt, window, mario_data, mario_tileset, pixel_size):
        if self.debug:
            pygame.draw.rect(window, (255, 0, 0), self.rect, 5)
        

        if self.animation_state == "run":
            self.animation_state = self.animation.nextFrame(dt)
            
            
        self.tile_x = mario_data[self.animation_state][0]["x"]
        self.tile_y = mario_data[self.animation_state][1]["y"]
        self.sprite = mario_tileset.subsurface(self.tile_x, self.tile_y, 16, 32)
        self.sprite = pygame.transform.flip(self.sprite, self.direction, False)
        self.sprite = pygame.transform.scale(self.sprite, (16 * pixel_size,32 * pixel_size))
        window.blit(self.sprite, (self.rect.x, self.rect.y + pixel_size))
