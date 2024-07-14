"""
    A class representing the tumultuous life of a scrolling side-scrolling game in the enchanting world of Pygame.

    Attributes:
    - screen (pygame.Surface): The magical canvas where the game unfolds, fit for a tale of adventure and mishaps.
    - background (pygame.Surface): The mystical background image setting the tone for the epic journey.
    - clock (pygame.time.Clock): The timekeeper ensuring the proper rhythm of the game, like a fiddler at a ceilidh.
    - player (Player): The resilient protagonist, navigating the treacherous landscape with boundless determination.
    - player_health_font (pygame.font.Font): The font used to inscribe the player's health, as important as a weathered map.
    - enemies (list): A mischievous band of antagonists, ready to challenge the player's mettle with unpredictable antics.
    - clouds (list): Wispy entities floating above, adding an ethereal touch to the scenic beauty of the game world.
    - gravity (int): The force that pulls entities downward, as inevitable as a spilled pint on a pub floor.
    - scroll (int): The positional marker, guiding the viewport through the vast expanse of the game world.
    - game_active (bool): Flag indicating whether the game is currently active or paused.
    - paused (bool): Flag indicating whether the game is currently paused.

    Constants:
    - MAX_WIDTH (int): The maximum width of the game window, a boundary as firm as a country fence.
    - HEIGHT (int): The height of the game window, reaching for the stars like a hopeful dream.
    - FPS (int): The frames per second, setting the pace of the adventure with the precision of a dance instructor.
    - PLAYER_SIZE (int): The size of the player, a formidable presence in the world, akin to a mighty oak.
    - ENEMY_SIZE (int): The size of enemies, each a mischievous imp posing a unique threat.

    Methods:
    - handle_events(): Keeps a vigilant eye on the realm of events, ensuring a graceful exit if the window must close.
    - update_entities(): Guides the entities through the ever-changing landscape, confronting collisions and challenges.
    - draw_entities(): Paints a vivid tableau on the screen, capturing the essence of the game world like a masterful artist.
    - show_game_over_screen(): Unveils a poignant scene of defeat, allowing a brief pause for reflection before the next adventure.
    - reset_game(): Restores the game to its initial state, giving the player a chance to redeem themselves and try again.
    - run(): Orchestrates the grand symphony of the game, balancing events and updates with the finesse of a seasoned conductor.
    - show_menu(): Invites players to embark on the journey anew or bid a temporary farewell, with options as clear as a crisp morning in the countryside.
    - quit_game(): Gracefully exits the game, bidding farewell to the brave adventurer.

    """

import pygame
import sys
import random
from constants import GREEN, WHITE, BLACK, DARK_GREEN, RED, LIGHT_BLUE, SHADOW_COLOR, GROUND_HEIGHT, MAX_WIDTH, HEIGHT, FPS, PAUSE_SYMBOL_X, PAUSE_SYMBOL_Y, PLAYER_SIZE, ENEMY_SIZE
from player import Player
from enemy import Enemy
from cloud import Cloud
from debug import Debug

class Game:
    def __init__(self):
        pygame.init()
        debug = Debug()
        print("Pitter-patter...")

        # Create the window, look at you with your big city ways
        self.screen = pygame.display.set_mode((MAX_WIDTH, HEIGHT))
        pygame.display.set_caption("Scrolling Side-Scrolling Game")
        print("Let's get at 'er!")

        # Load the background image, not so bad now
        self.background = pygame.image.load("menu_bg.png") 
        print("Background loaded.")

        # Clock to control the frame rate, keepin' time like a proper Irish dancer
        self.clock = pygame.time.Clock()
        print("Clock loaded.")

        # Create the feckin' game entities, right proper
        print("Loading game entities...")
        self.player = Player(20, GROUND_HEIGHT, (30, 80))
        self.player_health_font = pygame.font.Font(None, 24)
        self.enemies = [Enemy(random.randint(MAX_WIDTH, MAX_WIDTH + 500), GROUND_HEIGHT, ENEMY_SIZE, 2) for _ in range(5)]
        self.clouds = [Cloud(random.randint(MAX_WIDTH, MAX_WIDTH + 4000), random.randint(50, 200), random.randint(30, 80), random.randint(20, 60)) for _ in range(10)]
        print("Entities defined...")

        # Gravity, sure it's pullin' things down like a pint on a Friday
        self.gravity = 1  # Initialize gravity here
        self.scroll = 0  # Initialize scroll here
        print("gravity invented.")
        print("Loading...")
        
        self.game_active = True
        self.paused = False

        debug.pause_and_clear()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Game>handle_events>pygame quit.")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if MAX_WIDTH - 40 <= mouse_x <= MAX_WIDTH - 10 and GROUND_HEIGHT + 10 <= mouse_y <= GROUND_HEIGHT + 40:
                    if not self.paused:
                        # Pause the game when clicking the pause/settings button
                        self.paused = True
                        self.show_pause_menu()
                    else:
                        # Resume the game when clicking the button on the pause menu
                        self.paused = False
    
    def show_pause_menu(self):
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Game>show_pause_menu>pygame quit.")
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Check if the mouse click is on the "Resume" button
                    resume_button_rect = pygame.Rect(MAX_WIDTH // 2 - 50, HEIGHT // 2, 100, 50)
                    if resume_button_rect.collidepoint(mouse_x, mouse_y):
                        # Resume the game when clicking the "Resume" button
                        self.paused = False
                    # Check if the mouse click is on the "Main Menu" button
                    main_menu_button_rect = pygame.Rect(MAX_WIDTH // 2 - 50, HEIGHT // 2 + 60, 100, 50)
                    if main_menu_button_rect.collidepoint(mouse_x, mouse_y):
                        # Return to the main menu when clicking the "Main Menu" button
                        self.paused = False
                        self.show_menu()  # This will display the main menu and handle user input

            # Draw the pause menu
            self.screen.fill((0, 0, 0))  # Fill the screen with black
            resume_button_rect = pygame.Rect(MAX_WIDTH // 2 - 50, HEIGHT // 2, 100, 50)
            main_menu_button_rect = pygame.Rect(MAX_WIDTH // 2 - 50, HEIGHT // 2 + 60, 100, 50)

            pygame.draw.rect(self.screen, GREEN, resume_button_rect)
            pygame.draw.rect(self.screen, RED, main_menu_button_rect)

            resume_text = self.player_health_font.render("Resume", True, WHITE)
            main_menu_text = self.player_health_font.render("Main Menu", True, WHITE)

            self.screen.blit(resume_text, (MAX_WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2 + 10))
            self.screen.blit(main_menu_text, (MAX_WIDTH // 2 - main_menu_text.get_width() // 2, HEIGHT // 2 + 70))

            pygame.display.flip()

    def update_entities(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.gravity)

        # Check for collision with gobshite enemies
        for enemy in self.enemies:
            enemy.update(self.player.rect.x, self.enemies, MAX_WIDTH, self.player)
        # Updating the state of each cloud based on the current scroll position.
        for cloud in self.clouds:
            cloud.update(self.scroll)

    def draw_entities(self):
        # Draw the grand sky background
        pygame.draw.rect(self.screen, LIGHT_BLUE, (0 - self.scroll, 0, 4000, GROUND_HEIGHT))

        # Draw the ground rectangle based on the current scroll position
        pygame.draw.rect(self.screen, DARK_GREEN, (0 - self.scroll, GROUND_HEIGHT, 4000, HEIGHT - GROUND_HEIGHT))

        # Draw the player and his shadow, 'cause he's a legend
        self.player.draw(self.screen, self.scroll)
        self.player.draw_shadow(self.screen, self.scroll)

        # Draw the gobshite enemies
        for enemy in self.enemies:
            enemy.draw(self.screen, self.scroll)

        # Draw the feckin' clouds
        for cloud in self.clouds:
            cloud.draw(self.screen, self.scroll)

        # Show the player health UI bar
        ui_bar_rect = pygame.Rect(10, GROUND_HEIGHT + 10, self.player.health * 2, 20)
        pygame.draw.rect(self.screen, RED, ui_bar_rect)

        # Show the health gauge text
        health_text = self.player_health_font.render(f"Health: {self.player.health}%", True, WHITE)
        self.screen.blit(health_text, (ui_bar_rect.right + 10, GROUND_HEIGHT + 10))

        # Draw the pause/settings button
        pause_button_rect = pygame.Rect(MAX_WIDTH - 40, GROUND_HEIGHT + 10, 30, 30)
        pygame.draw.rect(self.screen, BLACK, pause_button_rect)

        # Draw the pause symbol (two white bars)
        pygame.draw.rect(self.screen, WHITE, (MAX_WIDTH - PAUSE_SYMBOL_X-10, GROUND_HEIGHT + PAUSE_SYMBOL_Y, 5, 15))
        pygame.draw.rect(self.screen, WHITE, (MAX_WIDTH - PAUSE_SYMBOL_X + 2, GROUND_HEIGHT + PAUSE_SYMBOL_Y, 5, 15))

        pygame.display.flip()
    
    def reset_game(self):
        # Reset the player's position and health, sure and begorrah
        self.player.rect.x = 20
        self.player.health = 100

        # Reset the enemy positions, may the road rise to meet them
        for enemy in self.enemies:
            enemy.rect.x = random.randint(MAX_WIDTH, MAX_WIDTH + 500)

        # Reset the other game entities as needed, to be sure
        # No hard feelings, just a bit of the old reset

        # Reset the scroll position, top of the mornin' to ya
        self.scroll = 0

        # Resume the game, sure and it's back to active we go
        self.run()

    def new_game(self):
        # Reset the player's position and health, sure and begorrah
        self.player.rect.x = 20
        self.player.health = 100

        # Reset the enemy positions, may the road rise to meet them
        for enemy in self.enemies:
            enemy.rect.x = random.randint(MAX_WIDTH, MAX_WIDTH + 500)

        # Reset the other game entities as needed, to be sure
        # No hard feelings, just a bit of the old reset

        # Reset the scroll position, top of the mornin' to ya
        self.scroll = 0

    def run(self):
        debug = Debug()
        game_active = True  # Keeping 'er going, but watch out for trouble, eh?

        while game_active:
            self.handle_events()
            self.update_entities()
            self.draw_entities()

            # Calculate scroll after updating entities, make sure you're not too far ahead, now
            self.scroll = max(min(self.player.rect.x - MAX_WIDTH // 2, 4000 - MAX_WIDTH), 0)

            # Cap the frame rate, don't want things movin' too fast, ya know
            self.clock.tick(FPS)

            # Check if player lost, oh no, looks like trouble, eh?
            print(f"Player health: {self.player.health}")
            if self.player.health <= 0:
                game_active = False  # Game over, buddy! Exit the loop
                debug.pause_and_clear()

        # Time to face the music, display the game over screen and get player input
        play_again = self.show_game_over_screen()
        if play_again == 1:
            # Player chose to play again, reset the game
            print("reset_game")
            # debug.pause_and_clear()
            self.reset_game()
        elif play_again == 2:
            # Player chose to quit
            print("pygame quit")
            pygame.quit()
            sys.exit()

    # Update the show_game_over_screen method
    def show_game_over_screen(self):
        print("show game over...")
        game_over_font = pygame.font.Font(None, 72)
        text = game_over_font.render("You Lost...", True, RED)

        # Create a surface for the game over screen
        game_over_screen = pygame.Surface((MAX_WIDTH, HEIGHT))
        game_over_screen.fill((0, 0, 0))  # Fill the screen with black
        game_over_screen.blit(text, (MAX_WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        # Display the game over screen on top of the main screen
        self.screen.blit(game_over_screen, (0, 0))
        pygame.display.flip()

        # Pause for 3000 milliseconds (3 seconds) to show the game over screen, just to ponder life's challenges
        pygame.time.delay(3000)

        # Update the display before waiting for player input
        pygame.display.flip()

        # Wait for player input
        return self.main_menu()

    def main_menu(self):
        debug = Debug()
        while True:
            # Unleash the mystical symbols upon the pixel canvas!
            self.screen.blit(self.background, (0, 0))
            # Manifesting the ethereal buttons for players to interact with
            play_rect = pygame.Rect(MAX_WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 50)
            quit_rect = pygame.Rect(MAX_WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)

            # Drawing the sacred rectangles with vibrant energies
            pygame.draw.rect(self.screen, GREEN, play_rect)
            pygame.draw.rect(self.screen, RED, quit_rect)

            # The Oracle of Pygame Events gazes upon the mortal events
            for event in pygame.event.get():
                # If the event foretells a window closure, Pygame gods decree an orderly exit
                if event.type == pygame.QUIT:
                    print("Game>main_menu>pygame quit.")
                    debug.pause_and_clear()
                    pygame.quit()
                    sys.exit()
                # When the mystical MOUSEBUTTONDOWN prophecy unfolds
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # The Seer retrieves the coordinates of the mouse's click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Should the click align with the sacred "Play" rectangle
                    if play_rect.collidepoint(mouse_x, mouse_y):
                        print("Game>main_menu> Play clicked")
                        self.reset_game()  # Reset the game state
                        return 1  # Return 1 for Play
                    # Or if the click resonates with the "Quit" rectangle
                    elif quit_rect.collidepoint(mouse_x, mouse_y):
                        print("Game>main_menu> Quit clicked")
                        debug.pause_and_clear()
                        self.quit_game()
                        return 2  # Return 2 for Quit

            # Inscribing the sacred texts upon the buttons, guiding the players' journey
            menu_font = pygame.font.Font(None, 36)
            play_text = menu_font.render("Play", True, WHITE)
            quit_text = menu_font.render("Quit", True, WHITE)
            self.screen.blit(play_text, (MAX_WIDTH // 2 - 25, HEIGHT // 2 - 40))
            self.screen.blit(quit_text, (MAX_WIDTH // 2 - 25, HEIGHT // 2 + 60))
            pygame.display.flip()

    def show_menu(self):
        debug = Debug()
        print("Game>show_menu")
        debug.pause_and_clear()
        return self.main_menu()
    
    def quit_game(self):
        print("Quitting the game. Farewell, brave adventurer!")
        pygame.quit()
        sys.exit()