$(document).ready(function(){

//    checked all checkbox
    $('#check-all').click(function(){
        var c = this.checked;
        $(':checkbox').prop('checked', c);
    });

//    submit
    $('#submit').click(function(){
        var token = $('#inputToken').val();
        $.ajax({
            url:'/a',
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