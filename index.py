import eel
from fht.main import *
from interfaces.gui_interface import *

eel.init('web')


@eel.expose
def analyse_file(file, offset):
    app = Main(file, offset)
    return app.run_fht_correlate()


@eel.expose
def select_file():
    gui = GuiInterface()
    file_path = gui.initialize_file_dialog('Selecionar arquivo para verificar')
    return file_path


eel.start('main.html', size=(900, 600))
