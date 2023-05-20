function deleteLikes(idItem) {
    $.ajax({
        type: 'POST',
        url: `likes/delete`,
        data: {'idItem': idItem},
        success: function(response) {
            $('#' + idItem + '-item').remove()
            $('#likes').text(response['likes'] == 0 ? "" : response['likes'])
        },
        error: function(error) {}
    })
}

