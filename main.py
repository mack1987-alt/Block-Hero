import pygame
import sys

from game import Game
 
if __name__ == "__main__":
    game = Game()

    while True:
        option = game.show_menu()
        print(option)
        if option == 1:  # Play
            print("main run")
            game.run()
        elif option == 2:  # Quit
            print("main quit")
            pygame.quit()
            sys.exit()

