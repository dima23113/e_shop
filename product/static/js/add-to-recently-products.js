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

function add_to_rv_product() {
    $.ajax({
        data: {'csrfmiddlewaretoken': csrftoken},
        url: './add-to-recently-viewed/',
        method: 'post',
        success: function (response) {
            console.log(response)
        }
    })
}


add_to_rv_product()