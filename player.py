"""
player.py
The Player class, eh!

This class represents the main player character in our little digital escapade. A true legend, it can move left or right with the arrow keys, jumping into the great unknown with the space bar. Always mindful of its health, this player is as resilient as a Canadian beaver dam in a storm.

Attributes:
- self.rect (pygame.Rect): The player's rectangular presence, solid as a double-double coffee.
- self.y_speed (int): The player's vertical speed, eh? Positive when falling, negative when jumping.
- self.jumping (bool): A flag indicating whether the player is airborne, just like a hockey puck in play.
- self.health (int): The player's health, starting at a robust 100%. Don't let it drop too low, or it's sorry time, bud.
- self.max_health (int): The player's maximum health, an unyielding fortress against the slings and arrows of digital misfortune.
- self.green (tuple): The color of the player, as Canadian as a fresh blanket of snow.
- self.shadow_color (tuple): The color of the player's shadow, a subtle reminder of its presence in the digital wilderness.
- self.ground_height (int): The height of the virtual ground, a solid foundation like a good pair of snowshoes.

Methods:
- update(keys, gravity): Updates the player's state based on keyboard input and gravitational forces, navigating the digital landscape with grace.
- draw(screen, scroll): Draws the player's rectangular prowess on the screen, a visual feast for the eyes.
- draw_shadow(screen, scroll): Draws the player's shadow when in mid-air, as ephemeral as a ghost's whisper.

Remember, this player is ready for a proper go, always prepared to face the challenges of the great digital outdoors, just like a Canadian facing the winter chill, eh!
"""

import pygame
from constants import GREEN, SHADOW_COLOR
from constants import GROUND_HEIGHT, SHADOW_OFFSET

class Player:
    def __init__(self, x, ground_height, size):
        # The player's rect, a rectangle as solid as a pint glass
        self.rect = pygame.Rect(x, ground_height - size[1], size[0], size[1])
        self.y_speed = 0
        self.jumping = False
        self.health = 100  # Initial health value, as sturdy as a barn in a storm
        self.max_health = 100  # Maximum health value, like a fence that won't budge
        self.green = GREEN
        self.shadow_color = SHADOW_COLOR
        self.ground_height = ground_height
        print("Player initialized, ready for a proper go, eh!")

    def update(self, keys, gravity):
        print("Player position:", self.rect.x, self.rect.y)
        # Save the current position for comparison, keepin' an eye on things
        current_x = self.rect.x

        # Update player state based on keys, navigatin' like a sailor through the keys
        if keys[pygame.K_LEFT]:
            self.rect.x = max(self.rect.x - 5, 0)  # Movin' left, like a traveler on the open road
        if keys[pygame.K_RIGHT]:
            self.rect.x = min(self.rect.x + 5, 4000 - self.rect.width)  # Movin' right, steady as a compass
        
        # If the position has changed, player is moving, sure and steady
        if current_x != self.rect.x:
            print("Player is moving, makin' strides like a champ")

        if keys[pygame.K_SPACE] and not self.jumping and self.rect.bottom == GROUND_HEIGHT:
            self.y_speed = -15
            self.jumping = True

        # Apply gravity, pullin' down like a solid pint on a Friday night
        self.y_speed += gravity
        self.rect.y += self.y_speed

        # Check for collision with the ground, landin' as gracefully as a dancer
        if self.rect.y > self.ground_height - self.rect.height:
            self.rect.y = self.ground_height - self.rect.height
            self.y_speed = 0
            self.jumping = False

        # Update health gauge, no need to go too low or too high
        self.health = max(0, self.health)
        self.health = min(self.max_health, self.health)

    def draw(self, screen, scroll):
        # Draw the player's rectangular prowess on the screen, a visual feast for the eyes
        player_draw_x = self.rect.x - scroll
        pygame.draw.rect(screen, self.green, (player_draw_x, self.rect.y, self.rect.width, self.rect.height))

    def draw_shadow(self, screen, scroll):
        # If the player is in mid-air, cast a shadow, as ephemeral as a ghost's whisper
        if self.jumping:
            player_shadow_rect = pygame.Rect(self.rect.x - scroll, GROUND_HEIGHT + SHADOW_OFFSET, self.rect.width, 10)
            pygame.draw.rect(screen, self.shadow_color, player_shadow_rect)
