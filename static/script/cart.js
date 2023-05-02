window.onload = function () {
    items = document.getElementsByClassName('row row-cols-1 row-cols-sm-2 row-cols-md-3 g-3')
    if (items.length == 0)
        return

    salary = 0
    items[0].childNodes.forEach(function(element) {
        if (element.tagName == 'DIV') {
            salary += Number(element.childNodes[1].childNodes[3].childNodes[3].textContent.split(' ')[0])
        }
    })

    payment = document.getElementsByTagName('form')[0]
    payment.childNodes[1].value = 'Совершить заказ на ' + salary + ' руб.'
}

