var offset;
var filePath;

async function verify () {
    offset = Number(document.querySelector('.offset-selector').value);

    console.log('File path escolhido: ', filePath)
    console.log('Offset escolhido: ', offset)

    var response = await eel.analyse_file(filePath, offset)()
    console.log(response)
}

async function select_file () {
    filePath = await eel.select_file()()
}