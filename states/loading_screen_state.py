# Script for the loading screen game state 
# Play Button --> Loading Screen --> InGame 
import pygame 

from scripts.settings import * 
from states.base_state import BaseState
from scripts.buttons import LoadButton

# class for the loading screen 
class LoadingScreen(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.screen = self.game.screen 
        self.clock = pygame.time.Clock()

        # Define fonts
        self.font = pygame.font.Font(FONT1, 80)
        self.font1 = pygame.font.Font(FONT2, 80)

        # loading 
        self.progress = 0
    
    # loading bar function, draws it onto the game screen
    def draw_loading_bar(self, progress):

        # draw the progress bar background
        pygame.draw.rect(self.screen, BLACK, (400, 750, 600, 50))
        # draw the progress bar
        pygame.draw.rect(self.screen, WHITE, (410, 755, progress * 5.8, 40))

    

    def update(self, events):


        enter_img = BUTTON_PATH + 'loadingscreen/enter.png'
        enter_button = LoadButton(enter_img, (1000, 800))

        back_img = BUTTON_PATH + 'loadingscreen/back.png'
        back_button = LoadButton(back_img, (100, 800))

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if enter_button.rect.collidepoint(event.pos):
                    print("in game")
                    self.game.state_manager.change_state("game")
                elif back_button.rect.collidepoint(event.pos):
                    self.game.state_manager.change_state("title_screen")
                    self.game.state_manager.exit_state("loading_screen")

        
        self.screen.fill((0, 0, 0))

        loading_bg = pygame.image.load('data/images/backgrounds/loadingscreen.png').convert_alpha()
        loading_bg = pygame.transform.scale(loading_bg, (WIDTH, HEIGHT))
        self.screen.blit(loading_bg, (0, 0))

        loading_txt = self.font.render('Loading...', True, BLACK)
        self.screen.blit(loading_txt, (530, 500))


        # calculate the width of the loading bar
        self.draw_loading_bar(self.progress)

        if self.progress < 100:
            self.progress += 1
        else:
            # once loading is complete, display the enter button
            enter_button.draw(self.screen)
            back_button.draw(self.screen)
            self.progress == False 

        pygame.time.delay(100)
        
        
        pygame.display.update() 
     
