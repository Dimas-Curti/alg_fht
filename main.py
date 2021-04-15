import eel
from fht import visualize
from interfaces.gui_interface import *

eel.init('web')


@eel.expose
def analyse_file(file, offset):
    return visualize.run_fht_correlate(file, offset)


@eel.expose
def select_file():
    gui = GuiInterface()
    gui.initialize_file_dialog('Selecionar arquivo para verificar')
    return gui.selected_path_name


eel.start('main.html', size=(900, 600))
