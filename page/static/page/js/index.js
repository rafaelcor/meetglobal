$(document).ready(function(){
	var slider = $('.bxslider').bxSlider({
	  mode: 'horizontal'
	});

	$('#reload-slider').click(function(e){
		e.preventDefault();
	    //$('.bxslider').append('<li><img src="{% static 'page/img/2.jpg' %}"></li>');
	    slider.reloadSlider();
	});

});