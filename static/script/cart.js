window.onload = function () {
    setAmount()
}

function setAmount() {
    let sum = 0
    for (let id = 1; id <= 25; id++) {
        let block = $('#' + id + '-price')
        if (block.length != 0)
            sum += Number(block.text().split(' ')[0])
    }

    $('#amount').text(`Оплатить` + (sum == 0 ? `` : `: ${sum} руб`))
}

function actionItem(idItem, change, price) {
    $.ajax({
        type: 'POST',
        url: `cart/${idItem}`,
        data: {'change': change},
        success: function(response) {
            if (response[idItem] == 0) {
                $('#' + idItem + '-item').remove()
                if ($("#items").children().length == 0)
                    $("#iibwn").remove()

                $('#cart').text($("#items").children().length != 0 ? $("#items").children().length : "")
            } else {
                $('#' + idItem).text(response[idItem])
                $('#' + idItem + '-price').text(response[idItem] * Number(price) + ' руб')
            }
            setAmount(0)
        },
        error: function(error) {}
    })

}

function deleteItem(idItem) {
    $.ajax({
        type: 'POST',
        url: 'delete/item',
        data: {'idItem': idItem},
        success: function(response) {
            $('#' + idItem + '-item').remove()
            if (response['quantity'] == 0)
                $("#iibwn").remove()

            $('#cart').text(response['quantity'] != 0 ? response['quantity'] : "")
            setAmount()
        },
        error: function(error) {}
    })
}