var offset;
var filePath;
const OFFSET = 5


async function verify () {
    initiate_verify()

    reset_database = $('#input-reset')[0].checked
    res = await eel.analyse_file(filePath, OFFSET, reset_database)()

    setTimeout(() => {
        $('.spinner-container').slideUp(500)

        switch (res.code) {
            case 'success':
                $('img').fadeOut(1000)
                change_final_text('Este arquivo é seguro, garantimos que o arquivo verificado é ' + res.correct_extension)

                break;

            case 'suspect_file':
                switch (res.correct_extensions.length) {
                    case 1:
                        change_final_text('Este é um arquivo modificado, sua extensão original é ' + res.correct_extensions[0])

                        break;
                    case 2:
                        change_final_text('Este é um arquivo modificado, ele tem uma alta probabilidade de ser ' + res.correct_extensions[0] + ' ou ' + res.correct_extensions[1])

                        break;
                }
                show_graphics()

                break;

            case 'unknown_extension':
                change_final_text('Desculpe, não possuímos esta extensão no banco de dados.')
                break;
        }
    }, 2000)
}

async function select_file () {
    filePath = await eel.select_file()()
}

function initiate_verify() {
    $('img').fadeOut(1000)

    $('.main-wrapper, img').removeClass('img-open')
    $('.initial-text, .final-text').hide()
    $('.spinner-container').fadeIn(500)
    $('.spinner-container').slideDown(500)
    $('.spinner-container').css('display', 'flex')
}

function show_graphics () {
    $('.spinner-container').fadeOut(500)

    $('img').attr('src', '/tmp/graphic.svg')
    $('img').slideUp(1000)
    $('.main-wrapper, img').addClass('img-open')
    $('img').fadeIn(1000)
    $('img').show()
}

function change_final_text(message) {
    $('.final-text').text(message)
    $('.final-text').fadeIn(1000)
    $('.final-text').slideDown(1000)
}