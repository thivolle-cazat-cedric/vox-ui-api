var MAX_CONTENT_LENGTH = 160;

function labelRemovable(number){
	return '<span class="label label-info label-tel" data-telnum="'+number+'">'+ number +' <i class="fa fa-times-circle"></i></span>'
}

$(document).ready(function() {

	$('form #phone_number').blur(function(){
		var value = $(this).val();
		if (value.split(',').length > 1) {
			var content = '' 
			value.split(',').forEach(function(num){
				content += labelRemovable(num)
			});
			$('#destnum-label').html(content)
		}
	})
	$(document).on('click', '.label-tel > .fa', function() {
		var num = $(this).parent().attr('data-telnum');
		console.log(num)
		var nums=$('form #phone_number').val().split(',');
		var content = '';
		nums.splice(nums.indexOf(num),1)
		nums.forEach(function(num){
			content += labelRemovable(num)
		});
		$('form #phone_number').val(nums.join(','))
		$('#destnum-label').html(content);
	});
	$('form #content').keyup(function(){
		$('#content-length').text($(this).val().length + " / " + MAX_CONTENT_LENGTH);
		if ($(this).val().length  > MAX_CONTENT_LENGTH){
			$(this).parent().addClass('has-error');
			// $(this).parent().parents('form').find('[type="submit"]').attr('disabled', 'disabled')
		} else {
			$(this).parent().removeClass('has-error');
			// $(this).parent().parents('form').find('[type="submit"]').removeAttr('disabled', 'disabled')
		}
	})
});