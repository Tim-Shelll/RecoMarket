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
            let cart = ""
            response['cart'].forEach(function(item) {
                cart += "" +
                    `<div class=\"card rounded-3 mb-4\" id=\"${item['idItem']}-item\">\n` +
                    "   <div class=\"card-body p-4\">\n" +
                    "       <div class=\"row d-flex justify-content-between align-items-center\">\n" +
                    "           <div class=\"col-md-2 col-lg-2 col-xl-2\">\n" +
                    `               <img src=\"${item['img']}\" class=\"img-fluid rounded-3\">\n` +
                    "           </div>\n" +
                    "           <div class=\"col-md-3 col-lg-3 col-xl-3\">\n" +
                    `               <p class=\"lead fw-normal mb-2\">${item['title']}</p>\n` +
                    "           </div>\n" +
                    "           <div class=\"col-md-3 col-lg-3 col-xl-2 d-flex\">\n" +
                    "               <button class=\"btn btn-link px-2\"\n" +
                    `                   onclick=\"actionItem(${item['idItem']}, -1, ${item['price']})\">\n` +
                    "                   <img src=\"/static/icons/minus.svg\" width=\"15\" height=\"15\">\n" +
                    "               </button>\n" +
                    `               <span id='${item['idItem']}' class=\"badge bg-dark rounded-pill\"\n` +
                    `                   style=\"line-height: 50px; font-size: 20px\">${item['numItem']}\n` +
                    "               </span>\n" +
                    "               <button class=\"btn btn-link px-2\"\n" +
                    `                   onclick=\"actionItem(${item['idItem']}, 1, ${item['price']})\">\n` +
                    "                   <img src=\"/static/icons/plus.svg\" width=\"15\" height=\"15\">\n" +
                    "               </button>\n" +
                    "           </div>\n" +
                    "           <div class=\"col-md-3 col-lg-2 col-xl-2 offset-lg-1\">\n" +
                    `               <h5 id='${item['idItem']}-price' class=\"mb-0\">\n` +
                    `${item['price'] * item['numItem']} руб.\n` +
                    `               </h5>\n` +
                    "           </div>\n" +
                    "           <div class=\"col-md-1 col-lg-1 col-xl-1 text-end\">\n" +
                    "               <button style=\"font-size : 100%;\" class=\"badge bg-light rounded-pill\"\n" +
                    `                   onclick=\"deleteItem(${item['idItem']})\">\n` +
                    "                   <img src=\"/static/icons/trash.svg\" width=\"20\" height=\"20\">\n" +
                    "               </button>\n" +
                    "           </div>\n" +
                    "       </div>\n" +
                    "   </div>\n" +
                    "</div>"
            })

            cart != "" ? $('#items').html(cart) : $('#iibwn').html("")
            $('#cart').text(response['quantity'] != 0 ? response['quantity'] : "")
            setAmount()
        },
        error: function(error) {}
    })
}