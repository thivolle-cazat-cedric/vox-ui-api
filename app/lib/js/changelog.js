$(document).ready(function() {
	var content = $("body #markdown").html().
		replace(/\[X\]/g, '<i class="fa fa-check-square-o"></i>').
		replace(/\[\s\]/g, '<i class="fa fa-square-o"></i>').
		replace(/\[\-\]/g, '<i class="fa fa-minus-square-o"></i>').
		replace(/\[(\:\w+\:)?.+\]/g, function(txt){
			var labelClass = 'default';
			var classLabelRegex = /:\w+:/

			if (classLabelRegex.test(txt)) {
				    var cl = classLabelRegex.exec(txt)[0];
				    labelClass = cl.substr(1, cl.length - 2)
				    txt = '['+txt.split(':')[2];
				}
			return '<span class="label label-'+labelClass+'">'+txt.substr(1, txt.length - 2)+'</span>'
		})

	$("body #markdown").html(content)
});