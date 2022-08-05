function update_cart_qty() {
    $.ajax({
        url: 'get_cart_qty/',
        method: 'get',
        success: function (response) {
            $('.badge-qty').innerText = response['cart-qty']
        }
    })
}
