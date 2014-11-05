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
            t = "/page/static/page/media"+ user + ".jpg";
            console.log(user);
            $("#usersToMeet").append("<div class='user'>"+
                                          "<img class='photoProfile' src='"+t+"'></img>"+
                                          "<label class='name'>&nbsp;&nbsp;Complete Name: "+ langs[1] + "</label>"+ "<br>"+
                                          "<label class='age'>&nbsp;&nbsp;Age: " + langs[2] + "</label>"+ "<br>"+
                                          "<label class='country'>&nbsp;&nbsp;Country: " + countries[langs[3]] + "</label>"+
                                          
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
