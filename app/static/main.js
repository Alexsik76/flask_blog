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
$(".card").hover(
    function () {
        $(this).removeClass('shadow').addClass('shadow-lg');
    }, function () {
        $(this).removeClass('shadow-lg').addClass('shadow');
    }
);

function delete_obj(row, needed_class, route) {
    let obj_id = row.find("." + needed_class).text();
    row.addClass('table-danger');
    $.get((route + obj_id), function (response) {
        if (response === "Success") {
            setTimeout(function () {
                row.remove();
            }, 1800);
        }
    });
};

//delete user
$(".user-del-btn").click(function () {
    let row = $(this).closest("tr");
    delete_obj(row, 'user-id', '/_delete_user/');
});

//delete post
$(".post-del-btn").click(function () {
    let row = $(this).closest("tr");
    delete_obj(row, 'post-id', '/_delete_post/');
});