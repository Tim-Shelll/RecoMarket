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


function check() {
    if (search.value == "") {
        onload()
        return;
    }
}


search.oninput = function () {
    check();
}


function searchItItems() {
    check();
    onload();

    container.forEach(function(element) {
        if (element.tagName == 'DIV' && element.style.display != 'none') {
            let text = element.childNodes[1].childNodes[3].childNodes[1].textContent

            if (text.toLowerCase().indexOf(search.value.trim().toLowerCase()) > -1) {
                element.style.display = ''
            } else {
                element.style.display = 'none'
            }

        }
    });
}


function onload() {
    container.forEach(function(element) {
        if (element.tagName == 'DIV') {
             element.style.display = ''
        }
    })
}


function filterItems(idCategory) {
    onload();
    if (idCategory == -1)
        return;
    container.forEach(function(element) {
        if (element.tagName == 'DIV' && element.style.display != 'none') {
            let text = element.childNodes[1].childNodes[3].childNodes[5]
                .childNodes[1].childNodes[1].value
            element.style.display = (text == idCategory) ?  '' : 'none'
        }
    });
}