import pygame
from title import Title # Import the Title class from title.py

def main():
    """
    The main function to run the game.
    """
    # --- Initialization ---
    pygame.init()

    # --- Screen Setup ---
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Centered Title Example")

    # --- Game Objects ---
    # Create an instance of our Title class
    game_title = Title("My Awesome Game", screen_width, screen_height)

    # --- Main Game Loop ---
    running = True
    clock = pygame.time.Clock()

    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # --- Drawing ---
        # Fill the background with a color (e.g., dark grey)
        screen.fill((50, 50, 50))

        # Draw the title on the screen
        game_title.draw(screen)

        # --- Update the Display ---
        # This is crucial; it pushes everything drawn to the actual display.
        pygame.display.flip()

        # --- Frame Rate Control ---
        # Limit the loop to 60 frames per second
        clock.tick(60)

    # --- Quit Pygame ---
    pygame.quit()

if __name__ == '__main__':
    main()