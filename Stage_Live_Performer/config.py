import sys
import pygame
import platform

s_width = 0
s_height = 0
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0
RES_WIN_W = 1920
RES_WIN_H = 1080
RES_MAC_W = 1280
RES_MAC_H = 800

import pyautogui

def get_screen_resolution():
    width, height = pyautogui.size()
    return width, height

SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_resolution()
print(SCREEN_WIDTH)
print(SCREEN_HEIGHT)
RES_WIN_H = SCREEN_HEIGHT
RES_WIN_W = SCREEN_WIDTH

HEADER_BG_COLOR = (30,30,30)
FOOTER_BG_COLOR = (30,30,30)

FONT_SIZE = 56
LINE_SPACING = 15
FONT_COLOR = (179, 179, 179)  # Lighter gray for inactive text
HIGHLIGHT_COLOR = (255, 255, 255)  # White for active text
