var offset;
var filePath;

async function verify () {
    $('.initial-text, img, .final-text').hide()
    $('.spinner-container').css('display', 'flex')

    reset_database = $('#input-reset')[0].checked
    offset = Number($('.offset-selector').val());
    res = await eel.analyse_file(filePath, offset, reset_database)()

    setTimeout(() => {
        $('.spinner-container').hide()

        if (res.code === 'success') {
            $('.final-text').text('Garantimos que o arquivo verificado é ' + res.correct_extension)
            $('img').attr('src', '/tmp/graphic.png')
            $('img, .final-text').css('display', 'block')
        }

        if (res.code === 'suspect_file') {
            $('.final-text').text('Este é um arquivo modificado, sua extensão original é ' + res.correct_extensions[0])
            $('img').attr('src', '/tmp/graphic.png')
            $('img, .final-text').css('display', 'block')
        }
    }, 2000)
}

async function select_file () {
    filePath = await eel.select_file()()
}