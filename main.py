import pygame
import json
from Mario import Mario
from Block import Block
from World import World

pygame.init()
fps = 60
pixel_size = 5
level = 'level.json'

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



mario_tileset = pygame.image.load("assets/mario tiles.png").convert_alpha()
background_tileset = pygame.image.load("assets/background tiles.png").convert_alpha()

mario = Mario(500, 100, 16, 32)

world = World(level, pixel_size)
world.loadWorldData()
blocks = world.loadWorld()

run = True
while run:
    window.fill(sky)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    #mario.update(keys, blocks)
    mario.test(blocks, keys)
    mario.draw(timer, window, mario_data, mario_tileset, pixel_size)
    for block in blocks:
        block.draw(window, blocks_data, background_tileset, pixel_size)
    pygame.display.flip()
    dt = clock.tick(fps)/1000
    
    if timer > 0.4:
        timer = 0

    timer += dt
    
pygame.quit()