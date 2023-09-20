$(document).ready(function(){

    $("#submitButton").click(function() {
    var serializedData = $("#createDataForm").serialize();
        $.ajax({
            url: $("createDataForm").data('url'),
            data: serializedData,
            type: 'post',
            success: function(response){
                console.log(response.url)
                $("#resultPhoto").html('<div class="row align-items-center"><div class="col-6 mx-auto"><div class="jumbotron card mb-1"><h2>Result</h2><br><img src="static/main/osc.png"></div></div></div>');
                window.location.hash = '#resultPhoto';
            }
        })
    });
});
