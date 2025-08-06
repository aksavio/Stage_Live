import pygame
import re
import time

# --- Configuration ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (24, 24, 24)
FONT_SIZE = 36
CHORD_FONT_SIZE = 32
LINE_SPACING = 15
CHORD_MARGIN_BOTTOM = 8 # Space between chord and lyric
FONT_COLOR = (179, 179, 179)
HIGHLIGHT_COLOR = (255, 255, 255)
CHORD_COLOR = (251, 189, 34) # A nice gold/yellow for chords
FPS = 60
LYRIC_FILE = 'bohemian_rhapsody.lrc'

# --- Helper Function to Parse LRC File with Chords ---
def parse_lrc_with_chords(filepath):
    """
    Parses an .lrc file with chords.
    Chords are expected on the line immediately preceding the lyric line.
    Returns a sorted list of (time_in_ms, chords, text) tuples.
    """
    lyrics_with_chords = []
    # Regex to capture time [mm:ss.xx]
    time_regex = r'\[(\d{2}):(\d{2})\.(\d{2})\]'
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: The lyric file '{filepath}' was not found.")
        return None

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        time_match = re.match(time_regex, line)
        
        if time_match:
            # This line has a timestamp.
            minutes, seconds, centiseconds = time_match.groups()
            time_in_ms = int(minutes) * 60000 + int(seconds) * 1000 + int(centiseconds) * 10
            
            # The rest of the line is the first line of text (could be chord or lyric)
            first_text_part = line[len(time_match.group(0)):].strip()
            
            # Look ahead to the next line to see if it's part of this entry
            if i + 1 < len(lines) and not re.match(time_regex, lines[i+1]):
                # The next line does NOT have a timestamp, so it's the lyric for the current chord.
                chords = first_text_part
                lyrics = lines[i+1].strip()
                i += 1 # Consume the next line as well
            else:
                # The next line has its own timestamp, so this line is just a lyric.
                chords = "" # No chord for this line
                lyrics = first_text_part
            
            if chords or lyrics: # Only add if there's some content
                 lyrics_with_chords.append((time_in_ms, chords, lyrics))
        
        i += 1

    lyrics_with_chords.sort()
    return lyrics_with_chords

# --- Main Application Class ---
class LyricScroller:
    def __init__(self):
        """Initialize Pygame, the display, and load resources."""
        pygame.init()
        pygame.display.set_caption("Spotify-Style Lyric & Chord Scroller")
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Load fonts
        try:
            self.font = pygame.font.SysFont('sans', FONT_SIZE)
            self.bold_font = pygame.font.SysFont('sans', FONT_SIZE, bold=True)
            self.chord_font = pygame.font.SysFont('sans', CHORD_FONT_SIZE, bold=True)
        except pygame.error:
            print("Default font not found, using pygame's default.")
            self.font = pygame.font.Font(None, FONT_SIZE)
            self.bold_font = pygame.font.Font(None, FONT_SIZE + 2)
            self.chord_font = pygame.font.Font(None, CHORD_FONT_SIZE)

        # Load and parse lyrics
        self.lyrics_data = parse_lrc_with_chords(LYRIC_FILE)
        if not self.lyrics_data:
            self.running = False
            return
            
        self.start_time = 0
        self.current_line_index = -1
        
        # Scrolling variables
        self.scroll_y = 0
        self.target_scroll_y = 0
        
        self.running = True

    def get_line_height(self, index):
        """Calculates the total height of a line, including chords."""
        _, chords, lyrics = self.lyrics_data[index]
        height = 0
        if chords:
            height += self.chord_font.get_height() + CHORD_MARGIN_BOTTOM
        if lyrics:
            height += self.font.get_height()
        return height + LINE_SPACING

    def run(self):
        """The main game loop."""
        self.start_time = pygame.time.get_ticks()
        
        while self.running:
            self.handle_events()
            self.update_state()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()

    def handle_events(self):
        """Handle user input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False

    def update_state(self):
        """Update the current line and scroll position."""
        elapsed_time = pygame.time.get_ticks() - self.start_time

        new_line_index = -1
        for i, (time_ms, _, _) in enumerate(self.lyrics_data):
            if elapsed_time >= time_ms:
                new_line_index = i
            else:
                break
        
        if new_line_index != self.current_line_index:
            self.current_line_index = new_line_index
            
            # Calculate the total height of all lines up to the current one
            total_height_before_current = sum(self.get_line_height(i) for i in range(self.current_line_index))
            self.target_scroll_y = total_height_before_current

        # Smoothly interpolate scroll position
        self.scroll_y += (self.target_scroll_y - self.scroll_y) * 0.05

    def draw(self):
        """Render all graphics."""
        self.screen.fill(BACKGROUND_COLOR)
        center_y = SCREEN_HEIGHT // 2
        
        current_y_pos = 0
        for i, (time_ms, chords, lyrics) in enumerate(self.lyrics_data):
            is_current = (i == self.current_line_index)
            lyric_font = self.bold_font if is_current else self.font
            lyric_color = HIGHLIGHT_COLOR if is_current else FONT_COLOR
            
            # --- Draw Chords ---
            chord_surface = None
            if chords:
                chord_surface = self.chord_font.render(chords, True, CHORD_COLOR)
                chord_rect = chord_surface.get_rect(centerx=SCREEN_WIDTH // 2, y=center_y + current_y_pos - self.scroll_y)
                if chord_rect.bottom > 0 and chord_rect.top < SCREEN_HEIGHT:
                    self.screen.blit(chord_surface, chord_rect)
                current_y_pos += chord_surface.get_height() + CHORD_MARGIN_BOTTOM

            # --- Draw Lyrics ---
            lyric_surface = None
            if lyrics:
                lyric_surface = lyric_font.render(lyrics, True, lyric_color)
                lyric_rect = lyric_surface.get_rect(centerx=SCREEN_WIDTH // 2, y=center_y + current_y_pos - self.scroll_y)
                if lyric_rect.bottom > 0 and lyric_rect.top < SCREEN_HEIGHT:
                    self.screen.blit(lyric_surface, lyric_rect)
                current_y_pos += lyric_surface.get_height()
            
            current_y_pos += LINE_SPACING


        pygame.display.flip()

# --- Entry Point ---
if __name__ == '__main__':
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