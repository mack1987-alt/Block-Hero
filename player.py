import pygame
from constants import GREEN, SHADOW_COLOR
from constants import GROUND_HEIGHT, SHADOW_OFFSET

class Player:
    def __init__(self, x, ground_height, size):
        # Initialize the player slightly below the ground height
        self.rect = pygame.Rect(x, ground_height - size[1] + 30, size[0], size[1])
        self.y_speed = 0
        self.jumping = False
        self.health = 100
        self.max_health = 100
        self.green = GREEN
        self.shadow_color = SHADOW_COLOR
        self.ground_height = ground_height
        print("Player initialized...")

    def update(self, keys, gravity):
        # print("Player position:", self.rect.x, self.rect.y)
        current_x = self.rect.x

        if keys[pygame.K_LEFT]:
            self.rect.x = max(self.rect.x - 5, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.x = min(self.rect.x + 5, 4000 - self.rect.width)
        
        # if current_x != self.rect.x:
    

        # Adjust jump condition to account for new ground position
        if keys[pygame.K_SPACE] and not self.jumping and self.rect.bottom == self.ground_height + 30:
            self.y_speed = -15
            self.jumping = True

        self.y_speed += gravity
        self.rect.y += self.y_speed

        # Adjust ground collision to account for new ground position
        if self.rect.y > self.ground_height - self.rect.height + 30:
            self.rect.y = self.ground_height - self.rect.height + 30
            self.y_speed = 0
            self.jumping = False

        self.health = max(0, min(self.max_health, self.health))

    def draw(self, screen, scroll):
        player_draw_x = self.rect.x - scroll
        pygame.draw.rect(screen, self.green, (player_draw_x, self.rect.y, self.rect.width, self.rect.height))

    def draw_shadow(self, screen, scroll):
        if self.jumping:
            player_shadow_rect = pygame.Rect(self.rect.x - scroll, GROUND_HEIGHT + SHADOW_OFFSET, self.rect.width, 10)
            pygame.draw.rect(screen, self.shadow_color, player_shadow_rect)