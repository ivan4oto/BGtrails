var userName = "{{ user.get_username }}"
var csrfToken = "{{ csrf_token }}"
var favUrl = "{% url 'favourite-trail' object.id %}"

$("#fav-button").click(function () {
    $.ajax({
        type: 'POST',
        url: "{% url 'favourite-trail' object.id %}",
        data: {
            user: userName,
            csrfmiddlewaretoken: csrfToken
        },
        success: function (response) {
          console.log('success')                  
            // display the newly friend to table.
            var instance = JSON.parse(response["is-fav"]);
        },
        error: function (response) {
            // alert the error if any error occured
            alert(response["responseJSON"]["error"]);
        }
    })
})