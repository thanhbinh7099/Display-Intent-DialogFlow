$(document).ready(function(){
    $('#submit').click(function(){
        var token = $('#inputToken').val();
        $.ajax({
            url:'http://127.0.0.1:5000/a',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                $('embed').attr('src', response);
            },
            error: function(error){
                console.log(error);
            }
        });
    });

});