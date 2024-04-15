import pygame
import sys 

from pygame import image
from pygame.locals import *
from scripts.settings import *

class PauseButton:
    def __init__(self):
        self.button_frames = {
            'resume': [f'data/images/buttons/pausemenu/resume/resume_{str(i).zfill(2)}.png' for i in range(0, 23)],
            'restart': [f'data/images/buttons/pausemenu/restart/restart_{str(i).zfill(2)}.png' for i in range(0, 23)],
            'options': [f'data/images/buttons/pausemenu/options/options_{str(i).zfill(2)}.png' for i in range(0, 23)],
            'quit': [f'data/images/buttons/pausemenu/quit/quit_{str(i).zfill(2)}.png' for i in range(0, 23)]
        }
        self.hovering = {button: False for button in self.button_frames}
        self.current_frame = {button: 0 for button in self.button_frames}
        self.mouse_click = False
        self.load_images()

    def load_images(self, scale_factor=3):
        self.images = {button: [pygame.transform.scale(pygame.image.load(frame), (int(pygame.image.load(frame).get_width() * scale_factor), int(pygame.image.load(frame).get_height() * scale_factor))) for frame in frames] for button, frames in self.button_frames.items()}

    def draw(self, screen, button_name, position):
        screen.blit(self.images[button_name][self.current_frame[button_name]], position)

    def update(self, button_name, mouse_pos, button_rect):
        if button_rect.collidepoint(mouse_pos):
            if not self.hovering[button_name]:
                self.hovering[button_name] = True
                self.current_frame[button_name] = 0
            else:
                if self.current_frame[button_name] < len(self.images[button_name]) - 1:
                    self.current_frame[button_name] += 1
                # Check for mouse button down event
                if pygame.mouse.get_pressed()[0]:  # Left mouse button
                    print(f'{button_name} button clicked!')
        else:
            if self.hovering[button_name]:
                self.hovering[button_name] = False
                self.current_frame[button_name] = 0
            else:
                if self.current_frame[button_name] > 0:
                    self.current_frame[button_name] -= 1

