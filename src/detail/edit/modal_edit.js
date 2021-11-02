// This is the JS that is triggering the popup of the Modal


$('#exampleModal').on('show.bs.modal', function (event) {
    console.log('hi')
    var button = $(event.relatedTarget) // Button that triggered the modal
    var recipient = button.data('whatever') // Extract info from data-* attributes
    // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    var modal = $(this)
    modal.find('.modal-title').text(recipient)
    modal.find('.modal-body input').val(recipient)
  })