import pygame
import sys 

from states.state_manager import StateManager
from states.in_game_state import InGame
from states.title_screen_state import TitleScreen
from states.options_screen_state import OptionsScreen
from states.information_screen_state import InformationScreen 
from states.loading_screen_state import LoadingScreen
from scripts.settings import * 

# Game class
class Game:
    def __init__(self, screen):
        self.screen = screen  
        self.clock = pygame.time.Clock()
        self.running = True 
        self.state_manager = StateManager(self)

        # Initialise and add game states
        self.state_manager.add_state("title_screen", TitleScreen(self))
        self.state_manager.add_state("loading_screen", LoadingScreen(self))
        self.state_manager.add_state("game", InGame(self))
        self.state_manager.add_state("options_screen", OptionsScreen(self))
        self.state_manager.add_state("information_screen", InformationScreen(self))
        self.state_manager.change_state("title_screen")
    
    def run(self):
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False 
            
            self.state_manager.update(events)
      
            self.state_manager.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit() 