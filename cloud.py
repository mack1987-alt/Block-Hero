"""
cloud.py
Cloud Class: The Silent Drifter of the Game Sky

Attributes:
- self.rect (pygame.Rect): The ethereal rectangular presence of the cloud in the game world.

Constants:
- CLOUD_SPEED (int): The mystical speed at which clouds traverse the sky.
- WHITE (tuple): The color of the clouds, as pure as a fresh layer of snow.

Methods:
- __init__(self, x, y, width, height): Initiates the cloud, bringing a touch of the sky to the game.
- update(self, scroll): Adjusts the cloud's state, drifting along with the breeze, just like life.
- draw(self, screen, scroll): Draws the cloud on the screen, a white puff in the vast canvas of the game world.

Note: May the clouds of your code always bring a serene ambiance to your gaming experience.
"""

import pygame
from constants import CLOUD_SPEED, WHITE

class Cloud:
    def __init__(self, x, y, width, height):
        # Initiating a cloud, 'cause every game needs a touch of the sky, eh?
        self.rect = pygame.Rect(x, y, width, height)

    def update(self, scroll):
        # Adjusting the cloud state, drifting along with the breeze, just like life
        self.rect.x -= CLOUD_SPEED

    def draw(self, screen, scroll):
        # Drawing the cloud on the screen, a white puff in the vast canvas of the game world
        pygame.draw.rect(screen, WHITE, (self.rect.x - scroll, self.rect.y, self.rect.width, self.rect.height))
