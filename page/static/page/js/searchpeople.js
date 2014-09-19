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
    $.get( "/searchpeople_request/", function( data ) {
        console.log("Hello");
        //datal = []
        //datal.push(data.split(";"));
        console.log(data);
        $.each(data, function(user, langs, nameAndSurname){
            $("#usersToMeet").append("<div class='user'>"+
                                          //"<img src='/media/{0}.png'.format(user)></img>"+
                                          "<label class='name'>&nbsp;&nbsp;Complete Name: "+ langs[1] + "</label>"+ "<br>"+
                                          "<label class='age'>&nbsp;&nbsp;Age: " + langs[2] + "</label>"+
                                          
                                     "</div>");
            $(".user").mouseover(function(){
                $(this).addClass("selected");
            });
            $(".user").mouseout(function(){
                $(this).removeClass("selected");
            });
            $(".user").click(function(){
                console.log("More info...");
            });
        });
            
    });
    
});