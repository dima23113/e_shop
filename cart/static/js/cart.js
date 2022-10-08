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
                        el.remove()
                        update_cart_qty()
                    }
                })
            });
            $('.icon-minus').click(function () {
                console.log($(this).data('item-id'))
                var product = $(this).data('item-id')
                var product_count = Number($('#'+ 'qty' + product).text())
                if (product_count === 1) {
                    console.log('ss');
                } else {
                    $.ajax({
                        data: {
                            'product': product,
                            'sign': '-',
                            'csrfmiddlewaretoken': csrftoken,
                            'id': product
                        },
                        url: './change-qty/',
                        method: 'post',
                        success: function (response) {
                            $('#'+ 'qty' + response['id']).html(response['qty'])
                            $('#'+ 'cost' + response['id']).html(response['total_cost'] + 'Руб.')
                            update_cart_qty()
                        }
                    })
                }
            });
            $('.icon-plus').click(function () {
                console.log($(this).data('item-id'))
                var product = $(this).data('item-id')
                var product_count = Number($('#'+ 'qty' + product).text())
                console.log(product_count)
                var max_qty = Number($('#' + product).data('quantity-available'))
                console.log(max_qty)
                if (product_count < max_qty) {
                    $.ajax({
                        data: {
                            'product': product,
                            'sign': '+',
                            'csrfmiddlewaretoken': csrftoken,
                            'id': product
                        },
                        url: './change-qty/',
                        method: 'post',
                        success: function (response) {
                            $('#'+ 'qty' + response['id']).html(response['qty'])
                            $('#'+ 'cost' + response['id']).html(response['total_cost'] + 'Руб.')
                            update_cart_qty()
                        }
                    })
                } else {
                }
            });

        }
    )
})


