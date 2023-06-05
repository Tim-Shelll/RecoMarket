const searchFocus = document.getElementById('search-focus');
const keys = [
  { keyCode: 'AltLeft', isTriggered: false },
  { keyCode: 'ControlLeft', isTriggered: false },
];


window.addEventListener('keydown', (e) => {
  keys.forEach((obj) => {
    if (obj.keyCode === e.code) {
      obj.isTriggered = true;
    }
  });

  const shortcutTriggered = keys.filter((obj) => obj.isTriggered).length === keys.length;

  if (shortcutTriggered) {
    searchFocus.focus();
  }
});


window.addEventListener('keyup', (e) => {
  keys.forEach((obj) => {
    if (obj.keyCode === e.code) {
      obj.isTriggered = false;
    }
  });
});


let storage = document.getElementById('items')
let statistic = document.getElementById('statistic')
let search = document.getElementById('search-focus')

search.oninput = function () {
    searchItItems()
}


function searchItItems() {
    if (search.value == "")
        onload()
    let count = 0
    storage.childNodes.forEach(function(element) {
        if (element.tagName == 'DIV' && element.style.display != 'none') {
            let text = element.childNodes[1].childNodes[3].childNodes[1].textContent

            if (text.toLowerCase().indexOf(search.value.trim().toLowerCase()) > -1) {
                element.style.display = '';
                count++;
            } else
                element.style.display = 'none'
        }
    });

    statistic.textContent = `${count} / 25`
}


function onload() {
    storage.childNodes.forEach(function(element) {
        if (element.tagName == 'DIV')
             element.style.display = ''
    })

    statistic.textContent = `25 / 25`

}


function filterItems(idCategory, name) {
    document.getElementById('dropdownMenuButton1').textContent = name
    if (search.value == "")
        onload()
    let count = 0
    if (idCategory == -1) return;
    storage.childNodes.forEach(function(element) {
        if (element.tagName == 'DIV' && element.style.display != 'none') {
            if (element.id.split('-')[2] != idCategory) {
                element.style.display = 'none'
            } else
                count++
        }
    });
    statistic.textContent = `${count} / 25`

}

const { Toast } = bootstrap;


function toast(title, to) {
    var template = document.createElement('template')
    html = `
      <div aria-atomic="true" aria-live="assertive" data-bs-delay="2500" class="toast position-fixed end-0 bottom-0 m-3"
       role="alert" id="myAlert">
          <div class="toast-header">
                <strong class="me-auto">${to}</strong>
                <small>Только что</small>
                <button aria-label="Close" class="btn-close"
                        data-bs-dismiss="toast" type="button">
                </button>
          </div>
          <div class="toast-body text-success">
              ${title}
          </div>
      </div>
    `.trim()
    template.innerHTML = html
    return template.content.firstChild
}

function eventMSG(message, to) {

    var toastEl = toast(message, to)
    document.body.appendChild(toastEl)
    const myToast = new Toast(toastEl);
    myToast.show();
}


function addCart(idItem, object) {

    $.ajax({
        type: 'POST',
        url: `index/${idItem}`,
        data: {},
        success: function(response) {
            cartFill = "<img src=\"/static/icons/cart-check.svg\" width=\"40\" height=\"40\">"
            $(`#${object.id}`).html(cartFill)

            if ($('#button-cart-ps-' + idItem).length && `button-cart-ps-${idItem}` != `${object.id}`)
                $('#button-cart-ps-' + idItem).html(cartFill)

            if ($('#button-cart-p-' + idItem).length && `button-cart-p-${idItem}` != `${object.id}`)
                $('#button-cart-p-' + idItem).html(cartFill)

            if ($('#button-cart-c-' + idItem).length && `button-cart-c-${idItem}` != `${object.id}`)
                $('#button-cart-c-' + idItem).html(cartFill)

            let iconCart = `<img src="/static/icons/cart.svg" width="40" height="40">`
            let count = response['quantity'] + (response['quantity'] == 1 ? ' item' : ' items')
            let text = `<p span id='cart' class="badge text-dark">${count}</p>`

            if (response['quantity'] == 1) {
                $('#container-cart').html(iconCart + text)
            } else {
                $('#cart').text(count)
            }

            let message= object.parentNode.parentNode.parentNode.childNodes[1].childNodes[0].textContent
            let to = `Корзина`
            eventMSG(`${message} добавлен в ${to.toLowerCase()}.`, to)

        },
        error: function(error) {}
    })


}

function addLikes(idItem, object) {
    $.ajax({
        type: 'POST',
        url: `likes/${idItem}`,
        data: {},
        success: function(response) {
            if (response['message']) {
                eventMSG(response['message'], 'Войдите в систему')
            } else {
                let message= object.parentNode.parentNode.parentNode.childNodes[1].childNodes[0].textContent
                let to = 'Избранное'
                eventMSG(`${message} добавлен в ${to.toLowerCase()}.`, to)
                $('#likes').text()
                heartFill = "<img src=\"/static/icons/heart-fill.svg\" width=\"40\" height=\"40\">"
                $(`#${object.id}`).html(heartFill)

                if ($('#button-like-ps-' + idItem).length && `button-like-ps-${idItem}` != `${object.id}`)
                    $('#button-like-ps-' + idItem).html(heartFill)

                if ($('#button-like-p-' + idItem).length && `button-like-p-${idItem}` != `${object.id}`)
                    $('#button-like-p-' + idItem).html(heartFill)

                if ($('#button-like-c-' + idItem).length && `button-like-c-${idItem}` != `${object.id}`)
                    $('#button-like-c-' + idItem).html(heartFill)

                let iconFill = `<img src="/static/icons/bag-heart.svg" width="40" height="40">`
                let count = response['like'] + (response['like'] == 1 ? ' item' : ' items')
                let text = `<p span id='likes' class="badge text-dark">${count}</p>`

                response['like'] == 1 ? $('#container-like').html(iconFill + text) : $('#likes').text(count)
            }
        },
        error: function(error) {}
    })
}
