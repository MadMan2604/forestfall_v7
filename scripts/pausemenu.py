import pygame, sys


from pm_buttons import PauseButton
from settings import *



# Initialize Pygame
pygame.init()



# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Create Button objects
buttons = {
    'resume': PauseButton(),
    'restart': PauseButton(),
    'options': PauseButton(),
    'quit': PauseButton()
}

# Define button positions
button_positions = {
    'resume': (100, 100),
    'restart': (100, 200),
    'options': (100, 300),
    'quit': (100, 400)
}

# Main game loop
running = True
while running:
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        

    # Update and draw each button
    mouse_pos = pygame.mouse.get_pos()
    screen.fill((29, 30, 60))
    for button_name, button in buttons.items():
        button_rect = pygame.Rect(button_positions[button_name], (200, 50))  # Replace with the actual button size
        button.update(button_name, mouse_pos, button_rect)
        button.draw(screen, button_name, button_positions[button_name])

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
