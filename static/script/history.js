function onClickHistory(object) {
    object.parentNode.childNodes.forEach(function(node) {
        if (node.tagName == 'DIV') {
            node.style.display = (node.style.display != 'none') ? 'none' : ''
        }
    })
}
