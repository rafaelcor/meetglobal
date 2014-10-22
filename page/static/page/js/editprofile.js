$(document).ready(function(){
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

    String.prototype.format = String.prototype.f = function() {
        var s = this,
            i = arguments.length;

        while (i--) {
            s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
        }
        return s;
    };
    //console.log("hello1")

    for(x in countries){
        $("#country").append("<option value='"+x+"'>"+countries[x]+"</option>");
    }
    var country;
    $.post( "/editprofile/", {'action':'get_country', 'csrfmiddlewaretoken': $.cookie('csrftoken')}, function(data){
        $("#country").val(data);
    });
        
    var testt = $.get( "/getLang_request/", function( data ) {
        console.log(data=="");
        if (data != ""){
            $.each(data.split(";"), function(index, item){
                $("#knownLanguages").append("<div><label>{0}</label><button class='removeLanguage btn btn-default' id='language_{1}'>Remove</button>                                                                  </div>".format(window.lang[item], item));
                console.log(item);
            });
            $(".removeLanguage").click(function(){
                console.log("clicked");
                var langToRem = $(this)[0].id.replace("language_", "");
                var obj = {"lang": langToRem,
                           'csrfmiddlewaretoken': $.cookie('csrftoken')}
                $.post("/removeLang_request/", obj, function(data){
                    console.log("rmvlr");
                    $(location).attr('href', "/editprofile");
                });
            });
        }
        else{
            
        }
    });

    $("#save_changes").click(function(){
        var obj = {"action": "change_profile",
                   "name": $("#iname").val(),
                   "surname": $("#isurname").val(),
                   "date_of_birth": $("#datepicker").val(),
                   "email": $("#iemail").val(),
                   "country": $("#country").val(),
                   'csrfmiddlewaretoken': $.cookie('csrftoken')}

        $.post("/editprofile", obj, function(data){
            $(location).attr('href', "/editprofile");
        });

    });

    $("#reset_changes").click(function(){
        $(location).attr('href', "/editprofile");
    });

    $("#changePassword").click(function(){
        if($("#changePassword").val() != $("#confirmPassword").val()){
            $("#bad_confirm")[0].style.display="inline";
        }
        else{
            $("#bad_confirm")[0].style.display="none";
        }
    });

    $("#confirmPassword").click(function(){
        if($("#changePassword").val() != $("#confirmPassword").val()){
            $("#bad_confirm")[0].style.display="inline";
        }
        else{
            $("#bad_confirm")[0].style.display="none";
        }
    });

    $("#save_password").click(function(){
        if($("#changePassword").val() != $("#confirmPassword").val()){
            return;
        }
        var obj = {"action": "change_password",
                   "actual": $("#actualPassword").val(),
                   "new": $("#changePassword").val(),
                   'csrfmiddlewaretoken': $.cookie('csrftoken')}

        $.post("/editprofile", obj, function(data){
            $(location).attr('href', "/editprofile");
        });

    });

    jQuery.each(window.lang, function(name, value) {
        //alert(name + ": " + value);
        $("#language").append("<option value='{0}'>{1}</option>".format(name, value));
    });
    var selectedLanguage = "";
    $("#changeLanguageButton").click(function(){
        console.log("clicked");
        selectedLanguage = $("select#language").val();
        var obj = {"language": selectedLanguage, 
                   'csrfmiddlewaretoken': $.cookie('csrftoken')}

        $.post("/addLang_request/", obj, function(data){
            console.log("hello");
            console.log(data);
            console.log("hello");
            $(location).attr('href', "/editprofile");
        });

    });
});
