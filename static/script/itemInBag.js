/*
document.addEventListener('DOMContentLoader', () => {
    document.getElementById("#button").onclick = (event) => {
        event.preventDefault();
        let xml = new XMLHttpRequest();
        xml.onload() => {
            const item = JSON.parse(xml.responseText);
            console.log(item)
            if (item.success) {
                console.log("Success")
            } else {
                console.log("Error")
            }

            const data = new FormData();
            data.append('')
        }
    }

})
*/