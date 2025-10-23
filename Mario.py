import pygame
from Vector import Vector

class Mario:
    def __init__(self, x, y, width, height):
        self.pos = Vector(x, y)
        self.dim = Vector(width, height)
        self.vel = Vector(0, 0)

        self.rect = pygame.Rect(self.pos.getX(), self.pos.getY(), self.dim.getX(), self.dim.getY())

        self.animation_state = "idle"
        self.direction = True
    def jump(self, on_ground=True):
        if on_ground:
            self.vel.setY(-6)
            self.animation_state = "jump"


    def left(self):
        self.vel.setX(-5)
        self.animation_state = "run"
        self.direction = False

    def right(self):
        self.vel.setX(5)
        self.animation_state = "run"
        self.direction = True

    def crouch(self):
        self.vel.setY(5)
        self.animation_state = "crouch"
    
    def stand(self):
        self.animation_state = "idle"
        self.vel.setX(0)
    
    def fall(self):
        self.vel.setY(self.vel.getY() + 0.01)# Gravity effect
        self.animation_state = "idle"

    def update(self, keys, blocks):
        # --- Apply horizontal movement ---
        if keys[pygame.K_LEFT]:
            self.left()
        elif keys[pygame.K_RIGHT]:
            self.right()
        else:
            self.stand()

        # --- Jump / crouch ---
        if keys[pygame.K_UP] and on_ground:
            self.jump(on_ground=True)

        elif keys[pygame.K_DOWN]:
            self.crouch()

        # --- Apply gravity ---
        self.vel.setY(self.vel.getY() + 0.3)  # gravity acceleration
        if self.vel.getY() > 5:               # limit fall speed
            self.vel.setY(5)

        # --- Predict next position ---
        next_pos = Vector(self.pos.getX(), self.pos.getY() + self.vel.getY())

        # --- Collision detection (simple ground check) ---
        on_ground = False
        for block in blocks:
            if block.collisionbox.rect.collidepoint(self.pos.getX(), self.pos.getY()):
                print(True)
                on_ground = True
                self.vel.setY(0)
                self.animation_state = "idle"
                break
            
            

        if not on_ground:
            self.animation_state = "idle"

        # --- Apply final position ---
        self.pos.add(self.vel.getX(), self.vel.getY())
        self.rect.topleft = (self.pos.getX(), self.pos.getY())

    def test(self, blocks, keys):
        if keys[pygame.K_LEFT]:
            self.pos.add(-5, 0)
        elif keys[pygame.K_RIGHT]:
            self.pos.add(5, 0)
        elif keys[pygame.K_DOWN]:
            self.pos.add(0, 5)
        if keys[pygame.K_UP]:
            self.pos.add(0, -5)

        elif keys[pygame.K_DOWN]:
            self.crouch()
        
        for block in blocks:
            #print("mario pos: ", self.pos.get())
            #print("mario dim: ", self.dim.get())
            #print("block pos: ", block.pos.get())
            #print("block dim: ", block.dim.get())
            if block.rect.colliderect(self.rect):
                print(True)
                self.vel.setY(0)
                self.animation_state = "idle"
                break
            else:
                print(False)

    def draw(self, time, window, mario_data, mario_tileset, pixel_size):
        
        run_frames = ["run1", "run2", "run3", "run4"]
        frame_duration = 0.1  # seconds per frame

        if self.animation_state.startswith("run"):
            # Determine which frame to display based on time
            frame_index = int((time / frame_duration) % len(run_frames))
            self.animation_state = run_frames[frame_index]
        self.tile_x = mario_data[self.animation_state][0]["x"]
        self.tile_y = mario_data[self.animation_state][1]["y"]
        self.sprite = mario_tileset.subsurface(self.tile_x, self.tile_y, 16, 32)
        self.sprite = pygame.transform.flip(self.sprite, self.direction, False)
        self.sprite = pygame.transform.scale(self.sprite, (16 * pixel_size,32 * pixel_size))
        window.blit(self.sprite, self.pos.get())