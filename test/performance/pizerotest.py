# optimized_lyrics_scroll.py
import pygame, time, sys

pygame.init()
# set a small resolution for better perf on Pi Zero
W, H = 800, 480
screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# load/parse lyrics into list of lines (you already have this)
lyrics = [
    "Some people live their dreams",
    "Some people close their eyes",
    "Some people's destiny",
    "Passes by"
]

# Choose font once and pre-render each line
# font = pygame.font.Font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
font = pygame.font.SysFont('sans', 36)
rendered = [font.render(line, True, (255,255,255)).convert_alpha() for line in lyrics]

# Vertical spacing and initial offset (start below screen)
line_height = rendered[0].get_height() + 8
y = H  # start off-screen
scroll_speed = 60  # pixels per second

running = True
last_t = time.time()
while running:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT or (evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE):
            running = False

    # time-based movement (smooth even if framerate varies)
    t = time.time()
    dt = t - last_t
    last_t = t
    y -= scroll_speed * dt

    # reset or stop when all lines scrolled past top
    if y + len(rendered) * line_height < 0:
        y = H  # loop for demo

    # draw background and blit all pre-rendered lines
    screen.fill((0,0,0))
    for i, surf in enumerate(rendered):
        screen.blit(surf, (20, int(y + i * line_height)))

    pygame.display.flip()
    clock.tick(30)  # limit to 30 FPS

pygame.quit()
sys.exit()
