$(document).ready(function(){
    String.prototype.format = String.prototype.f = function() {
        var s = this,
            i = arguments.length;

        while (i--) {
            s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
        }
        return s;
    };
    console.log("Hello");
    $.get( "/getLang_request/", function( data ) {
        console.log("Hello");
        $.each(data, function(user, langs){
            $("#usersToMeet").append("<div class='user'>"+
                                          "<img src='/media/{0}.png'.format(user)></img>"+
                                          "<label class='name'></label>"+
                                          "<label class='age'></label>"+
                                     "</div>");
        });
    });
    
});