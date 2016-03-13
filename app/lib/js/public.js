$(document).ready(function() {
	$('[data-toggle="tooltip"], abbr').tooltip()
	$('#btn-get-started').hover(function(){
		$(this).addClass('btn-success');
		$(this).removeClass('btn-default');
		$(this).find('img').hide();
		$(this).find('i').show()
	}, function(){
		$(this).removeClass('btn-success');
		$(this).addClass('btn-default');
		$(this).find('img').show();
		$(this).find('i').hide()
	});
});