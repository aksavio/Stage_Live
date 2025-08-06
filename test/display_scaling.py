import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up font
font_size = 150
font = pygame.font.SysFont("Arial", font_size)

# Virtual resolution (higher internal resolution for Retina displays)
virtual_width, virtual_height = 1600, 900
window_width, window_height = virtual_width // 2, virtual_height // 2

# Create a scaled window
screen = pygame.display.set_mode((window_width, window_height), pygame.SCALED | pygame.HWSURFACE)
virtual_surface = pygame.Surface((virtual_width, virtual_height))

# Set window title
pygame.display.set_caption("HiDPI Text Test")

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill virtual surface with white
    virtual_surface.fill((255, 255, 255))

    # Render text on the virtual surface
    text = "Crisp Retina Text?"
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(virtual_width // 2, virtual_height // 2))
    virtual_surface.blit(text_surface, text_rect)

    # Smoothly scale down to screen size
    scaled_surface = pygame.transform.smoothscale(virtual_surface, (window_width, window_height))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
