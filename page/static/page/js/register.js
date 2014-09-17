$(document).ready(function () {
    $("button").click(function(){
        var name = $("#iname").val();
        var surname = $("#isurname").val();
        var email = $("#iemail").val();
        var password = $("#ipassword").val();
        var country = $("select").val();

            var obj = {"name" : name,
                       "surname" : surname,
                       "email": email,
                       "password": password,
                       "country": country,
                       'csrfmiddlewaretoken': $.cookie('csrftoken')}

            $.post("/register_request/", obj, function(data){
                console.log(data["register"]);
                
                if (data["register"] == "wrong"){
                    //$(".register_form").css("display", "none");
                    $("#okornot").css("display", "block");
                    $("#okornot").css("color", "red")
                    $("#okornot").text("Ha insertado datos no correctos, por favor intente nuevamente");
                }
                else{
                    $(".register_form").css("display", "none");
                    $("#okornot").css("display", "block");
                    $("#okornot").css("color", "green")
                    $("#okornot").text("Gracias por registrarse en Meet Global, se le va a enviar un correo de activacion.");
                }
            });
    })
});