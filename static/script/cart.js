window.onload = function () {
    setAmount()
}

function actionItem(idItem, change, price) {
    $.ajax({
        type: 'POST',
        url: `cart/${idItem}`,
        data: {'change': change},
        success: function(response) {
            $('#' + idItem).text(response[idItem]);
            $('#' + idItem + '-price').text(response[idItem] * Number(price) + ' руб');
            setAmount()
        },
        error: function(error) {}
    })
}

function setAmount() {
    let sum = 0
    for (let id = 1; id <= 25; id++) {
        let block = $('#' + id + '-price')
        if (block.length != 0) {
            sum += Number(block.text().split(' ')[0])
        }
    }

    $('#amount').text(`Оплатить` + (sum == 0 ? `` : `: ${sum} руб`))
}
