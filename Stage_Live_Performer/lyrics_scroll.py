import pygame
import re
import time

# --- Configuration ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (24, 24, 24)  # Dark gray, similar to Spotify
FONT_SIZE = 36
LINE_SPACING = 15
FONT_COLOR = (179, 179, 179)  # Lighter gray for inactive text
HIGHLIGHT_COLOR = (255, 255, 255)  # White for active text
FPS = 60
LYRIC_FILE = 'Ill_Be_Over_You.lrc' # Make sure this file is in the same directory

from core import

# --- Helper Function to Parse LRC File ---
def parse_lrc(filepath):
    """
    Parses an .lrc file and returns a sorted list of (time_in_ms, text) tuples.
    """
    lyrics = []
    # Regex to capture time [mm:ss.xx] and text
    lrc_regex = r'\[(\d{2}):(\d{2})\.(\d{2})\](.*)'

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.match(lrc_regex, line)
                if match:
                    minutes, seconds, centiseconds, text = match.groups()
                    # Convert timestamp to total milliseconds
                    time_in_ms = int(minutes) * 60000 + int(seconds) * 1000 + int(centiseconds) * 10
                    text = text.strip()
                    if text: # Only add lines that have text
                        lyrics.append((time_in_ms, text))
    except FileNotFoundError:
        print(f"Error: The lyric file '{filepath}' was not found.")
        return None

    # Sort by time, just in case the file is not ordered
    lyrics.sort()
    return lyrics

# --- Main Application Class ---
class LyricScroller:
    def __init__(self):
        """Initialize Pygame, the display, and load resources."""
        pygame.init()
        pygame.display.set_caption("Spotify-Style Lyric Scroller")
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Load fonts
        try:
            self.font = pygame.font.SysFont('sans', FONT_SIZE)
            self.bold_font = pygame.font.SysFont('sans', FONT_SIZE, bold=True)
        except pygame.error:
            print("Default font not found, using pygame's default.")
            self.font = pygame.font.Font(None, FONT_SIZE)
            self.bold_font = pygame.font.Font(None, FONT_SIZE + 2) # Make it slightly bigger to simulate bold

        # Load and parse lyrics
        self.lyrics = parse_lrc(LYRIC_FILE)
        if not self.lyrics:
            self.running = False
            return
            
        self.start_time = 0
        self.current_line_index = -1
        
        # Scrolling variables
        self.scroll_y = 0
        self.target_scroll_y = 0
        
        self.running = True

    def run(self):
        """The main game loop."""
        self.start_time = pygame.time.get_ticks() # Simulate song starting now
        
        while self.running:
            self.handle_events()
            self.update_state()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()

    def handle_events(self):
        """Handle user input, like closing the window."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update_state(self):
        """Update the current line and scroll position based on time."""
        # Get elapsed time since the "song" started
        elapsed_time = pygame.time.get_ticks() - self.start_time

        # Find the current active line
        new_line_index = -1
        for i, (time_ms, text) in enumerate(self.lyrics):
            if elapsed_time >= time_ms:
                new_line_index = i
            else:
                break # Since the list is sorted, we can stop early
        
        # If the line has changed, update the target scroll position
        if new_line_index != self.current_line_index:
            self.current_line_index = new_line_index
            # The target is to move the current line to the center of the screen
            line_height = self.font.get_height() + LINE_SPACING
            self.target_scroll_y = self.current_line_index * line_height

        # Smoothly interpolate the current scroll position towards the target
        # The factor (e.g., 0.05) determines the "smoothness". Lower is smoother.
        self.scroll_y += (self.target_scroll_y - self.scroll_y) * 0.05

    def draw(self):
        """Render all the graphics to the screen."""
        self.screen.fill(BACKGROUND_COLOR)

        # Calculate the vertical center for drawing lyrics
        center_y = SCREEN_HEIGHT // 2
        line_height = self.font.get_height() + LINE_SPACING

        for i, (time_ms, text) in enumerate(self.lyrics):
            # Determine font and color based on whether it's the current line
            is_current = (i == self.current_line_index)
            font_to_use = self.bold_font if is_current else self.font
            color = HIGHLIGHT_COLOR if is_current else FONT_COLOR

            # Render the text surface
            text_surface = font_to_use.render(text, True, color)
            
            # Calculate the position of the line
            # Start all lines at the center, then offset by their index
            # Finally, apply the smooth scroll
            draw_pos_y = center_y + (i * line_height) - self.scroll_y
            
            # Center the text horizontally
            text_rect = text_surface.get_rect(centerx=SCREEN_WIDTH // 2, y=draw_pos_y)
            
            # Only draw lines that are visible on the screen
            if text_rect.bottom > 0 and text_rect.top < SCREEN_HEIGHT:
                self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

# --- Entry Point ---
if __name__ == '__main__':
    # Ensure the lyric file exists before starting
    try:
        with open(LYRIC_FILE, 'r') as f:
            pass
        app = LyricScroller()
        if app.running:
            app.run()
    except FileNotFoundError:
        print(f"\nFATAL ERROR: '{LYRIC_FILE}' not found.")
        print("Please make sure the lyric file is in the same directory as the script.")
        time.sleep(5)