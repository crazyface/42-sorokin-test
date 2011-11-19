$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

$.fn.addThanHide = function(){
	return $(this).clone().delay(2000).fadeOut();
}

$(document).ready(function(){
	var ajax_spiner = $('#ajax_spiner');
	var ajax_success = $('#ajax_success');
	var ajax_error = $('#ajax_error');
	$('#req_formset input[type="submit"]').hide();
	$('.request_form select').bind('change', function(event){
		var target = $(this);
		var form = target.parents('.request_form');
		var ajax_status = form.find('.ajax_status')
		var inputs = form.find('input, textarea, select');
		var data = {};
		for(var i = 0, length = inputs.length; i<length; i++){
			var input = $(inputs[i]);
			data[input.attr('name').match(/-\d+-(.*)$/)[1]] = input.val()
		}
		$.ajax({
		  url: document.location.href,
		  type: 'POST',
		  data: data,
		  dataType: 'json',
		  beforeSend: function(){
		  	ajax_status.html(ajax_spiner);
		  },
		  success: function(response){
		  	if(response.status == 'success'){
		  		ajax_status.html(ajax_success.addThanHide());
		  	}else{
		  		ajax_status.html(ajax_error.addThanHide());
		  	}
		  },
		  error: function(){
		  	ajax_status.html(ajax_error.addThanHide());
		  }
		});
	});
})
