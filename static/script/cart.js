function actionItem(idItem, change, price) {
    $.ajax({
        type: 'POST',
        url: `cart/${idItem}`,
        data: {'change': change},
        success: function(response) {
            $('#' + idItem).text(response[idItem]);
            $('#' + idItem + '-price').text(response[idItem] * Number(price) + ' руб.')
        },
        error: function(error) {}
    })
}
