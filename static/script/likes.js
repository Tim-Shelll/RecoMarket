function deleteLikes(idItem) {
    $.ajax({
        type: 'POST',
        url: `likes/delete`,
        data: {'idItem': idItem},
        success: function(response) {
            $('#' + idItem + '-item').remove()

            count = response['likes'] == 0 ? "" : response['likes'] + (response['likes'] == 1 ? ' item' : ' items')
            let iconBag = `<img src="/static/icons/bag.svg" width="40" height="40">`
            if (response['likes'] != 0) {
                $('#likes').text(count)
            } else {
                $('#container-like').html(iconBag)
            }
        },
        error: function(error) {}
    })
}

