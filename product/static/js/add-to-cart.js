document.addEventListener('DOMContentLoaded', function () {

    $('#add-to-cart').click(function () {
        let size = get_size()
        if (size === 'undefined') {

        } else {
            $.ajax({
                data: {'size': size},
                url: './add-to-cart/',
                method: 'get',
                success: function (response){
                    console.log(response)
                }
            })
        }
    })
})


function get_size() {
    let size = $('#product-size-chooser').val()
    let element = $('.product-size-chooser-message')
    let chooser = $('.product-size-chooser')
    if ((size === '') || (size === 'Выберите размер')) {
        let span = document.createElement('span').innerHTML = '<span class="error-message-size" style="color: red; ">Пожалуйста, выберите размер!</span>'
        chooser.toggleClass('product-size-chooser-error')
        element.append(span)
    } else {
        chooser.removeClass('product-size-chooser-error')
        $('.error-message-size').remove()
        return size
    }
}

