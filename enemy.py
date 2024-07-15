import pygame
import random
from constants import RED, ENEMY_ATTACK_DAMAGE, ENEMY_SPEED

class Enemy:
    def __init__(self, spawn_x, ground_height, size, speed, attack_damage=ENEMY_ATTACK_DAMAGE):
        self.spawn_x = spawn_x
        self.rect = pygame.Rect(spawn_x, ground_height - size, size, size)
        self.speed = ENEMY_SPEED
        self.attack_damage = attack_damage
        self.red = RED
        self.active = False
        self.activation_distance = 500  # Distance at which the enemy becomes active
        self.return_distance = 1000  # Distance at which the enemy returns to spawn point

    def update(self, player_x, enemies, screen_width, player):
        distance_to_player = abs(self.rect.x - player_x)

        if not self.active and distance_to_player <= self.activation_distance:
            self.active = True

        if self.active:
            if distance_to_player <= self.return_distance:
                if self.rect.x > player_x:
                    self.rect.x -= self.speed
                elif self.rect.x < player_x:
                    self.rect.x += self.speed
            else:
                # Return to spawn point
                if abs(self.rect.x - self.spawn_x) > self.speed:
                    if self.rect.x > self.spawn_x:
                        self.rect.x -= self.speed
                    else:
                        self.rect.x += self.speed
                else:
                    self.rect.x = self.spawn_x
                    self.active = False

            # Prevent overlapping with other enemies
            for other_enemy in enemies:
                if other_enemy != self and self.rect.colliderect(other_enemy.rect):
                    if self.rect.x < other_enemy.rect.x:
                        self.rect.x -= 1
                    else:
                        self.rect.x += 1

            # Check for collision with the player and deduct health
            if self.rect.colliderect(player.rect):
                print("Player is under attack!")
                player.health -= self.attack_damage
                print(f"Player health: {player.health}")

    def draw(self, screen, scroll):
        enemy_draw_x = self.rect.x - scroll
        pygame.draw.circle(screen, self.red, (int(enemy_draw_x + self.rect.width // 2), int(self.rect.y + self.rect.height // 2)), self.rect.width // 2)

def generate_enemies(num_enemies, ground_height, size, player_start_x, level_width):
    enemies = []
    min_distance = 1000  # Minimum distance from player start
    max_distance = level_width - 1000  # Maximum distance from level end

    for _ in range(num_enemies):
        spawn_x = random.randint(player_start_x + min_distance, max_distance)
        enemy = Enemy(spawn_x, ground_height, size, ENEMY_SPEED)
        enemies.append(enemy)

    return enemies