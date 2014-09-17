$(document).ready(function(){
    String.prototype.format = String.prototype.f = function() {
        var s = this,
            i = arguments.length;

        while (i--) {
            s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
        }
        return s;
    };
    //console.log("hello1")
        
    var testt = $.get( "/getLang_request/", function( data ) {
        console.log(data=="");
        if (data != ""){
            $.each(data.split(";"), function(index, item){
                $("#knownLanguages").append("<div><label>{0}</label><button class='removeLanguage'>Remove</button>                                                                  </div>".format(item));
                console.log(item);
            });
            $(".removeLanguage").click(function(){
                console.log("clicked");
                var langToRem = $(this).siblings().text();
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

    jQuery.each(window.lang, function(name, value) {
        //alert(name + ": " + value);
        $("#language").append("<option value='{0}'>{1}</option>".format(name, value));
    });
    var selectedLanguage = "";
    $("#changeLanguageButton").click(function(){
        console.log("clicked");
        selectedLanguage = $("select").val();
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