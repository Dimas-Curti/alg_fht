import tkinter as tk
from tkinter import filedialog


class GuiInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.wm_attributes("-topmost", 1)
        self.selected_path_name = ''

    def initialize_file_dialog(self, title):
        file_path = filedialog.askopenfile(title=title)

        if file_path is not None:
            self.selected_path_name = file_path.name

