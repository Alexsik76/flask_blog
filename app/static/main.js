$(function () {
    $(window).on('beforeunload', function () {
        let user = $('meta[name=user-name]').attr('content');
        $.ajax({
            url: $SCRIPT_ROOT + '/_user_info',
            method: "POST",
            data:
                {
                    user_name: user
                },
            headers:
                {
                    'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
                },
            datatype: "json"
        });
    });
});