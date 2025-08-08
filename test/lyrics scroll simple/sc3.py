import pygame
import time
import re

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FONT_SIZE = 36
SCROLL_SPEED = 0.5  # pixels per frame
LYRIC_FILE = "Ill_Be_Over_You.lrc"

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Scrolling Lyrics")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", FONT_SIZE)

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
    
    # Sort by time
    return sorted(lyrics, key=lambda x: x[0])

lyrics = parse_lrc(LYRIC_FILE)

# Rendered lyric surfaces
rendered_lyrics = [font.render(line[1], True, pygame.Color("white")) for line in lyrics]
highlight_font = pygame.font.SysFont("Arial", FONT_SIZE, bold=True)

start_time = time.time()

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))
    current_time = time.time() - start_time

    # Find current line index
    current_index = 0
    for i in range(len(lyrics)):
        if lyrics[i][0] <= current_time:
            current_index = i
        else:
            break

    # Calculate y offset to scroll current line to center
    target_y = SCREEN_HEIGHT // 2 - FONT_SIZE // 2
    total_height = FONT_SIZE + 10
    offset = -current_index * total_height + target_y

    # Draw lyrics
    for i, (timestamp, text) in enumerate(lyrics):
        y = i * total_height + offset
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
