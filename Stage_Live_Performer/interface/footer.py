import sys
import pygame
import platform
from config import (FOOTER_BG_COLOR, RES_MAC_W, RES_MAC_H, RES_WIN_W, RES_WIN_H)
footer_height = 0
footer_width = 0
t_height = 0

os_sys = platform.system()
        
    # Set different resolutions for Mac and Windows
if os_sys == "Darwin":  # macOS
    footer_height = RES_MAC_H / 10
    footer_width = RES_MAC_W
    t_height = RES_MAC_H
elif os_sys == "Windows":
    footer_height = RES_WIN_H / 10
    footer_width = RES_WIN_W
    t_height = RES_WIN_H
else:  # Linux/Raspberry Pi, fallback
    footer_height = RES_WIN_H / 10
    footer_width = RES_WIN_W
    t_height = RES_WIN_H

footer_start = t_height - footer_height

class Footer:
    def __init__(self):
        self.rect = pygame.Rect(0, footer_start, footer_width, footer_height)
        self.color = FOOTER_BG_COLOR
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
