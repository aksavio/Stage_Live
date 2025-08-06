import sys
import pygame
import platform
from config import (HEADER_BG_COLOR, RES_MAC_W, RES_MAC_H, RES_WIN_W, RES_WIN_H)
header_height = 0
header_width = 0

os_sys = platform.system()
        
    # Set different resolutions for Mac and Windows
if os_sys == "Darwin":  # macOS
    header_height = RES_MAC_H / 10
    header_width = RES_MAC_W
elif os_sys == "Windows":
    header_height = RES_WIN_H / 10
    header_width = RES_WIN_W
else:  # Linux/Raspberry Pi, fallback
    header_height = RES_WIN_H / 10
    header_width = RES_WIN_W


class Header:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, header_width, header_height)
        self.color = HEADER_BG_COLOR
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
