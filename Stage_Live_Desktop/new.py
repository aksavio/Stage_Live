import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import time
import threading

class LRCTool:
    def __init__(self, root):
        self.root = root
        self.root.title("LRC Timestamp Maker")
        self.root.geometry("600x400")

        pygame.mixer.init()

        self.mp3_path = None
        self.lyrics = []
        self.current_index = 0
        self.timestamps = []

        # ---- UI ----
        self.load_mp3_btn = tk.Button(root, text="Load MP3", command=self.load_mp3)
        self.load_mp3_btn.pack(pady=5)

        self.load_lyrics_btn = tk.Button(root, text="Load Lyrics (.txt)", command=self.load_lyrics)
        self.load_lyrics_btn.pack(pady=5)

        self.play_btn = tk.Button(root, text="Play", command=self.toggle_play_pause, state="disabled")
        self.play_btn.pack(pady=5)

        # Display current & next lyric
        self.current_label = tk.Label(root, text="Current: ---", font=("Helvetica", 14))
        self.current_label.pack(pady=10)

        self.next_label = tk.Label(root, text="Next: ---", font=("Helvetica", 12), fg="gray")
        self.next_label.pack(pady=10)

        # Export button
        self.export_btn = tk.Button(root, text="Export .lrc", command=self.export_lrc, state="disabled")
        self.export_btn.pack(pady=10)

        # Bind spacebar
        root.bind("<space>", self.timestamp_line)

    # -------------------------
    # Load MP3
    # -------------------------
    def load_mp3(self):
        file = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if file:
            self.mp3_path = file
            pygame.mixer.music.load(file)
            self.play_btn.config(state="normal")
            messagebox.showinfo("Loaded", "MP3 Loaded Successfully")

    # -------------------------
    # Load Lyrics
    # -------------------------
    def load_lyrics(self):
        file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file:
            with open(file, "r", encoding="utf-8") as f:
                self.lyrics = [line.strip() for line in f.readlines() if line.strip()]

            self.current_index = 0
            self.timestamps = []

            if self.lyrics:
                self.display_lyrics()

            messagebox.showinfo("Loaded", "Lyrics Loaded Successfully")
            self.export_btn.config(state="disabled")

    # -------------------------
    # Display current/next line
    # -------------------------
    def display_lyrics(self):
        current = self.lyrics[self.current_index] if self.current_index < len(self.lyrics) else "---"
        next_line = self.lyrics[self.current_index + 1] if self.current_index + 1 < len(self.lyrics) else "---"

        self.current_label.config(text=f"Current: {current}")
        self.next_label.config(text=f"Next: {next_line}")

    # -------------------------
    # Timestamp current line
    # -------------------------
    def timestamp_line(self, event=None):
        if not pygame.mixer.music.get_busy():
            return

        # Make sure there IS a "next" line to timestamp
        if self.current_index + 1 >= len(self.lyrics):
            return

        # Get music position in milliseconds
        pos_ms = pygame.mixer.music.get_pos()
        if pos_ms == -1:
            return

        total_seconds = pos_ms / 1000
        minutes = int(total_seconds // 60)
        seconds = total_seconds % 60

        timestamp = f"[{minutes:02d}:{seconds:05.2f}]"

        # Timestamp the NEXT line instead of the current line
        line = self.lyrics[self.current_index + 1]
        self.timestamps.append(f"{timestamp} {line}")

        # Move forward one line (the next becomes current)
        self.current_index += 1
        self.display_lyrics()

        # If this was the last line, allow exporting
        if self.current_index + 1 >= len(self.lyrics):
            messagebox.showinfo("Done", "All lines timestamped! You can now export.")
            self.export_btn.config(state="normal")


    # -------------------------
    # Play / Pause
    # -------------------------
    def toggle_play_pause(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
            self.play_btn.config(text="Pause")
        else:
            pygame.mixer.music.pause()
            self.play_btn.config(text="Play")

    # -------------------------
    # Export LRC File
    # -------------------------
    def export_lrc(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".lrc",
                                                 filetypes=[("LRC files", "*.lrc")])
        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write("\n".join(self.timestamps))

            messagebox.showinfo("Saved", "LRC File Exported Successfully")


# -------------------------
# Run App
# -------------------------
root = tk.Tk()
app = LRCTool(root)
root.mainloop()
