import pygame
import json
from mario import Mario
from world import World
from textBox import TextBox
from button import Button

#settings
fps = 60
pixel_size = 5
level = 'level2.json'

scene = "play_level"

#create window
pygame.init()
window = pygame.display.set_mode((1800, 1000), pygame.RESIZABLE)
pygame.display.set_caption("Mario 2.0")
font  = pygame.font.SysFont('Constantia', 15)
clock = pygame.time.Clock()
sky = (135, 205, 255)

#load mario.json and blocks.json
with open('mario.json') as m: 
    mario_data = json.load(m)
with open('blocks.json') as b:
    blocks_data = json.load(b)

#load tileset
mario_tileset = pygame.image.load("assets/mario tiles.png").convert_alpha()
background_tileset = pygame.image.load("assets/background tiles.png").convert_alpha()


#create mario
mario = Mario(400, 200, 16 * pixel_size,32 * pixel_size)

#create world
world = World(level, pixel_size, blocks_data)
world.loadWorldData()
blocks = world.loadWorld()

#textbox for fps
testbox = TextBox("Fps: ", (255, 255, 255), 'Cinstantia', 50, 20, 20)


edit_button = Button(20, 100, 50, 200, 60, (0, 0, 255), (255, 255, 255), "Edit Level", 'Cinstantia')
play_button = Button(20, 180, 50, 200, 60, (0, 0, 255), (255, 255, 255), "Play Level", 'Cinstantia')





def playLevel(window, sky, dt, mario, blocks, mario_data, mario_tileset, blocks_data, background_tileset, pixel_size):
    #clear window and fill in blue
    window.fill(sky)

    #update and draw mario
    keys = pygame.key.get_pressed()
    mario.update(keys, blocks, dt, window)
    mario.draw(dt, window, mario_data, mario_tileset, pixel_size)

    #draw blocks
    for block in blocks:
        block.draw(window, blocks_data, background_tileset, pixel_size)



def editLevel(window):
    #clear window and fill in blue
    window.fill(sky)
    




#main loop
dt = 0
run = True
while(run):
    #check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if scene == "play_level":
        playLevel(window, sky, dt, mario, blocks, mario_data, mario_tileset, blocks_data, background_tileset, pixel_size)
    
    elif scene == "edit_level":
        editLevel(window)
        
    if edit_button.isPressed():
        scene = "edit_level"
    
    if play_button.isPressed():
        scene = "play_level"
    

    play_button.draw(window)
    edit_button.draw(window)

    #show fps
    dt = clock.tick(fps)/1000
    testbox.setText("Fps: " + str(int(1/dt)), (255, 255, 255))
    testbox.draw(window)
    pygame.display.flip()

pygame.quit()