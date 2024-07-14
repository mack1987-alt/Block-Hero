import pygame
import sys
from constants import MAX_WIDTH, HEIGHT, WHITE, GREEN, RED

class Menu:
    def __init__(self, screen, background):
        self.screen = screen
        self.background = background

    def show_pause_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Menu>show_pause_menu>pygame quit.")
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    resume_button_rect = pygame.Rect(MAX_WIDTH // 2 - 50, HEIGHT // 2, 100, 50)
                    if resume_button_rect.collidepoint(mouse_x, mouse_y):
                        return "resume"
                    main_menu_button_rect = pygame.Rect(MAX_WIDTH // 2 - 45, HEIGHT // 2 + 60, 100, 50)
                    if main_menu_button_rect.collidepoint(mouse_x, mouse_y):
                        return "main_menu"

            # Draw the pause menu
            self.screen.blit(self.background, (0, 0))  # Use the background image to fill the screen

            resume_button_rect = pygame.Rect(MAX_WIDTH // 2 - 50, HEIGHT // 2, 100, 50)
            main_menu_button_rect = pygame.Rect(MAX_WIDTH // 2 - 50, HEIGHT // 2 + 60, 100, 50)

            pygame.draw.rect(self.screen, GREEN, resume_button_rect)
            pygame.draw.rect(self.screen, RED, main_menu_button_rect)

            resume_text = pygame.font.Font(None, 36).render("Resume", True, WHITE)
            main_menu_text = pygame.font.Font(None, 36).render("Main Menu", True, WHITE)

            self.screen.blit(resume_text, (MAX_WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2 + 10))
            self.screen.blit(main_menu_text, (MAX_WIDTH // 2 - main_menu_text.get_width() // 2, HEIGHT // 2 + 70))

            pygame.display.flip()

    def show_game_over_screen(self):
        while True:
            self.screen.blit(self.background, (0, 0))
            game_over_font = pygame.font.Font(None, 72)
            text = game_over_font.render("You Lost...", True, RED)
            self.screen.blit(text, (MAX_WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

            pygame.display.flip()
            
            pygame.time.delay(3000)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Assume the buttons are similar to the main menu for illustration purposes
                    play_rect = pygame.Rect(MAX_WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 50)
                    quit_rect = pygame.Rect(MAX_WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)
                    if play_rect.collidepoint(mouse_x, mouse_y):
                        return "play_again"
                    elif quit_rect.collidepoint(mouse_x, mouse_y):
                        return "main_menu"
