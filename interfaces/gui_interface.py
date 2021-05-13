import tkinter as tk
from tkinter import filedialog


class GuiInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.wm_attributes("-topmost", 1)

    def initialize_file_dialog(self, title):
        file_path = filedialog.askopenfile(title=title)

        if file_path is not None:
            return file_path.name

    def initialize_folder_dialog(self, title):
        folder_path = filedialog.askdirectory(title=title)

        if folder_path is not None:
            return folder_path

