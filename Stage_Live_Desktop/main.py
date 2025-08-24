import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
from tkinter import simpledialog


class LyricsSyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lyrics Sync Tool")

        self.audio_file = None
        self.lyrics_file = None
        self.lyrics_lines = []
        self.current_line_idx = 0
        self.is_timing = False
        self.time_stamps = []

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Open Audio File", command=self.load_audio).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Open Lyrics File", command=self.load_lyrics).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Play", command=self.play_audio).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Pause", command=self.pause_audio).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Stop", command=self.stop_audio).grid(row=0, column=4, padx=5)

        # Timing control buttons
        self.timing_btn = tk.Button(root, text="Start Timing", command=self.toggle_timing)
        self.timing_btn.pack(pady=5)

        # Lyrics navigation buttons
        nav_frame = tk.Frame(root)
        nav_frame.pack(pady=5)
        self.prev_btn = tk.Button(nav_frame, text="Previous", command=self.prev_lyric)
        self.prev_btn.grid(row=0, column=0, padx=5)
        self.next_btn = tk.Button(nav_frame, text="Next", command=self.next_lyric)
        self.next_btn.grid(row=0, column=1, padx=5)

        self.audio_label = tk.Label(root, text="Selected audio: None")
        self.audio_label.pack()
        self.lyrics_label = tk.Label(root, text="Selected lyrics: None")
        self.lyrics_label.pack()

        self.lyric_curr_label = tk.Label(root, text="Current line:", font=("Helvetica", 14), fg="black")
        self.lyric_curr_label.pack(pady=2)
        self.lyric_next_label = tk.Label(root, text="Next line:", font=("Helvetica", 12), fg="grey")
        self.lyric_next_label.pack(pady=2)

        # Add Save LRC button
        self.save_btn = tk.Button(root, text="Save LRC", command=self.save_lrc)
        self.save_btn.pack(pady=5)

        # Bind key for timing
        root.bind("<space>", self.register_timestamp)

        pygame.mixer.init()

    def load_audio(self):
        filename = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if filename:
            self.audio_file = filename
            self.audio_label.config(text="Selected audio: {}".format(filename))

    def load_lyrics(self):
        filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if filename:
            self.lyrics_file = filename
            self.lyrics_label.config(text="Selected lyrics: {}".format(filename))
            with open(filename, 'r', encoding='utf-8') as f:
                self.lyrics_lines = [line.strip() for line in f if line.strip()]
            self.current_line_idx = 0
            self.time_stamps = [None] * len(self.lyrics_lines)
            self.update_lyric_display()

    def update_lyric_display(self):
        if not self.lyrics_lines:
            self.lyric_curr_label.config(text="Current line: (no lyrics loaded)")
            self.lyric_next_label.config(text="Next line:")
            return
        curr_text = self.lyrics_lines[self.current_line_idx] if self.current_line_idx < len(self.lyrics_lines) else ""
        next_text = self.lyrics_lines[self.current_line_idx + 1] if self.current_line_idx + 1 < len(self.lyrics_lines) else ""
        self.lyric_curr_label.config(text="Current line: " + curr_text)
        self.lyric_next_label.config(text="Next line: " + next_text)

    def prev_lyric(self):
        if self.lyrics_lines and self.current_line_idx > 0 and not self.is_timing:
            self.current_line_idx -= 1
            self.update_lyric_display()

    def next_lyric(self):
        if self.lyrics_lines and self.current_line_idx + 1 < len(self.lyrics_lines) and not self.is_timing:
            self.current_line_idx += 1
            self.update_lyric_display()

    def play_audio(self):
        if self.audio_file:
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.play()
        else:
            messagebox.showwarning("Audio Not Selected", "Please select an audio file first.")

    def pause_audio(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()

    def stop_audio(self):
        pygame.mixer.music.stop()

    def toggle_timing(self):
        if not self.is_timing:
            if not self.audio_file or not self.lyrics_lines:
                messagebox.showwarning("Missing Files", "Audio and lyrics must be loaded to start timing.")
                return
            self.is_timing = True
            self.timing_btn.config(text="Stop Timing")
            self.current_line_idx = 0
            self.time_stamps = [None] * len(self.lyrics_lines)
            self.update_lyric_display()
            self.play_audio()
            # Disable navigation buttons during timing
            self.prev_btn.config(state='disabled')
            self.next_btn.config(state='disabled')
        else:
            self.is_timing = False
            self.timing_btn.config(text="Start Timing")
            # Enable navigation buttons after timing
            self.prev_btn.config(state='normal')
            self.next_btn.config(state='normal')
            pygame.mixer.music.stop()
            messagebox.showinfo("Timing Stopped", "Timing mode ended. You can now save the .lrc file.")

    def register_timestamp(self, event):
        if not self.is_timing:
            return
        if self.current_line_idx >= len(self.lyrics_lines):
            return

        # pygame returns milliseconds since music started
        pos_millis = pygame.mixer.music.get_pos()
        if pos_millis == -1:
            messagebox.showwarning("Playback Error", "Audio playback not detected.")
            return

        self.time_stamps[self.current_line_idx] = pos_millis
        self.current_line_idx += 1
        if self.current_line_idx < len(self.lyrics_lines):
            self.update_lyric_display()
        else:
            self.toggle_timing()  # Stop timing automatically at the end
    
    def save_lrc(self):
        if not self.lyrics_lines or not self.time_stamps:
            messagebox.showwarning("No Data", "Please load lyrics and time them before saving.")
            return
         # Check if all lines have timestamps
        if None in self.time_stamps:
            choice = messagebox.askyesno("Incomplete Timing",
                                         "Some lines are not timed. Save anyway?")
            if not choice:
                return

        # Format timestamps and prepare content
        lines_to_write = []
        for time_ms, lyric in zip(self.time_stamps, self.lyrics_lines):
            if time_ms is None:
                # Skip untimed lines or you could write without timestamp if desired
                continue
            total_seconds = time_ms / 1000
            minutes = int(total_seconds // 60)
            seconds = int(total_seconds % 60)
            hundredths = int((total_seconds - int(total_seconds)) * 100)
            timestamp = f"[{minutes:02d}:{seconds:02d}.{hundredths:02d}]"
            lines_to_write.append(f"{timestamp}{lyric}")

        # Ask user for save location
        save_path = filedialog.asksaveasfilename(defaultextension=".lrc",
                                                 filetypes=[("LRC Files", "*.lrc")])
        if save_path:
            try:
                with open(save_path, 'w', encoding='utf-8') as f:
                    for line in lines_to_write:
                        f.write(line + "\n")
                messagebox.showinfo("Success", f"LRC file saved to:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LyricsSyncApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import filedialog, messagebox
import pygame

class LyricsSyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lyrics Sync Tool")

        self.audio_file = None
        self.lyrics_file = None
        self.lyrics_lines = []
        self.current_line_idx = 0
        self.is_timing = False
        self.time_stamps = []

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Open Audio File", command=self.load_audio).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Open Lyrics File", command=self.load_lyrics).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Play", command=self.play_audio).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Pause", command=self.pause_audio).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Stop", command=self.stop_audio).grid(row=0, column=4, padx=5)

        # Timing control buttons
        self.timing_btn = tk.Button(root, text="Start Timing", command=self.toggle_timing)
        self.timing_btn.pack(pady=5)

        # Lyrics navigation buttons
        nav_frame = tk.Frame(root)
        nav_frame.pack(pady=5)
        self.prev_btn = tk.Button(nav_frame, text="Previous", command=self.prev_lyric)
        self.prev_btn.grid(row=0, column=0, padx=5)
        self.next_btn = tk.Button(nav_frame, text="Next", command=self.next_lyric)
        self.next_btn.grid(row=0, column=1, padx=5)

        self.audio_label = tk.Label(root, text="Selected audio: None")
        self.audio_label.pack()
        self.lyrics_label = tk.Label(root, text="Selected lyrics: None")
        self.lyrics_label.pack()

        self.lyric_curr_label = tk.Label(root, text="Current line:", font=("Helvetica", 14), fg="blue")
        self.lyric_curr_label.pack(pady=2)
        self.lyric_next_label = tk.Label(root, text="Next line:", font=("Helvetica", 12), fg="grey")
        self.lyric_next_label.pack(pady=2)

        # Bind key for timing
        root.bind("<space>", self.register_timestamp)

        pygame.mixer.init()

    def load_audio(self):
        filename = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if filename:
            self.audio_file = filename
            self.audio_label.config(text="Selected audio: {}".format(filename))

    def load_lyrics(self):
        filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if filename:
            self.lyrics_file = filename
            self.lyrics_label.config(text="Selected lyrics: {}".format(filename))
            with open(filename, 'r', encoding='utf-8') as f:
                self.lyrics_lines = [line.strip() for line in f if line.strip()]
            self.current_line_idx = 0
            self.time_stamps = [None] * len(self.lyrics_lines)
            self.update_lyric_display()

    def update_lyric_display(self):
        if not self.lyrics_lines:
            self.lyric_curr_label.config(text="Current line: (no lyrics loaded)")
            self.lyric_next_label.config(text="Next line:")
            return
        curr_text = self.lyrics_lines[self.current_line_idx] if self.current_line_idx < len(self.lyrics_lines) else ""
        next_text = self.lyrics_lines[self.current_line_idx + 1] if self.current_line_idx + 1 < len(self.lyrics_lines) else ""
        self.lyric_curr_label.config(text="Current line: " + curr_text)
        self.lyric_next_label.config(text="Next line: " + next_text)

    def prev_lyric(self):
        if self.lyrics_lines and self.current_line_idx > 0 and not self.is_timing:
            self.current_line_idx -= 1
            self.update_lyric_display()

    def next_lyric(self):
        if self.lyrics_lines and self.current_line_idx + 1 < len(self.lyrics_lines) and not self.is_timing:
            self.current_line_idx += 1
            self.update_lyric_display()

    def play_audio(self):
        if self.audio_file:
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.play()
        else:
            messagebox.showwarning("Audio Not Selected", "Please select an audio file first.")

    def pause_audio(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()

    def stop_audio(self):
        pygame.mixer.music.stop()

    def toggle_timing(self):
        if not self.is_timing:
            if not self.audio_file or not self.lyrics_lines:
                messagebox.showwarning("Missing Files", "Audio and lyrics must be loaded to start timing.")
                return
            self.is_timing = True
            self.timing_btn.config(text="Stop Timing")
            self.current_line_idx = 0
            self.time_stamps = [None] * len(self.lyrics_lines)
            self.update_lyric_display()
            self.play_audio()
            # Disable navigation buttons during timing
            self.prev_btn.config(state='disabled')
            self.next_btn.config(state='disabled')
        else:
            self.is_timing = False
            self.timing_btn.config(text="Start Timing")
            # Enable navigation buttons after timing
            self.prev_btn.config(state='normal')
            self.next_btn.config(state='normal')
            pygame.mixer.music.stop()
            messagebox.showinfo("Timing Stopped", "Timing mode ended. You can now save the .lrc file.")

    def register_timestamp(self, event):
        if not self.is_timing:
            return
        if self.current_line_idx >= len(self.lyrics_lines):
            return

        # pygame returns milliseconds since music started
        pos_millis = pygame.mixer.music.get_pos()
        if pos_millis == -1:
            messagebox.showwarning("Playback Error", "Audio playback not detected.")
            return

        self.time_stamps[self.current_line_idx] = pos_millis
        self.current_line_idx += 1
        if self.current_line_idx < len(self.lyrics_lines):
            self.update_lyric_display()
        else:
            self.toggle_timing()  # Stop timing automatically at the end

if __name__ == "__main__":
    root = tk.Tk()
    app = LyricsSyncApp(root)
    root.mainloop()
