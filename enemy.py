import pygame  # Bringing in the essentials, like a trusty hockey stick for the game.
import random

# Importing the RED color constant from the constants module, because we all know red is a classic Canadian color.
from constants import RED, ENEMY_ATTACK_DAMAGE, ENEEMY_SPEED
from player import Player

class Enemy:
    def __init__(self, x, ground_height, size, speed, attack_damage=ENEMY_ATTACK_DAMAGE):
        # Initializing the enemy with a stompin' ground rectangle, a starting position, and a swift speed.
        self.rect = pygame.Rect(x, ground_height - size, size, size)  
        self.speed = ENEEMY_SPEED  # The speed of our foe, as swift as a beaver's tail slap.
        self.attack_damage = attack_damage  # The damage the enemy inflicts upon collision.
        self.red = RED  # Setting the color of the enemy to the classic Canadian red.
        #print("Enemy initialized.")  # A friendly comment, the enemy's ready for the digital showdown, eh!

    def update(self, player_x, enemies, screen_width, player):
        # Updating the enemy's state based on the player's position, stalkin' like a sly fox in the woods.
        if self.rect.x > player_x:
            self.rect.x -= self.speed
        elif self.rect.x < player_x:
            self.rect.x += self.speed

        # Preventing enemies from overlapping, respecting personal space, just like Canadians in a queue.
        for other_enemy in enemies:
            if other_enemy != self and self.rect.colliderect(other_enemy.rect):
                if self.rect.x < other_enemy.rect.x:
                    self.rect.x -= 1
                else:
                    self.rect.x += 1

        # Checking if the enemy is on-screen before moving, no sense in wastin' energy off-camera.
        if 0 <= self.rect.x <= screen_width:
            # Randomly deciding whether to move left or right, adding a bit of unpredictability like a wild goose chase.
            move_direction = random.choice([-1, 1])
            self.rect.x += move_direction * self.speed

        # Check for collision with the player and deduct health
        if self.rect.colliderect(player.rect):
            print("Player is under attack! ")
            player.health -= self.attack_damage
            print(f"Player health: {player.health}")

    def draw(self, screen, scroll):
        # Adjusting the drawing position for the grand entrance, ready to face off against the player.
        enemy_draw_x = self.rect.x - scroll  
        # Drawing the enemy as a circle, 'cause in the digital wilderness, geometry is the way to go, bud.
        pygame.draw.circle(screen, self.red, (int(enemy_draw_x + self.rect.width // 2), int(self.rect.y + self.rect.height // 2)), self.rect.width // 2)
