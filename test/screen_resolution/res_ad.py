import pygame
import sys

def get_true_screen_resolution():
    # Try screeninfo first (most reliable)
    try:
        from screeninfo import get_monitors
        monitors = get_monitors()
        if monitors:
            primary = monitors[0]
            print(f"Using screeninfo library")
            return primary.width, primary.height
    except ImportError:
        print("screeninfo not available, trying platform-specific methods")
    
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
            main_screen = NSScreen.mainScreen()
            scale_factor = main_screen.backingScaleFactor()
            frame = main_screen.frame()
            width = int(frame.size.width * scale_factor)
            height = int(frame.size.height * scale_factor)
            print(f"Using AppKit with scale factor: {scale_factor}")
            return width, height
        except ImportError:
            print("AppKit not available")
    
    # Fallback to pygame
    print("Using pygame fallback")
    pygame.init()
    info = pygame.display.Info()
    return info.current_w, info.current_h

def create_fullscreen_display():
    pygame.init()
    
    width, height = get_true_screen_resolution()
    print(f"Detected screen resolution: {width} x {height}")
    
    if sys.platform == "darwin":
        screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.SCALED)
    else:
        screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    
    actual_width, actual_height = screen.get_size()
    print(f"Actual display surface size: {actual_width} x {actual_height}")
    
    return screen, width, height

# Usage
screen, screen_width, screen_height = create_fullscreen_display()
