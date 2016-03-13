var notifySettings  = {
	id: 'settings-notify',
	btn: $('#settings-notify'),
	icon: $("#settings-notify .fa")
};

function refreshNotify(){
	notifySettings.btn.attr('class', 'btn btn-default btn-lg btn-block');
	notifySettings.btn.text('');
	notifySettings.icon.attr('class', 'fa fa-spinner fa-spin');

	if (!notify.support()) {
		notifySettings.btn.addClass('disabled');
		notifySettings.btn.attr('disabled', 'disabled');
		notifySettings.icon.removeClass('fa-spinner fa-spin').addClass('fa-times');
		notifySettings.btn.text("Notifications non supporter par ce navigateur")
		notifySettings.btn.prepend('<i class="fa fa-times fa-fw"></i>  ')
	} else if(!notify.permited()){
		notifySettings.btn.removeClass('btn-default').addClass('btn-danger');
		notifySettings.btn.text("Notifications désactivé")
		notifySettings.btn.prepend('<i class="fa fa-square-o fa-fw"></i>  ')
	}else if(notify.permited()){
		notifySettings.btn.removeClass('btn-default').addClass('btn-success active');
		notifySettings.btn.text("Notification Activé")
		notifySettings.icon.removeClass('fa-spinner fa-spin').addClass('fa-check-square-o');
		notifySettings.btn.prepend('<i class="fa fa-check-square-o fa-fw"></i>  ')
	}else{
		notifySettings.btn.addClass('disabled').attr('disabled', 'disabled');
		notifySettings.icon.removeClass('fa-spinner fa-spin').addClass('fa-times');
	}
}
$(document).ready(function() {

	notifySettings.btn.click(function(){
		notify.showSettings();
		refreshNotify();
	})

	refreshNotify();
});