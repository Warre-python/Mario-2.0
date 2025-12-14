import pygame
from game import Game

debug = False
def main():
    global debug
    pygame.init()
    
    fps = 0
    pixel = 64

    print("creating window")
    window = pygame.display.set_mode((1500, 800), pygame.RESIZABLE)
    pygame.display.set_caption("Mario 2.4")

    print("creating clock")
    clock = pygame.time.Clock()

    print("creating game")
    game = Game(window, clock, pixel, fps, debug)

    game.run()

    

def changeDebug():
    global debug
    if debug == True:
        debug = False
    elif debug == False:
        debug = True

if __name__ == "__main__":
    print("Def: main")
    main()
    print("stop game")
