$.fn.disableForm = function(){
	var item = this.find('input, textarea, select');
	item.attr('disabled', 'disabled');
};

$.fn.enableForm = function(){
	var item = this.find('input, textarea, select');
	item.removeAttr('disabled');
};
var datePickerInit = function(){
	$( "#id_birthday" ).datepicker();
}


$(document).ready(function(){
	var form = $('#perso_edit_form');
	var form_content = form.find('.form_content');
	var wait_indicator = $('.wait');
	datePickerInit();
	form.bind('submit', function(e) {
		e.preventDefault(); // <-- important
		$(this).ajaxSubmit({
			beforeSubmit: function(){
				wait_indicator.show();
				form.disableForm();
			},
			 success: function(data){
			 	wait_indicator.hide();
			 	form.enableForm();
				if ($(data).find('.errorlist').length){
					form_content.html(data);
					datePickerInit();
				}else{
					document.location = form.attr('data-success-url');
				}
			 }
		});
	});
});
	
