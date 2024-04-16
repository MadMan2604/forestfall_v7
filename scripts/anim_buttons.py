# This is the script that will load an animated button from ay uploaded button animation file 
## the uploaded folder must contain the button animation frames (any number of frames other than one) 
## the script will play the animation frames when the button is hovered and/or clicked on and will play the frames until the last one and pause there. 
## when the button is no longer hovered and/or clicked on, the animation frames will return to the base frame (0)
import pygame 
import sys 
import os 
import math

from settings import * 

# button class 
class AnimButton(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, file_path):
        self.pos_x = x 
        self.pos_y = y 
        self.width = width
        self.height = height
        self.img_path = file_path
        self.images = [pygame.image.load(os.path.join(file_path, f)) for f in os.listdir(file_path) if f.endswith('.png')]
        self.current_image = 0 
        self.rect = pygame.Rect(x, y, width, height)
        self.hovering = False 
        self.playing = False
    
    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.hovering = True 
                    self.playing = True 
                else: 
                    self.hovering = False
                    self.playing = False
                    self.current_image = len(self.images) - 1 
        
        if self.playing:
            self.current_image += 1
            if self.current_image >= len(self.images):
                self.current_image = 0 
    
    def draw(self, screen):
        screen.blit(self.images[self.current_image], (self.pos_x, self.pos_y))