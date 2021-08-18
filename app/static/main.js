$(window).on('beforeunload', function () {
    $.get($SCRIPT_ROOT + '_close_window_info');
});
setTimeout(function () {
    let alertList = document.querySelectorAll('.alert');
    alertList.forEach(function (alert) {
        new bootstrap.Alert(alert).close();
    })
}, 3000);
