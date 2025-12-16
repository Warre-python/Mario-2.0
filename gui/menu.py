import pygame
from gui.button import Button
from gui.textBox import TextBox
from gui.inputText import InputText
import os

class Menu:
    def __init__(self, game):
        self.game = game
        self.buttons = pygame.sprite.Group()
        self.textboxes = pygame.sprite.Group()
        self.input_text = pygame.sprite.Group()
        self.level_name_input = None

        self.active_menu = 'main'
        self.create_menus()

    def create_menus(self):
        self.buttons.empty()
        self.textboxes.empty()
        self.input_text.empty()
        self.level_name_input = None

        if self.active_menu == 'main':
            self.create_main_menu()
        elif self.active_menu == 'new_level':
            self.create_new_level_menu()
        elif self.active_menu == 'load_level':
            self.create_load_level_menu()
        elif self.active_menu == 'settings':
            self.create_settings_menu()

    def create_main_menu(self):
        width, height = self.game.window.get_size()
        
        title = TextBox("Mario 2.4", (255,255,255), "Arial", 50, 0, height / 4)
        title.setPos(width / 2 - title.rect.width / 2, height / 4)
        self.textboxes.add(title)
        
        self.buttons.add(Button(width / 2 - 100, height / 2, 200, 50, "New Level", lambda: self.set_menu('new_level')))
        self.buttons.add(Button(width / 2 - 100, height / 2 + 60, 200, 50, "Load Level", lambda: self.set_menu('load_level')))
        self.buttons.add(Button(width / 2 - 100, height / 2 + 120, 200, 50, "Settings", lambda: self.set_menu('settings')))
        self.buttons.add(Button(width / 2 - 100, height / 2 + 180, 200, 50, "Quit", self.quit_game))

    def create_new_level_menu(self):
        width, height = self.game.window.get_size()
        
        title = TextBox("New Level", (255,255,255), "Arial", 50, 0, height / 4)
        title.setPos(width / 2 - title.rect.width / 2, height / 4)
        self.textboxes.add(title)

        self.level_name_input = InputText(width / 2 - 150, height / 2, 300, 50, (150, 150, 150), (255, 255, 255), "Arial", 32, (100, 100, 100))
        self.input_text.add(self.level_name_input)
        
        self.buttons.add(Button(width / 2 - 100, height / 2 + 60, 200, 50, "Start", self.start_new_level))
        self.buttons.add(Button(width / 2 - 100, height / 2 + 120, 200, 50, "Back", lambda: self.set_menu('main')))

    def create_load_level_menu(self):
        width, height = self.game.window.get_size()
        title = TextBox("Load Level", (255,255,255), "Arial", 50, 0, height / 4)
        title.setPos(width / 2 - title.rect.width / 2, height / 4)
        self.textboxes.add(title)
        
        y_offset = height / 2 - 60
        levels = [f for f in os.listdir('levels') if f.endswith('.json')]
        for level in levels:
            level_name = level.replace('.json', '')
            self.buttons.add(Button(width / 2 - 100, y_offset, 200, 50, level_name, lambda l=level_name: self.load_level(l)))
            y_offset += 60
            
        self.buttons.add(Button(width / 2 - 100, y_offset + 20, 200, 50, "Back", lambda: self.set_menu('main')))

    def create_settings_menu(self):
        width, height = self.game.window.get_size()
        title = TextBox("Settings", (255,255,255), "Arial", 50, 0, height / 4)
        title.setPos(width / 2 - title.rect.width / 2, height / 4)
        self.textboxes.add(title)
        
        # Debug Mode
        debug_text = TextBox(f"Debug Mode: {'On' if self.game.debug else 'Off'}", (255,255,255), "Arial", 30, 0, height / 2 - 90)
        debug_text.setPos(width / 2 - debug_text.rect.width / 2, height / 2 - 90)
        self.textboxes.add(debug_text)
        self.buttons.add(Button(width / 2 - 100, height / 2 - 60, 200, 50, "Toggle Debug", self.toggle_debug))

        # Pixel Size
        pixel_text = TextBox(f"Pixel Size: {self.game.pixel_size}", (255,255,255), "Arial", 30, 0, height / 2 - 10)
        pixel_text.setPos(width / 2 - pixel_text.rect.width / 2, height / 2 - 10)
        self.textboxes.add(pixel_text)
        self.buttons.add(Button(width / 2 - 75, height / 2 + 20, 50, 50, "-", lambda: self.change_pixel_size(-1)))
        self.buttons.add(Button(width / 2 + 25, height / 2 + 20, 50, 50, "+", lambda: self.change_pixel_size(1)))

        # FPS
        fps_text = TextBox(f"FPS: {self.game.fps}", (255,255,255), "Arial", 30, 0, height / 2 + 70)
        fps_text.setPos(width / 2 - fps_text.rect.width / 2, height / 2 + 70)
        self.textboxes.add(fps_text)
        self.buttons.add(Button(width / 2 - 75, height / 2 + 100, 50, 50, "-", lambda: self.change_fps(-10)))
        self.buttons.add(Button(width / 2 + 25, height / 2 + 100, 50, 50, "+", lambda: self.change_fps(10)))
        
        self.buttons.add(Button(width / 2 - 100, height / 2 + 180, 200, 50, "Back", lambda: self.set_menu('main')))

    def set_menu(self, menu_name):
        self.active_menu = menu_name
        self.create_menus()
        
    def start_new_level(self):
        if self.level_name_input:
            level_name = self.level_name_input.text
            if level_name:
                self.game.level_name = level_name
                self.game.load_level(new=True)
                self.game.scene = 'game'

    def load_level(self, level_name):
        self.game.level_name = level_name
        self.game.load_level()
        self.game.scene = 'game'
        
    def toggle_debug(self):
        self.game.debug = not self.game.debug
        self.create_menus()

    def change_pixel_size(self, amount):
        self.game.pixel_size += amount
        if self.game.pixel_size < 1:
            self.game.pixel_size = 1
        self.game.update_gui()
        self.create_menus()

    def change_fps(self, amount):
        self.game.fps += amount
        if self.game.fps < 10:
            self.game.fps = 10
        if self.game.fps == 0:
            self.game.fps = 100
        self.create_menus()

    def quit_game(self):
        self.game.running = False

    def run(self):
        self.set_menu('main')
        while self.game.running and self.game.scene == 'menu':
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
