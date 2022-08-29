function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function () {
    $(document).ready(function () {
            $('.js-product-delete').click(function () {
                var product = $(this).data('product')
                var size = $(this).data('size')
                var product_id = product + '-' + size
                $.ajax({
                    data: {'product_id': product_id, 'csrfmiddlewaretoken': csrftoken},
                    url: './remove-item/',
                    method: 'post',
                    success: function (response) {
                        console.log($(this))
                        var el = document.getElementById(response['id'])
                        el.parentNode.parentNode.parentNode.removeChild(el.parentNode.parentNode)
                        update_cart_qty()
                    }
                })
            });
            $('.icon-minus').click(function () {
                var product_count = Number($('.cart-product-quantity-value').text())
                var product = $('.cart-product').data('item-id')
                var size = $('.cart-product').data('size')
                console.log(product)
                if (product_count === 1) {
                    console.log('ss');
                } else {
                    $.ajax({
                        data: {'product': product + '-' + size, 'sign': '-', 'csrfmiddlewaretoken': csrftoken},
                        url: './change-qty/',
                        method: 'post',
                        success: function (response) {
                            product = $('.cart-product-quantity-value').html(response['qty'])
                        }
                    })
                }
            });
            $('.icon-plus').click(function () {
                var max_qty = Number($('.cart-product').data('quantity-available'))
                var product_count = Number($('.cart-product-quantity-value').text())
                var product = $('.cart-product').data('item-id')
                var size = $('.cart-product').data('size')
                if (product_count < max_qty) {
                    $.ajax({
                        data: {'product': product + '-' + size, 'sign': '+', 'csrfmiddlewaretoken': csrftoken},
                        url: './change-qty/',
                        method: 'post',
                        success: function (response) {
                            product = $('.cart-product-quantity-value').html(response['qty'])
                        }
                    })
                } else {
                }
            });

        }
    )
})


