import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import os
import numpy as np


class GuiInterface:
    def __init__(self):
        self.root = tk.Tk()

        ttk.Style().theme_use('clam')
        self.root.withdraw()
        self.root.wm_attributes("-topmost", 1)

        self.images_folder = 'web/tmp/'

        if not os.path.exists(self.images_folder):
            os.mkdir(self.images_folder)

    @staticmethod
    def initialize_file_dialog(title):
        file_path = filedialog.askopenfile(title=title)

        if file_path is not None:
            return file_path.name

    @staticmethod
    def initialize_folder_dialog(title):
        folder_path = filedialog.askdirectory(title=title)

        if folder_path is not None:
            return folder_path

    @staticmethod
    def generate_general_graphic(extensions, assurances, cmap):
        cmap_border = mpl.colors.LinearSegmentedColormap.from_list('white_to_black', ['white', 'black'])

        norm = plt.Normalize(0, 100)
        colors = cmap(norm(assurances))
        colors_border = cmap_border(norm(assurances))

        fig, ax = plt.subplots(figsize=(6, 6))

        ax.barh(extensions,
                assurances,
                color=colors,
                height=0.5,
                edgecolor=colors_border)
        ax.set(title="Visão geral das correlações",
               xlabel="% de correlação",
               ylabel="Extensões (com alguma porcentagem de correlação)",
               xlim=[0, 100])

        im = ax.imshow(np.arange(110, step=10).reshape((11, 1)), aspect='auto', cmap=cmap)

        cax = inset_axes(ax,
                         width="5%",  # width = 5% of parent_bbox width
                         height="100%",  # height : 50%
                         loc='lower left',
                         bbox_to_anchor=(1.05, 0., 1, 1),
                         bbox_transform=ax.transAxes,
                         borderpad=0,
                         )

        plt.colorbar(im, cax=cax)

        plt.savefig('web/tmp/graphic-general.svg', format='svg', dpi=1800, transparent=True)

    @staticmethod
    def generate_detailed_graphic(full_signature, cmap):
        norm = plt.Normalize(0, 1.0)

        fig2, ax2 = plt.subplots()

        ax2.plot(full_signature)
        ax2.set(title="Visão detalhada das correlações",
                xlabel="Byte",
                ylabel="Frequência",
                xlim=[0, 255],
                ylim=[0, 1.0])

        plt.savefig('web/tmp/graphic-detailed.svg', format='svg', dpi=1800, transparent=True)

    def generate_second_level_comparison_graphics(self, second_level_comparisons, comparison_signature):
        filtered_data = list(filter(lambda item: item[1] > 0, second_level_comparisons.items()))
        filtered_data.sort(key=lambda el: el[1], reverse=True)
        print(filtered_data)

        if filtered_data.__len__() == 0:
            return

        extensions = [item[0] for item in filtered_data]
        assurances = [item[1] for item in filtered_data]

        cmap = mpl.colors.LinearSegmentedColormap.from_list('red_to_green', ['red', 'yellow', 'green'])

        ht_concatenated = []

        for line in comparison_signature["header_signature"]:
            ht_concatenated.append(line)

        for line in comparison_signature["trailer_signature"]:
            ht_concatenated.append(line)

        final_data = np.around(np.average(ht_concatenated, axis=0), 2).tolist()
        self.generate_general_graphic(extensions, assurances, cmap)
        self.generate_detailed_graphic(final_data, cmap)

        # TODO: Melhorar design do graficos
