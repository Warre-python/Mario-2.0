import pygame
import json
from Mario import Mario

pygame.init()
fps = 60
pixel_size = 5
window = pygame.display.set_mode((1600, 1000), pygame.RESIZABLE)
pygame.display.set_caption("Mario 2.0")
font  = pygame.font.SysFont('Constantia', 15)
clock = pygame.time.Clock()
timer = 0
sky = (135, 205, 255)

with open('mario.json') as m: 
    mario_data = json.load(m)
with open('blocks.json') as b:
    blocks_data = json.load(b)

mario_tileset = pygame.image.load("assets/mario tiles.png").convert_alpha()
background_tileset = pygame.image.load("assets/mario tiles.png").convert_alpha()

mario = Mario(50, 100, 16, 32)

run = True
while run:
    window.fill(sky)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    mario.update(keys)
    mario.draw(timer, window, mario_data, mario_tileset, pixel_size)

    pygame.display.flip()
    dt = clock.tick(fps)/1000
    
    if timer == 0.2:
        timer = 0

    timer += dt
    
pygame.quit()