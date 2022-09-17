document.addEventListener('DOMContentLoaded', function () {

    $('#add-to-fav').click(function () {
        $.ajax({
            data: {'csrfmiddlewaretoken': csrftoken},
            url: './add-to-favorite/',
            method: 'post',
            success: function (response) {
                console.log(response)
                update_cart_qty()
            }
        })
    });
})

