
function onclickYear(year) {
    button = document.getElementById(year).parentElement.parentElement.children
    for (let idx = 1; idx < button.length; idx++) {
        button[idx].style.display = (button[idx].style.display != 'none') ? 'none' : ''
    }
}

function onclickMonth(year, day, month) {
    month = document.getElementById(`${year}_${day}_${month}`).parentElement.children
    for (let idx = 1; idx < month.length; idx++) {
        month[idx].style.display = (month[idx].style.display != 'none') ? 'none' : ''
    }
}
