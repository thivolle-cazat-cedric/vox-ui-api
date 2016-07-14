
var DEVICE_CLASS = {
    0: "fa fa-2x fa-fw fa-phone-square text-success",
    2: "fa fa-2x fa-fw fa-phone-square text-danger animated infinite flash",
    3: "fa fa-2x fa-fw fa-phone-square text-danger",
    5: "fa fa-2x fa-fw fa-phone-square text-muted",
    default: "fa fa-2x fa-fw fa-question-circle text-muted"
}


function getDevices(done){
    $.ajax({
        url: "/devices/json/",
        method: "GET",
        success: function(d, status) {
            if (d.data) {
                done(d.data)
            } else {
                toastr["warning"]("Erreur inatendue durant l'actualisation")
            }
        },
        error: function(xhr, state, data){
            toastr["warning"]("Réponse inatendue durant l'actualisation", "Error " +xhr.status)
        }
    });
}

function updateState(deviceId, statusName, iconClass){
    var icon = $('.vox-blf-dashbord #'+deviceId+' .icon-blf-state i')
    icon.attr('class', iconClass);
    icon.attr('data-original-title', statusName)
}
function refreshState() {
    getDevices(function(devices){
        if (typeof devices === 'object'){
            devices.forEach(function(device){
                updateState(device['id'], device['state_desc'], device['icon_class']);
            });
        }
    })
}
$(document).ready(function() {
});
