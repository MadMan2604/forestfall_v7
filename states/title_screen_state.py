import pygame 
import sys 

from scripts.settings import *
from states.base_state import BaseState

class TitleScreen(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.screen = self.game.screen 
        self.clock = pygame.time.Clock()

        # Define music
        pygame.mixer.init()
        tts_music = 'data/music/menu_screen.wav'
        pygame.mixer.music.load(tts_music)

        # Define fonts
        self.font = pygame.font.Font(FONT1, 80)
        self.font1 = pygame.font.Font(FONT2, 80)
        self.font2 = pygame.font.Font(FONT3, 80)
        self.font3 = pygame.font.Font(FONT4, 80)
        self.font4 = pygame.font.Font(FONT5, 80)


    def draw_button(self, x, y, width, height, text, text_colour, font, hover_colour=None):
        button_rect = pygame.Rect(x, y, width, height)

        # Check if the mouse is over the button
        is_hovered = button_rect.collidepoint(pygame.mouse.get_pos())

        button_text = font.render(text, True, text_colour)

        # Adjust font size based on the hover state
        if is_hovered:
            font_size = 40  # Increased font size when hovered
        else:
            font_size = 36

        button_text = pygame.font.Font.render(font, text, True, text_colour)
        button_text = pygame.transform.scale(button_text, (width, height))

        # Center the text on the button
        text_rect = button_text.get_rect(center=button_rect.center)

        self.screen.blit(button_text, text_rect.topleft)

        # Draw the arrows when hovered or clicked
        if is_hovered:
            pygame.draw.polygon(self.screen, WHITE, [(x-20, y+height/2), (x, y+height/2+20), (x, y+height/2-20)])  # Left arrow
            pygame.draw.polygon(self.screen, WHITE, [(x+width+20, y+height/2), (x+width, y+height/2+20), (x+width, y+height/2-20)])  # Right arrow

        return button_rect

    def stop_music(self):
        pygame.mixer.music.stop()

    def update(self, events):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse click is on the "Play" button
                if self.play_button.collidepoint(event.pos):
                    # Add code here to change game state
                    self.stop_music()
                    self.game.state_manager.change_state("loading_screen")

                # Check if the mouse click is on the "Information" button 
                elif self.info_button.collidepoint(event.pos): 
                    print('information')
                    self.game.state_manager.change_state("information_screen")
                # Check if the mouse click is on the "Options" button 
                elif self.options_button.collidepoint(event.pos):
                    print('options')
                    self.game.state_manager.change_state("options_screen")
                # Check if the mouse click is on the "Quit" button
                elif self.quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            
            
        # Define the main background 
        title_screen_bg = pygame.image.load(BACKGROUND_PATH + 'titlescreen.png')
        title_screen_bg = pygame.transform.scale(title_screen_bg, (WIDTH, HEIGHT))

        # Clear Screen
        self.screen.fill((0, 0, 0))
        # Draw the title and buttons
        # tmbg = title menu background
        self.screen.blit(title_screen_bg, (0, 0))

        # DRAW GAME TITLE 
        title_screen_text = pygame.image.load(BACKGROUND_PATH + 'title_txt.png').convert_alpha()
        title_screen_text = pygame.transform.scale(title_screen_text, (700, 700))
        self.screen.blit(title_screen_text, (0, 0))
        # Draw play button
        self.play_button = self.draw_button(WIDTH - 300, 200, 200, 100, "PLAY", WHITE, self.font3, hover_colour=GRAY)

        # Draw information button 
        self.info_button = self.draw_button(WIDTH - 350, 350, 300, 100, "INFORMATION", WHITE, self.font3, hover_colour=GRAY)

        # Draw options button 
        self.options_button = self.draw_button(WIDTH - 350, 500, 300, 100, "OPTIONS", WHITE, self.font3, hover_colour=GRAY)

        # Draw quit button
        self.quit_button = self.draw_button(WIDTH - 300, 650, 200, 100, "QUIT", WHITE, self.font3, hover_colour=GRAY)

        pygame.display.flip()
        pygame.display.update()
        self.clock.tick(FPS)