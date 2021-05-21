import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib as mpl
import os


class GuiInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.wm_attributes("-topmost", 1)

        self.images_folder = 'web/tmp/'

        if not os.path.exists(self.images_folder):
            os.mkdir(self.images_folder)

    def initialize_file_dialog(self, title):
        file_path = filedialog.askopenfile(title=title)

        if file_path is not None:
            return file_path.name

    def initialize_folder_dialog(self, title):
        folder_path = filedialog.askdirectory(title=title)

        if folder_path is not None:
            return folder_path

    def generate_second_level_comparison_graphic(self, second_level_comparisons):
        filtered_data = list(filter(lambda item: item[1] > 0, second_level_comparisons.items()))

        if filtered_data.__len__() == 0:
            return

        extensions = [item[0] for item in filtered_data]
        assurances = [item[1] for item in filtered_data]
        
        fig, ax = plt.subplots()

        cmap = mpl.colors.LinearSegmentedColormap.from_list('red_to_green', ['red', 'yellow', 'green'])
        cmap_border = mpl.colors.LinearSegmentedColormap.from_list('white_to_black', ['white', 'black'])

        norm = plt.Normalize(0, 100)
        colors = cmap(norm(assurances))
        colors_border = cmap_border(norm(assurances))

        ax.barh(extensions,
                assurances,
                color=colors,
                height=0.4,
                edgecolor=colors_border)
        ax.set(title="Visão geral das correlações",
               xlabel="% de correlação",
               ylabel="Extensões (com alguma porcentagem de correlação)",
               xlim=[0, 100])

        plt.savefig('web/tmp/graphic.svg', format='svg', dpi=1800, transparent=True)
        # TODO: Melhorar design do graficos
        # ax = bars[0].axes
        # lim = ax.get_xlim() + ax.get_ylim()
        # for bar in bars:
        #     bar.set_zorder(1)
        #     bar.set_facecolor("none")
        #     x, y = bar.get_xy()
        #     w, h = bar.get_width(), bar.get_height()
        #     grad = np.atleast_2d(np.linspace(0, 1 * w / max(assurances), 256))
        #     ax.imshow(grad, extent=[x, x + w, y, y + h], aspect="auto", zorder=0,
        #             norm=mpl.colors.NoNorm(vmin=0, vmax=1))
        # ax.axis(lim)
