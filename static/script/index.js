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


let storage = document.getElementById('album py-5 bg-light')
let container = storage.childNodes[1].childNodes[1].childNodes

let search = document.getElementById('search-focus')
let statistics = document.getElementsByClassName('input-group')[0]
statistics = statistics.childNodes[statistics.childNodes.length - 2]


search.oninput = function () {
    searchItItems()
}


function searchItItems() {
    onload()
    let count = 0
    container.forEach(function(element) {
        if (element.tagName == 'DIV' && element.style.display != 'none') {
            let text = element.childNodes[1].childNodes[3].childNodes[1].textContent

            if (text.toLowerCase().indexOf(search.value.trim().toLowerCase()) > -1) {
                element.style.display = '';
                count++;
            } else
                element.style.display = 'none'
        }
    });
    console.log(count)
    statistics.innerHTML = `${count} / 25`
}


function onload() {
    container.forEach(function(element) {
        if (element.tagName == 'DIV')
             element.style.display = ''
    })

    statistics.innerHTML = "25 / 25"
}


function filterItems(idCategory) {
    onload()
    let count = 0
    if (idCategory == -1) return;
    container.forEach(function(element) {
        if (element.tagName == 'DIV' && element.style.display != 'none') {
            let text = element.childNodes[1].childNodes[3].childNodes[5].childNodes[1].childNodes[1].value
            if (text == idCategory ) {
                element.style.display = '';
                count++;
            } else
                element.style.display = 'none'
        }
    });
    statistics.innerHTML = `${count} / 25`
}


function addCart(idItem) {
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

function addLikes(idItem) {
    $.ajax({
        type: 'POST',
        url: `likes/${idItem}`,
        data: {},
        success: function(response) {
            $('#likes').text(response['like'])
            let template = "<img src=\"/static/icons/favorite-success.svg\" width=\"40\" height=\"40\">"
            $('#button-p-' + idItem).html(template)
            if ($('#button-r-' + idItem).length) {
                $('#button-r-' + idItem).html(template)
            }
        },
        error: function(error) {}
    })
}
