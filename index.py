import eel
from fht.main import *
from interfaces.gui_interface import *

eel.init('web')


@eel.expose
def analyse_file(file, offset, reset_database):
    app = Main(file, offset, reset_database)

    res = app.run_fht_correlate()
    print(res)
    return res


@eel.expose
def select_file():
    gui = GuiInterface()
    file_path = gui.initialize_file_dialog('Selecionar arquivo para verificar')
    return file_path


def close_callback(route, websockets):
    if os.path.exists('web/tmp'):
        shutil.rmtree("web/tmp")

    if not websockets:
        exit()


eel.start('main.html', size=(1200, 600), close_callback=close_callback)
