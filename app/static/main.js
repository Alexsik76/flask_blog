$(window).on('beforeunload', function () {
    $.get($SCRIPT_ROOT + '_user_info');
});