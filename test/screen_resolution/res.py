import pygame
import sys

def get_true_screen_resolution():
    # Windows DPI awareness
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.user32.SetProcessDPIAware()
        except:
            pass
    
    # macOS native resolution
    elif sys.platform == "darwin":
        try:
            from AppKit import NSScreen
            rect = NSScreen.mainScreen().frame()
            return int(rect.size.width), int(rect.size.height)
        except ImportError:
            pass
    
    # Fallback for all platforms
    pygame.init()
    info = pygame.display.Info()
    return info.current_w, info.current_h

def create_fullscreen_display():
    pygame.init()
    
    if sys.platform == "darwin":  # macOS
        # Get actual screen dimensions first
        width, height = get_true_screen_resolution()
        # Use actual dimensions with SCALED flag
        screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.SCALED)
    else:
        # For Windows and Linux
        width, height = get_true_screen_resolution()
        screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    
    return screen

# Usage
screen = create_fullscreen_display()
