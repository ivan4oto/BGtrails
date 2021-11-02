// This is the JS that is getting the data from the Modal and then doing
// the ajax request to send the data to the update view on the server.


// AJAX for posting
function create_post() {
    console.log("create post is working!") // sanity check
    console.log($('#trail-name').val())
};

// Submit post on submit
$('#post-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")
    create_post();
    });

// AJAX for posting
function create_post() {
    console.log("create post is working!") // sanity check
    var trailName = $('#trail-name').val()
    var trailDistance = $('#trail-distance').val()
    var trailElevation = $('#trail-elevation').val()
    var trailDescription = $('#trail-description').val()
    $.ajax({
        url : editUrl, // the endpoint
        type : "POST", // http method
        data : {
            trail_name: trailName,
            trail_elevation: trailElevation,
            trail_distance: trailDistance,
            trail_description: trailDescription
        }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#exampleModalLabel').text("Успешна промяна")
            $('#exampleModalLabel').css({ 'color': 'green'});
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            // $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
            //     " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            $('#exampleModalLabel').text("Промяната е неуспешна")
            $('#exampleModalLabel').css({ 'color': 'red'}); // provide a bit more info about the error to the console
        }
    });
};