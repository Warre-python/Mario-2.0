import pygame
import json
from Mario import Mario
from Block import Block

pygame.init()
fps = 60
pixel_size = 5
window = pygame.display.set_mode((1100, 700), pygame.RESIZABLE)
pygame.display.set_caption("Mario 2.0")
font  = pygame.font.SysFont('Constantia', 15)
clock = pygame.time.Clock()
timer = 0
sky = (135, 205, 255)

with open('mario.json') as m: 
    mario_data = json.load(m)
with open('blocks.json') as b:
    blocks_data = json.load(b)
with open('level.json') as l:
    level_data = json.load(l)


mario_tileset = pygame.image.load("assets/mario tiles.png").convert_alpha()
background_tileset = pygame.image.load("assets/background tiles.png").convert_alpha()

mario = Mario(500, 100, 16, 32)

blocks = []

# Loop through each block in the level data
for block_id, block_info in level_data.items():
    x = block_info[0]["x"] * 16 * pixel_size - 500
    y = block_info[1]["y"] * 16 * pixel_size - 500
    tile = block_info[2]["tile"] 

    # Create a Block instance (assuming Block class exists)
    blocks.append(Block(x, y, 16, 16, tile))

run = True
while run:
    window.fill(sky)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    mario.update(keys, blocks)
    mario.draw(timer, window, mario_data, mario_tileset, pixel_size)
    for block in blocks:
        block.draw(window, blocks_data, background_tileset, pixel_size)
    pygame.display.flip()
    dt = clock.tick(fps)/1000
    
    if timer > 0.4:
        timer = 0

    timer += dt
    
pygame.quit()