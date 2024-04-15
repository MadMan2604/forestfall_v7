# Script for the options screen game state 
import pygame
import sys 

from scripts.settings import *
from states.base_state import BaseState
from scripts.buttons import LoadButton

# options screen class 
class OptionsScreen(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.screen = self.game.screen
        self.fullscreen = False  

    def update(self, events):

        fullscreen_img = BUTTON_PATH + 'optionsscreen/fullscreen.png'
        windowed_img = BUTTON_PATH + 'optionsscreen/windowed.png'
        back_img = BUTTON_PATH + 'optionsscreen/back.png'

        fullscreen_button = LoadButton(fullscreen_img, (16, 200))
        windowed_button = LoadButton(windowed_img, (16, 500))
        back_button = LoadButton(back_img, (16, 700))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if fullscreen_button.rect.collidepoint(event.pos):
                    self.fullscreen = True
                elif windowed_button.rect.collidepoint(event.pos):
                    self.fullscreen = False
                elif back_button.rect.collidepoint(event.pos):
                    self.game.state_manager.change_state("title_screen")
        
        self.screen.fill((0, 0, 0))
        
        

        fullscreen_button.draw(self.screen)
        windowed_button.draw(self.screen)
        back_button.draw(self.screen)

