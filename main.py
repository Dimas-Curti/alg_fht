import eel

eel.init('web')


@eel.expose
def analyse_file():
    return 'teste'
    # fht.run_fht(offset, file)


eel.start('main.html', size=(900, 600))
