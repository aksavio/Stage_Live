import pygame
import time
import re

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FONT_SIZE = 36
LYRIC_FILE = "Ill_Be_Over_You.lrc"
LINE_SPACING = 10

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Smooth Scrolling Lyrics")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", FONT_SIZE)
highlight_font = pygame.font.SysFont("Arial", FONT_SIZE, bold=True)

# Parse the .lrc file
def parse_lrc(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    lyrics = []
    for line in lines:
        matches = re.findall(r'\[(\d+):(\d+\.\d+)\](.*)', line)
        for match in matches:
            minutes, seconds, text = match
            time_in_seconds = int(minutes) * 60 + float(seconds)
            lyrics.append((time_in_seconds, text.strip()))
    
    return sorted(lyrics, key=lambda x: x[0])

lyrics = parse_lrc(LYRIC_FILE)
rendered_lyrics = [font.render(line[1], True, pygame.Color("white")) for line in lyrics]

start_time = time.time()
running = True

while running:
    screen.fill((0, 0, 0))
    current_time = time.time() - start_time

    # Find previous and next lyric lines
    current_index = 0
    for i in range(len(lyrics)):
        if lyrics[i][0] <= current_time:
            current_index = i
        else:
            break

    # Calculate interpolation between lines for smooth scrolling
    line_height = FONT_SIZE + LINE_SPACING
    if current_index < len(lyrics) - 1:
        t1, _ = lyrics[current_index]
        t2, _ = lyrics[current_index + 1]
        progress = (current_time - t1) / (t2 - t1) if t2 != t1 else 0
    else:
        progress = 0

    scroll_y = -((current_index + progress) * line_height) + SCREEN_HEIGHT // 2 - FONT_SIZE // 2

    # Draw all lines with interpolated scroll offset
    for i, (timestamp, text) in enumerate(lyrics):
        y = i * line_height + scroll_y
        if i == current_index:
            surface = highlight_font.render(text, True, pygame.Color("cyan"))
        else:
            surface = font.render(text, True, pygame.Color("gray"))
        screen.blit(surface, (SCREEN_WIDTH // 2 - surface.get_width() // 2, y))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
