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


function filterItems(idCategory) {
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
          <div aria-atomic="true" aria-live="assertive" class="toast position-absolute end-0 bottom-0 m-3"
           role="alert" id="myAlert">
              <div class="toast-header">
                    <strong class="me-auto">${to}</strong>
                    <small>Только что</small>
                    <button aria-label="Close" class="btn-close"
                            data-bs-dismiss="toast" type="button">
                    </button>
              </div>
              <div class="toast-body">
                  ${title} добавлен в ${to.toLowerCase()}.
              </div>
          </div>
        `.trim()
    template.innerHTML = html
    return template.content.firstChild
}

function eventMSG(to, object) {
    const title = object.parentNode.parentNode.childNodes[1].childNodes[0].textContent

    var toastEl = toast(title, to);
    document.body.appendChild(toastEl)
    const myToast = new Toast(toastEl);
    myToast.show();
}


function addCart(idItem, object) {

    eventMSG('Корзина', object)

    $.ajax({
        type: 'POST',
        url: `index/${idItem}`,
        data: {},
        success: function(response) {
            $('#cart').text(response['quantity'])
        },
        error: function(error) {}
    })
}

function addLikes(idItem, object) {

    eventMSG('Избранное', object)

    $.ajax({
        type: 'POST',
        url: `likes/${idItem}`,
        data: {},
        success: function(response) {
            $('#likes').text(response['like'])
            let template = "<img src=\"/static/icons/favorite-success.svg\" width=\"40\" height=\"40\">"
            $('#button-p-' + idItem).html(template)
            if ($('#button-r-' + idItem).length)
                $('#button-r-' + idItem).html(template)

            if ($('#button-s-' + idItem).length)
                $('#button-s-' + idItem).html(template)
        },
        error: function(error) {}
    })
}
