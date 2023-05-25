let object = document.getElementById('date')

datetime = object.textContent.substring(0, 19)

let months = {
    '01': 'января',    '07': 'июля',
    '02': 'февраля',   '08': 'августа',
    '03': 'марта',     '09': 'сентября',
    '04': 'апреля',    '10': 'октября',
    '05': 'мая',       '11': 'ноября',
    '06': 'июня',      '12': 'декабря'
}

let year = `${datetime.substring(0, 4)} год `
let month = `${datetime.substring(8, 10)} ${months[datetime.substring(5, 7)]} `
let time = datetime.substring(10, 16)

date.innerHTML = year + month + time
