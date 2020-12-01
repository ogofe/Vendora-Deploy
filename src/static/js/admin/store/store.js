// shows the delete confimation when "DELETE" is called on an item
function confirmDelete(num) {
    document.getElementById(`popup-wrapper${num}`).classList.remove('d-none')
}


// hides the "Delete" confirmation
function hideConfirmation(num) {
    popup = document.getElementById(`popup-wrapper${num}`)
    popup.classList.add('d-none')
}


// show popup when "close store" is pressed
function confirmClose() {
    popup = document.getElementById('close-popup')
    popup.classList.remove('d-none')
}

// hide "close store" popup
function hideClose() {
    popup = document.getElementById('close-popup')
    popup.classList.add('d-none')
}


// Set the price label when priceSlider is dragged
function setPrice() {
    let value = event.target.value
    let price = document.getElementById('price')
    price.innerText = `${value}`
}


// hide items that do not match query string
function filter() {
    let count = []
    let item_count = document.getElementById('count')
    let items = Array.from(document.querySelectorAll('.item'))
    let query = event.target.value
    for (var i = 0; i < items.length; i++) {
      items[i].classList.add('d-none')
      if (items[i].firstElementChild.innerText.toLowerCase().search(query.toLowerCase()) >= 0) {
        items[i].classList.remove('d-none')
        count.push(items[i])
      }
    }
    let length = count.length
    if(length === 1){
      item_count.innerText = `${length.toString()} Item`
    } else{
      item_count.innerText = `${length.toString()} Items`
    }
}
