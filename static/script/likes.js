function deleteLikes(idItem) {
    $.ajax({
        type: 'POST',
        url: `likes/delete`,
        data: {'idItem': idItem},
        success: function(response) {
            let favorites = ""
            response['favorites'].forEach(function(favorite) {
                favorites += "" +
                    "<div class=\"flex_row\">\n" +
                    "   <div class=\"card shadow-sm bg-white rounded border\">\n" +
                    `       <img class=\"img\" src=${favorite['img']}>\n` +
                    "       <div class=\"card-body\">\n" +
                    `           <p class=\"card-text\"><b>${favorite['title']} </b></p>\n` +
                    `           <p class=\"card-text\"><h5>${favorite['price']} руб. </h5></p>\n` +
                    "           <button class=\"badge bg-dark rounded-pill\"\n" +
                    `                   onclick=\"deleteLikes(${favorite['idItem']})\">\n` +
                    "               Удалить из избранных\n" +
                    "           </button>\n" +
                    "       </div>\n" +
                    "   </div>\n" +
                    "</div>"
            })

            $('#likes').text(response['likes'] == 0 ? "" : response['likes'])
            $('#favorites').html(favorites)

        },
        error: function(error) {}
    })
}

