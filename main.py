from gui.block_button import BlockButton
import pygame
import json

from elements.mario import Mario
from world import World
from gui.textBox import TextBox
from gui.button import Button
from elements.entity import Entity
from elements.coin import Coin
from elements.block import Block

#settings
fps = 60
pixel_size = 3
debug = True

level = 'levels/level5.json'

scene = "play_level"

#create window
pygame.init()
window = pygame.display.set_mode((1500, 800), pygame.RESIZABLE)
pygame.display.set_caption("Mario 2.0")

clock = pygame.time.Clock()
sky = (135, 205, 255)

#load mario.json and blocks.json
with open('assets/mario.json') as m: 
    mario_data = json.load(m)
with open('assets/blocks.json') as b:
    blocks_data = json.load(b)
with open('assets/coin.json') as c:
    coin_data = json.load(c)

#load tileset
mario_tileset = pygame.image.load("assets/images/mario tiles.png").convert_alpha()
background_tileset = pygame.image.load("assets/images/background tiles1.png").convert_alpha()
coin_tileset = pygame.image.load("assets/images/coin.png").convert_alpha()




#create world
world = World(level, pixel_size, debug)

elements, mario = world.loadWorld()

mario_group = pygame.sprite.Group()
mario_group.add(mario)

#textbox for fps
testbox = TextBox("Fps: ", (255, 255, 255), 'arial', 20, 20, 20)
textbox = TextBox("Avg. Fps: ", (255, 255, 255), 'arial', 20, 100, 20)

coin_text = TextBox("Coins: 0", (255, 255, 255), 'arial', 50, 20, 50)
coins = 0


delete_all_button = Button(20, 340, 50, 200, 60, (0, 0, 255), (255, 255, 255), "Delete All", 'arial')

block_buttons = []

for i in range(len(blocks_data)):
    tile = list(blocks_data.keys())[i]
    block_button = BlockButton(20 + i * 70, 260, 50, 50, tile)
    block_buttons.append(block_button)




tile = "grass"

def playLevel(window, sky, dt, mario, mario_group, elements, mario_data, mario_tileset, blocks_data, background_tileset, pixel_size):
    #clear window and fill in blue
    global coins, coin_text
    window.fill(sky)

    
    #draw coins
    for coin in elements:
        if isinstance(coin, Coin):
            if coin.update(dt, mario_group, elements) == 1:
                coins += 1
                
                coin_text.setText("Coins: " + str(coins), (255, 255, 255))
        
            coin.draw(window, coin_data, coin_tileset, pixel_size)

    #draw blocks
    for block in elements:
        if isinstance(block, Block):
            block.update(dt, mario, mario_group)
            block.draw(window, blocks_data, background_tileset, pixel_size)
    
    #update and draw mario
    keys = pygame.key.get_pressed()
    mario.update(keys, elements, dt, window)
    mario.draw(dt, window, mario_data, mario_tileset, pixel_size)
    
        

tile = "grass"
pressed = False

def editLevel(window, delete_all_button, elements, blocks_data, background_tileset, pixel_size, pressed, tile, debug, mario):
    #clear window and fill in blue
    window.fill(sky)
    button_pressed = False

    
    
    for block_button in block_buttons:
        block_button.draw(window, blocks_data, background_tileset, pixel_size)
        if block_button.isPressed():
            tile = block_button.tile
            button_pressed = True

    for element in elements:
        element.draw(window, blocks_data, background_tileset, pixel_size)

    mouse_buttons = pygame.mouse.get_pressed()
    
    # Left click: add block
    if mouse_buttons[0] and not pressed:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Convert mouse position to world coordinates  
        world_x = mouse_x - mario.offsetX
        world_y = mouse_y - 0  # <-- you MUST track Y offset too!

        # Snap to grid in world space
        grid_x = (round(world_x / (16 * pixel_size)) * (16 * pixel_size))
        grid_y = (round(world_y / (16 * pixel_size)) * (16 * pixel_size)) 
        # Check if block already exists at this position
        block_exists = False
        for block in elements:
            if block.rect.x == grid_x and block.rect.y == grid_y:
                block_exists = True
                break
        
        # Only add block if position is empty
        if not block_exists and not button_pressed:
            new_block = world.createBlock(grid_x, grid_y, tile, blocks_data, pixel_size, True, debug)
            elements.add(new_block)
    
    # Right click: remove block
    if mouse_buttons[2] and not pressed:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for block in elements:
            if block.rect.collidepoint(mouse_x, mouse_y):
                elements.remove(block)
                break
    delete_all_button.draw(window)
    if delete_all_button.isPressed():
        elements.empty()


    return tile



#main loop
dt = 0
avg_fps = 0
frame_count = 0

run = True
while(run):
    #check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            world.saveWorld(elements, mario, level)
        

    if scene == "play_level":
        playLevel(window, sky, dt, mario, mario_group, elements, mario_data, mario_tileset, blocks_data, background_tileset, pixel_size)
    
    elif scene == "edit_level":
        tile = editLevel(window, delete_all_button, elements, blocks_data, background_tileset, pixel_size, pressed, tile, debug, mario)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_e]:
        scene = "edit_level"
        pressed = True
    
    elif keys[pygame.K_p]:
        scene = "play_level"
        pressed = True

    else:
        pressed = False

   

    #show fps
    dt = clock.tick(fps)/1000
    testbox.setText("Fps: " + str(int(1/dt)), (255, 255, 255))
    testbox.draw(window)
    
    avg_fps += 1/dt
    frame_count += 1
    average_fps = avg_fps / frame_count
    textbox.setText("Avg. Fps: " + str(int(average_fps)), (255, 255, 255))
    textbox.draw(window)
    coin_text.draw(window)
    pygame.display.flip()

pygame.quit()