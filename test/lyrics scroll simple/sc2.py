import pygame
import re
import time

# --- Function to parse LRC file ---
def parse_lrc(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    pattern = re.compile(r'\[(\d+):(\d+\.\d+)\](.*)')
    timestamps = []
    for line in lines:
        match = pattern.match(line.strip())
        if match:
            mins = int(match.group(1))
            secs = float(match.group(2))
            t = mins * 60 + secs
            lyric = match.group(3).strip()
            timestamps.append((t, lyric))
    return timestamps

# --- Pygame setup ---
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scrolling Lyrics Viewer")
font = pygame.font.SysFont('Arial', 36)
highlight_font = pygame.font.SysFont('Arial', 42, bold=True)

# --- Load lyrics ---
filename = "Ill_Be_Over_You.lrc"  # Change if needed
lyrics = parse_lrc(filename)

# --- Main loop ---
clock = pygame.time.Clock()
running = True
start_time = time.time()

while running:
    screen.fill((20, 20, 30))
    now = time.time() - start_time

    # Find current lyric
    current_index = 0
    for i in range(len(lyrics)):
        if now >= lyrics[i][0]:
            current_index = i
        else:
            break

    # Scrolling effect - center the current line
    center_y = HEIGHT // 2
    line_height = 50
    for i, (lyric_time, text) in enumerate(lyrics):
        y = center_y + (i - current_index) * line_height
        if i == current_index:
            txt_surface = highlight_font.render(text, True, (220, 255, 80))
        else:
            txt_surface = font.render(text, True, (180, 180, 220))
        screen.blit(txt_surface, ((WIDTH - txt_surface.get_width()) // 2, y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
