import eel
from fht import visualize
import tkinter as tk
from tkinter import filedialog
import os
import inspect

eel.init('web')


@eel.expose
def analyse_file(file, offset):
    return visualize.run_fht(file, offset)


@eel.expose
def select_file():
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    file_path = filedialog.askopenfile(title="Selecionar arquivo")
    print(file_path.name)
    return file_path.name


eel.start('main.html', size=(900, 600))
