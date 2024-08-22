import pygame
import sys
import random
from constants import *
from player import Player
from enemy import Enemy
from cloud import Cloud
from debug import Debug

class Game:
    def __init__(self):
        pygame.init()
        debug = Debug()

        print("Initializing window...")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Block-Hero")
        
        print("Initializing levels...")
        self.levels = [
            {"background": "/media/mcbuntu/mcbig/git/Block-Hero/level1_bg.png", "enemies": NUM_LVL1_ENEMIES, "clouds": NUM_LVL1_CLOUDS},
            {"background": "/media/mcbuntu/mcbig/git/Block-Hero/level2_bg.png", "enemies": NUM_LVL2_ENEMIES, "clouds": NUM_LVL2_CLOUDS},
            #{"background": "level3_bg.png", "enemies": NUM_LVL3_ENEMIES, "clouds": NUM_LVL3_CLOUDS},
            #{"background": "level4_bg.png", "enemies": NUM_LVL4_ENEMIES, "clouds": NUM_LVL4_CLOUDS},
            #{"background": "level5_bg.png", "enemies": NUM_LVL5_ENEMIES, "clouds": NUM_LVL5_CLOUDS},
        ]

        self.current_level = 0
        print("Initializing level...")
        self.load_level(self.current_level)

        print("Initializing menu resources...")
        self.menu_background = pygame.image.load("/media/mcbuntu/mcbig/git/Block-Hero/menu_bg2.png")
        self.menu_background = pygame.transform.scale(self.menu_background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        print("Initializing time...")
        self.clock = pygame.time.Clock()
        print("Clock loaded.")

        print("Initializing gravity...")
        self.gravity = 1
        print("Initializing scroll...")
        self.scroll = 0
        
        print("Loading...")
        self.game_active = True
        self.paused = False
        debug.pause_and_clear()

    def load_level(self, level_index):
        level = self.levels[level_index]
        self.background = pygame.image.load(level["background"])
        self.background = pygame.transform.scale(self.background, (MAP_WIDTH, WINDOW_HEIGHT))  # Resize to match level width and window WINDOW_HEIGHT
        print("Background loaded.")

        print("Loading game entities...")
        self.player = Player(20, GROUND_HEIGHT, (30, 80))
        self.player_health_font = pygame.font.Font(None, 24)
        self.enemies = [Enemy(random.randint(WINDOW_WIDTH, DEFAULT_ENEMY_SPAWN_WIDTH), DEFAULT_ENEMY_SPAWN_HEIGHT, ENEMY_SIZE, ENEMY_SPEED) for _ in range(level["enemies"])]
        self.clouds = [Cloud(random.randint(WINDOW_WIDTH, WINDOW_WIDTH + MAP_WIDTH), random.randint(50, 200), random.randint(30, 80), random.randint(20, 60)) for _ in range(level["clouds"])]
        print("Entities defined...")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting...")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print(f"Mouse coordinates: ({mouse_x}, {mouse_y})")
                
                if WINDOW_WIDTH - 40 <= mouse_x <= WINDOW_WIDTH - 20 and 20 <= mouse_y <= 60:  # Update the collision detection for the pause button
                    if not self.paused:
                        self.paused = True
                        self.show_pause_menu()
                        print("Paused.")
                    else:
                        self.paused = False
                        print("Resume.")

    def show_pause_menu(self):
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Check if the mouse click is on the "Resume" button
                    resume_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2, 100, 50)
                    if resume_button_rect.collidepoint(mouse_x, mouse_y):
                        # Resume the game when clicking the "Resume" button
                        self.paused = False
                        print("Resume.")
                    main_menu_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 + 60, 100, 50)
                    if main_menu_button_rect.collidepoint(mouse_x, mouse_y):
                        self.paused = False
                        print("Returning to menu...")
                        self.reset_game_state()
                        self.show_menu()  # This will display the main menu and handle user input
                        
            # Draw the pause menu
            self.screen.fill((0, 0, 0))  # Fill the screen with black
            resume_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2, 100, 50)
            main_menu_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 + 60, 100, 50)

            pygame.draw.rect(self.screen, GREEN, resume_button_rect)
            pygame.draw.rect(self.screen, RED, main_menu_button_rect)

            resume_text = self.player_health_font.render("Resume", True, WHITE)
            main_menu_text = self.player_health_font.render("Main Menu", True, WHITE)

            self.screen.blit(resume_text, (WINDOW_WIDTH // 2 - resume_text.get_width() // 2, WINDOW_HEIGHT // 2 + 10))
            self.screen.blit(main_menu_text, (WINDOW_WIDTH // 2 - main_menu_text.get_width() // 2, WINDOW_HEIGHT // 2 + 70))

            pygame.display.flip()

    def update_entities(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.gravity)

        # Check for collision with enemies
        for enemy in self.enemies:
            enemy.update(self.player.rect.x, self.enemies, WINDOW_WIDTH, self.player)
        # Updating the state of each cloud based on the current scroll position.
        for cloud in self.clouds:
            cloud.update(self.scroll)

        # Check if the player has reached the end of the level
        if self.player.rect.x >= 3900:  # Assuming 3900 is the end of the level
            self.current_level += 1
            if self.current_level < len(self.levels):
                self.load_level(self.current_level)
                self.player.rect.x = 20  # Reset player position to the far left
            else:
                print("Congratulations! You've completed all levels!")
                self.game_active = False

    def draw_entities(self):
        # Clear the screen
        self.screen.fill((0, 0, 0))

        # Draw the grand sky background
        self.screen.blit(self.background, (0 - self.scroll, 0))

        # Draw the ground rectangle based on the current scroll position
        #pygame.draw.rect(self.screen, DARK_GREEN, (0 - self.scroll, GROUND_HEIGHT, MAP_WIDTH, WINDOW_HEIGHT - GROUND_HEIGHT))

        # Draw the player and his shadow
        self.player.draw(self.screen, self.scroll)
        self.player.draw_shadow(self.screen, self.scroll)

        # Draw the enemies
        for enemy in self.enemies:
            enemy.draw(self.screen, self.scroll)

        # Draw the clouds
        for cloud in self.clouds:
            cloud.draw(self.screen, self.scroll)

        # Show the player health UI bar at the bottom
        # ui_bar_rect = pygame.Rect(10, GROUND_HEIGHT + 10, self.player.health * 2, 20)
        # Show the player health UI bar at the top
        ui_bar_rect = pygame.Rect(10, 30, self.player.health * 2, 20)

        pygame.draw.rect(self.screen, RED, ui_bar_rect)
        
        health_text = self.player_health_font.render(f"Health: {self.player.health}%", True, WHITE)
        # Show the health gauge text at the bottom
        # self.screen.blit(health_text, (ui_bar_rect.right + 10, GROUND_HEIGHT + 10))
        # Show the health gauge text at the top
        self.screen.blit(health_text, (ui_bar_rect.right + 10, 30))

        # Draw the pause/settings button at the bottom
        # pause_button_rect = pygame.Rect(WINDOW_WIDTH - 40, GROUND_HEIGHT + 10, 30, 30)
        # Draw the pause/settings button at the top
        pause_button_rect = pygame.Rect(WINDOW_WIDTH - 40, 30, 30, 30)
        pygame.draw.rect(self.screen, BLACK, pause_button_rect)

        # Draw the pause symbol (two white bars) at the bottom
        # pygame.draw.rect(self.screen, WHITE, (WINDOW_WIDTH - PAUSE_SYMBOL_X-10, GROUND_HEIGHT + PAUSE_SYMBOL_Y, 5, 15))
        # pygame.draw.rect(self.screen, WHITE, (WINDOW_WIDTH - PAUSE_SYMBOL_X + 2, GROUND_HEIGHT + PAUSE_SYMBOL_Y, 5, 15))
        # Draw the pause symbol (two white bars) at the top
        pygame.draw.rect(self.screen, WHITE, (WINDOW_WIDTH - PAUSE_SYMBOL_X-10, 20 + PAUSE_SYMBOL_Y, 5, 15))
        pygame.draw.rect(self.screen, WHITE, (WINDOW_WIDTH - PAUSE_SYMBOL_X + 2, 20 + PAUSE_SYMBOL_Y, 5, 15))

        pygame.display.flip()

    def reset_game_state(self):
        self.current_level = 0  # Change this from 1 to 0
        self.load_level(self.current_level)
        self.player.rect.x = 20
        self.player.health = 100
        # Reset the enemy positions
        for enemy in self.enemies:
            enemy.rect.x = random.randint(WINDOW_WIDTH, WINDOW_WIDTH + 500)
        self.scroll = 0

    def new_game(self):
        self.reset_game_state()


    def run(self):
        debug = Debug()
        game_active = True

        while game_active:
            self.handle_events()
            self.update_entities()
            self.draw_entities()
            # Calculate scroll after updating entities
            self.scroll = max(min(self.player.rect.x - WINDOW_WIDTH // 2, MAP_WIDTH - WINDOW_WIDTH), 0)

            # Cap the frame rate
            self.clock.tick(FPS)

            # Check if player lost
            # print(f"Player health: {self.player.health}")
            if self.player.health <= 0:
                game_active = False  # Game over, buddy! Exit the loop
                debug.pause_and_clear()

        # Display game over
        play_again = self.show_game_over_screen()
        if play_again == 1:
            # Player chose to play again, reset the game
            print("Play again...")
            # debug.pause_and_clear()
            self.reset_game()
        elif play_again == 2:
            # Player chose to quit
            print("Quitting...")
            pygame.quit()
            sys.exit()

    # Update the show_game_over_screen method
    def show_game_over_screen(self):
        print("Game over...")
        game_over_font = pygame.font.Font(None, 72)
        text = game_over_font.render("You Lost...", True, RED)

        # Create a surface for the game over screen
        game_over_screen = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        game_over_screen.fill((0, 0, 0))  # Fill the screen with black
        game_over_screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_WINDOW_HEIGHT() // 2))

        # Display the game over screen on top of the main screen
        self.screen.blit(game_over_screen, (0, 0))
        pygame.display.flip()

        # Pause for 3000 milliseconds (3 seconds)
        pygame.time.delay(3000)

        # Update the display before waiting for player input
        pygame.display.flip()

        # Wait for player input
        return self.main_menu()

    def main_menu(self):
        debug = Debug()
        while True:
            # Draw the background image
            self.screen.blit(self.menu_background, (0, 0))

            play_rect = pygame.Rect(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 - 50, 100, 50)
            quit_rect = pygame.Rect(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 + 50, 100, 50)

            pygame.draw.rect(self.screen, GREEN, play_rect)
            pygame.draw.rect(self.screen, RED, quit_rect)
  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting...")
                    debug.pause_and_clear()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if play_rect.collidepoint(mouse_x, mouse_y):
                        self.new_game()  # Reset the game state
                        return 1  # Return 1 for Play
                    elif quit_rect.collidepoint(mouse_x, mouse_y):
                        debug.pause_and_clear()
                        self.quit_game()
                        return 2  # Return 2 for Quit

            menu_font = pygame.font.Font(None, 36)
            play_text = menu_font.render("Play", True, WHITE)
            quit_text = menu_font.render("Quit", True, WHITE)
            self.screen.blit(play_text, (WINDOW_WIDTH // 2 - 25, WINDOW_HEIGHT // 2 - 40))
            self.screen.blit(quit_text, (WINDOW_WIDTH // 2 - 25, WINDOW_HEIGHT // 2 + 60))
            pygame.display.flip()

    def show_menu(self):
        debug = Debug()
        print("Main menu...")
        debug.pause_and_clear()
        return self.main_menu()
    
    def quit_game(self):
        print("Quitting the game. Farewell, brave adventurer!")
        pygame.quit()
        sys.exit()