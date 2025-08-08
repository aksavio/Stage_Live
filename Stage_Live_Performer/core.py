import sys
import pygame
import platform


from config import (SCREEN_WIDTH, SCREEN_HEIGHT, RES_MAC_W, RES_MAC_H, RES_WIN_W, RES_WIN_H, FONT_SIZE, FOOTER_BG_COLOR, FONT_COLOR, LINE_SPACING,HEADER_BG_COLOR, HIGHLIGHT_COLOR)
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
file_path = "Lyrics"
folder = "Lyrics"
start_time = 0
song_lyrics = "lyrics"
start_file = "00_open.lrc"

# variables for states of the main program
song_counter = int(0)
# song_counter = file_count      #counter for the songs
song_counter_l = file_count -  1

print (song_counter_l)

LYRIC_FILE = '00_open.lrc'
from lyrics_scroll import  parse_lrc
song_lyrics = parse_lrc(f"{folder}/{start_file}")
print(song_lyrics)
elapsed_time = 0
timer_start = 0

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

        self.start_time = 0
        self.current_line_index = -1
        
        # Scrolling variables
        self.scroll_y = 0
        self.target_scroll_y = 0


        try:
            self.font = pygame.font.SysFont('sans', FONT_SIZE)
            self.bold_font = pygame.font.SysFont('sans', FONT_SIZE, bold=True)
        except pygame.error:
            print("Default font not found, using pygame's default.")
            self.font = pygame.font.Font(None, FONT_SIZE)
            self.bold_font = pygame.font.Font(None, FONT_SIZE + 2) # Make it slightly bigger to simulate bold
        
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
        global start_time
        global song_lyrics
        global lrc_files_f
        global elapsed_time
        global timer_start
        # Set different resolutions for Mac and Windows
        if self.os_type == "Darwin":  # macOS
            self.width, self.height = RES_MAC_W, RES_MAC_H
        elif self.os_type == "Windows":
            self.width, self.height = RES_WIN_W, RES_WIN_H
        else:  # Linux/Raspberry Pi, fallback
            self.width, self.height = RES_WIN_W, RES_WIN_H
        running = True
        song_counter = 0
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
                    self.file_path = f"{folder}/{file_names_f[song_counter]}"
                    self.lyrics = parse_lrc(self.file_path)
                    song_lyrics = self.lyrics
                    print(file_names_f[song_counter])
                    start_time = 0
                    self.current_line_index = -1
                    # Scrolling variables
                    self.scroll_y = 0
                    self.target_scroll_y = 0
                    print(song_lyrics)
                    self.start_time = 0
                    elapsed_time = 0
                    timer_start = pygame.time.get_ticks()

            # Drawing Graphics
            # self.screen = pygame.display.set_mode((self.width, self.height), pygame.SCALED | pygame.RESIZABLE | pygame.HIDDEN | pygame.NOFRAME | pygame.OPENGL | pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.ASYNCBLIT)
            # self.screen = pygame.display.set_mode((self.width, self.height), pygame.SCALED)
            self.screen.fill((0, 0, 0))
            header_.draw(self.screen)
            footer_.draw(self.screen)
            title = Title(file_names[song_counter], self.width, 70)
            title.draw(self.screen)
            self.update_state()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
    
    def update_state(self):
        """Update the current line and scroll position based on time."""
        # Get elapsed time since the "song" started
        elapsed_time = pygame.time.get_ticks() - timer_start

        # Find the current active line
        new_line_index = -1
        for i, (time_ms, text) in enumerate(song_lyrics):
            if elapsed_time >= time_ms:
                new_line_index = i
            else:
                break # Since the list is sorted, we can stop early
        
        # If the line has changed, update the target scroll position
        if new_line_index != self.current_line_index:
            self.current_line_index = new_line_index
            # The target is to move the current line to the center of the screen
            line_height = self.font.get_height() + LINE_SPACING
            self.target_scroll_y = self.current_line_index * line_height

        # Smoothly interpolate the current scroll position towards the target
        # The factor (e.g., 0.05) determines the "smoothness". Lower is smoother.
        self.scroll_y += (self.target_scroll_y - self.scroll_y) * 0.05

    def draw(self):
        """Render all the graphics to the screen."""
        # self.screen.fill(BACKGROUND_COLOR)

        # Calculate the vertical center for drawing lyrics
        center_y = SCREEN_HEIGHT // 2
        line_height = self.font.get_height() + LINE_SPACING

        for i, (time_ms, text) in enumerate(song_lyrics):
            # Determine font and color based on whether it's the current line
            is_current = (i == self.current_line_index)
            font_to_use = self.bold_font if is_current else self.font
            color = HIGHLIGHT_COLOR if is_current else FONT_COLOR

            # Render the text surface
            text_surface = font_to_use.render(text, True, color)
            
            # Calculate the position of the line
            # Start all lines at the center, then offset by their index
            # Finally, apply the smooth scroll
            draw_pos_y = center_y + (i * line_height) - self.scroll_y
            
            # Center the text horizontally
            text_rect = text_surface.get_rect(centerx=self.width // 2, y=draw_pos_y)
            
            # Only draw lines that are visible on the screen
            if text_rect.bottom > 0 and text_rect.top < self.height:
                self.screen.blit(text_surface, text_rect)

        #print("exit")
        #sys.exit()