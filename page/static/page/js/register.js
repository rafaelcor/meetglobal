$(document).ready(function () {
    
    $('#datepicker').datepicker({
            dateFormat: 'yy-mm-dd',
            yearRange: "-100:+0",
            changeYear: true,
            inline: true,
            altField: '#datepicker_value',
            onSelect: function(){
                var day1 = $("#datepicker").datepicker('getDate').getDate();                 
                var month1 = $("#datepicker").datepicker('getDate').getMonth() + 1;             
                var year1 = $("#datepicker").datepicker('getDate').getFullYear();
                window.date = year1 + "-" + month1 + "-" + day1;
                //var str_output = "<h1><center><img src=\"/images/a" + fullDate +".png\"></center></h1><br/><br>";
                //$('#page_output').html(str_output);
            }
        });
    $("button").click(function(){
        var name = $("#iname").val();
        var surname = $("#isurname").val();
        var email = $("#iemail").val();
        var password = $("#ipassword").val();
        var country = $("select").val();

            var obj = {"name" : name,
                       "surname" : surname,
                       "date_of_birth" : window.date,
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
