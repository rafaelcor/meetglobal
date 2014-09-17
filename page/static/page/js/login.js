$(document).ready(function () {
    $("button").click(function(){
        var email = $("#iemail").val();
        var password = $("#ipassword").val();

            var obj = {"email": email,
                       "password": password,
                       'csrfmiddlewaretoken': $.cookie('csrftoken')}

            $.post("/login_request/", obj, function(data){
                
                if (data["register"] == "wrong"){
                    //$(".register_form").css("display", "none");
                    $("#okornot").css("display", "block");
                    $("#okornot").css("color", "red")
                    $("#okornot").text("Ha insertado datos no correctos, por favor intente nuevamente");
                }
                else{
                    console.log("login ok");
                    $(location).attr('href', "/");
                }
            });
    })
});