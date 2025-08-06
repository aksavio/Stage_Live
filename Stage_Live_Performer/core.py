import sys
import pygame
import platform


from config import (SCREEN_WIDTH, SCREEN_HEIGHT, RES_MAC_W, RES_MAC_H, RES_WIN_W, RES_WIN_H)
window_width = 0
window_height = 0

from interface.header import Header
from interface.footer import Footer
from interface.title import Title

header_ = Header()
footer_ = Footer()

from file_counter import count_lrc_files
from file_counter import get_lrc_names_sorted
from file_counter import get_lrc_names_sorted_f


# .lrc file counter
target_dir = "Lyrics"  # Change this to your directory
    
file_count = count_lrc_files(target_dir)
file_names = get_lrc_names_sorted(target_dir)
file_names_f = get_lrc_names_sorted_f(target_dir)



# variables for states of the main program
song_counter = int(0)
# song_counter = file_count      #counter for the songs
song_counter_l = file_count -  1

print (song_counter_l)

class LyricsApp:
    def __init__(self):
        pygame.init()
        self.os_type = platform.system()
        
        # Set different resolutions for Mac and Windows
        if self.os_type == "Darwin":  # macOS
            self.width, self.height = RES_MAC_W, RES_MAC_H
        elif self.os_type == "Windows":
            self.width, self.height = RES_WIN_W, RES_WIN_H
        else:  # Linux/Raspberry Pi, fallback
            self.width, self.height = RES_WIN_W, RES_WIN_H
        
        self.fullscreen = False
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.SCALED | pygame.RESIZABLE)
        print(self.width)
        print(self.height)
        window_width = self.width
        window_height = self.height
        pygame.display.set_caption("Stage_Live")
        self.clock = pygame.time.Clock()
        
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
            f_s = 1
            print("full_screen")
        else:
            self.screen = pygame.display.set_mode((self.width, self.height))
    
    
    def run(self):
        global song_counter
        global song_counter_l
        # Set different resolutions for Mac and Windows
        if self.os_type == "Darwin":  # macOS
            self.width, self.height = RES_MAC_W, RES_MAC_H
        elif self.os_type == "Windows":
            self.width, self.height = RES_WIN_W, RES_WIN_H
        else:  # Linux/Raspberry Pi, fallback
            self.width, self.height = RES_WIN_W, RES_WIN_H
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        song_counter = song_counter - 1
                        if song_counter < 0:
                            song_counter = 0
                    if event.key == pygame.K_m:
                        song_counter = song_counter + 1
                        if song_counter > song_counter_l:
                            song_counter = song_counter_l
                    print(song_counter)
        
            # Drawing Graphics
            # self.screen = pygame.display.set_mode((self.width, self.height), pygame.SCALED | pygame.RESIZABLE | pygame.HIDDEN | pygame.NOFRAME | pygame.OPENGL | pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.ASYNCBLIT)
            # self.screen = pygame.display.set_mode((self.width, self.height), pygame.SCALED)
            self.screen.fill((0, 0, 0))
            header_.draw(self.screen)
            footer_.draw(self.screen)
            title = Title(file_names[song_counter], self.width, 70)
            title.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
    
        sys.exit()