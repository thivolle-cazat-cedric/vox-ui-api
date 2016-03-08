
function getDevices(done){
    $.ajax({
        url: "/devices/json/",
        method: "GET",
        success: function(d, status) {
            if (d.data) {
                done(d.data)
            } else {
                toastr["warning"]("Unknow error on refresh devices state")
            }
        },
        error: function(xhr, state, data){
            toastr["warning"]("Unknow error on refresh devices state", "Error " +xhr.status)
        }
    });
}

function updateState(deviceId, statusName, iconClass){
    var icon = $('.vox-blf-dashbord #'+deviceId+' .icon-blf-state i')
    icon.attr('class', iconClass);
    icon.attr('data-original-title', statusName)
}
function refreshState() {
    var icon = $("#refresh-dashboard .fa")
    icon.addClass('fa-spin')
    getDevices(function(devices){
        if (typeof devices === 'object'){
            devices.forEach(function(device){
                updateState(device['id'], device['state_desc'], device['icon_class']);
            });
        }
        icon.removeClass('fa-spin');
    })
}
$(document).ready(function() {
    $("#refresh-dashboard").click(refreshState);
});

// var ring = 'fa fa-2x fa-fw fa-phone-square text-danger animated infinite flash'