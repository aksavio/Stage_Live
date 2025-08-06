import pygame
from config import (SCREEN_WIDTH, HEADER_HEIGHT)


class Title:
    """
    A class to represent a text title centered on the screen.
    """
    def __init__(self, text, SCREEN_WIDTH, HEADER_HEIGHT, font_size=74, font_color=(255, 255, 255), font_name=None):
        """
        Initializes the Title object.

        Args:
            text (str): The text to be displayed as the title.
            screen_width (int): The width of the game screen.
            screen_height (int): The height of the game screen.
            font_size (int, optional): The size of the font. Defaults to 74.
            font_color (tuple, optional): The color of the font in (R, G, B). Defaults to white.
            font_name (str, optional): The name of the font to use. Defaults to Pygame's default font.
        """
        self.screen_width = SCREEN_WIDTH
        self.screen_height = HEADER_HEIGHT
        self.font_color = font_color

        # Create a font object.
        # You can specify a font file (e.g., 'your_font.ttf') or use None for the default.
        self.font = pygame.font.Font(font_name, font_size)

        # Render the text into a surface.
        # The 'True' is for anti-aliasing, which makes the text look smoother.
        self.text_surface = self.font.render(text, True, self.font_color)

        # Get the rectangle of the text surface and center it on the screen.
        self.rect = self.text_surface.get_rect(center=(self.screen_width / 2, self.screen_height / 2))

    def draw(self, screen):
        """
        Draws the title onto the given screen surface.

        Args:
            screen (pygame.Surface): The screen surface to draw the title on.
        """
        screen.blit(self.text_surface, self.rect)