console.log("connected")

document.getElementById('removeItemForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const itemId = document.getElementById('itemId').value;
    removeFromCart(itemId);
    alert('*****Product with ID ' + itemId + ' deleted from cart\nUpdated Cart: ' + JSON.stringify(getCartItems()));
    displayCart();
});




function addToCart(item) {
    let cart = {};
    if (sessionStorage.getItem('cart')) {
        cart = JSON.parse(sessionStorage.getItem('cart'));
    }
    if (cart[item.id]) {
        cart[item.id].quantity += 1;
    } else {
        cart[item.id] = { price: item.price, quantity: 1 };
    }
    sessionStorage.setItem('cart', JSON.stringify(cart));
}
function getCartItems() {
    return JSON.parse(sessionStorage.getItem('cart')) || {};
}


function removeFromCart(itemId) {
    const cart = getCartItems();
    delete cart[itemId];
    sessionStorage.setItem('cart', JSON.stringify(cart));
}

function displayCart() {
    const cartList = document.getElementById('cartList');
    cartList.innerHTML = '';  
    const items = getCartItems();
    for (let id in items) {
        const item = items[id];
        const listItem = document.createElement('li');
        listItem.textContent = `ID: ${id} - Price: $${item.price} - Quantity: ${item.quantity}`;
        cartList.appendChild(listItem);
    }
}