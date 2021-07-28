$(function() {
    let user = 'Unknown'
    if ($('#user-data').data() !== null){
        user = $('#user-data').data('name');
    }
    // let user = ($('#user-data').data() == null) ? 'Unknown': $('#user-data').data('name');
    console.log(user);
    $(window).on('beforeunload', function() {
        // e.preventDefault();
        $.post('/_user_info', {'user_name': user}).done(function (){
            // e.returnValue = "";
            console.log('posted');
        });
        // e.returnValue = "";
        return false;
    });
  });