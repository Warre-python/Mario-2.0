import pygame

from gui.button import Button
from gui.textBox import TextBox
from gui.inputText import InputText

class inGameMenu:
    def __init__(self, game):
        self.game = game

        self.buttons = pygame.sprite.Group()
        self.textboxes = pygame.sprite.Group()
        self.input_text = pygame.sprite.Group()

        self.active_menu = 'main'
        self.create_menus()

    def create_menus(self):
        self.buttons.empty()
        self.textboxes.empty()
        self.input_text.empty()
        self.level_name_input = None

        if self.active_menu == 'main':
            self.create_main_menu()

    def create_main_menu(self):
        width, height = self.game.window.get_size()
        self.buttons.add(Button(width / 2 - 100, height / 2, 200, 50, "Resume Game", lambda: setattr(self.game, 'scene', "game")))
        self.buttons.add(Button(width / 2 - 100, height / 2 + 60, 200, 50, "Save Game", lambda: self.game.world.saveWorld(self.game.camera)))
        self.buttons.add(Button(width / 2 - 100, height / 2 + 120, 200, 50, "To main menu", lambda: setattr(self.game, 'scene', "menu")))

        self.textboxes.add(TextBox("By Warre Decock", (255,255,255), "Arial", 20, 20, height - 40))

    def set_menu(self, menu_name):
        self.active_menu = menu_name
        self.create_menus()    
        return
    def run(self):
        self.set_menu('main')
        while self.game.running and self.game.scene == 'in-game-menu':
            if self.game.fps > 0:
                self.game.clock.tick(self.game.fps)
            
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if self.level_name_input:
                    self.level_name_input.handle_event(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        for button in self.buttons:
                            if button.rect.collidepoint(mouse_pos):
                                button.callback()
            
            self.buttons.update(mouse_pos)
            if self.level_name_input:
                self.input_text.update()
            
            self.game.window.fill((0, 0, 0))
            
            self.textboxes.draw(self.game.window)
            self.buttons.draw(self.game.window)
            if self.level_name_input:
                for box in self.input_text:
                    box.draw(self.game.window)
            
            pygame.display.flip()
