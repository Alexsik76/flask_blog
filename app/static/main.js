// Get info about clossed tab or window
$(window).on('beforeunload', function () {
    $.get($SCRIPT_ROOT + '_close_window_info');
});

// Auto closse alerts after 3 c
setTimeout(function () {
    let alertList = document.querySelectorAll('.alert');
    alertList.forEach(function (alert) {
        new bootstrap.Alert(alert).close();
    })
}, 3000);

// Posts cards reaction for the hover
$( ".card" ).hover(
  function() {
    $( this ).removeClass('shadow').addClass('shadow-lg');
  }, function() {
    $( this ).removeClass('shadow-lg').addClass('shadow');;
  }
);
