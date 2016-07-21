var LOADCALSS = "fa-circle-o-notch fa-spin";
var REG_INTERNAL_EXTEN = /^[1-7]\d{2,3}$/


function getDeviceChanels(deviceId, done){
    $.ajax({
        url: "/devices/"+deviceId+"/channels.json",
        method: "GET",
        success: function(data, status) {
            if (Array.isArray(data.data)) {
                done(null, data.data)
            } else {
                done(400, data);
            }
        },
        error: function(xhr, state, data){
            done('error', data);
        }
    });
}

function getChannels(done){
    $.ajax({
        url: "/calls/json/",
        method: "GET",
        success: function(data, status) {
            if (Array.isArray(data.data)) {
                done(null, data.data)
            } else {
                done(400, data);
            }
        },
        error: function(xhr, state, data){
            done('error', data);
        }
    });
}

function rowChannel(channel){
    if (channel.is_incomming_call) {
        var faClass = 'fa-arrow-down';
        var directionClass = 'list-group-item-warning';
        var name = channel.caller_name;
        var num = channel.caller_num;
    } else {
        var faClass = 'fa-arrow-up';
        var directionClass = 'list-group-item-info';
        var name = channel.caller_name;
        var num = channel.caller_num;
    }

    var ret = "";
    ret += '<li class="list-group-item ' + directionClass + '" id="call-' + channel.id + '">';
    if (channel.icon_class){
        ret += '<i class="' + channel.icon_class + '"></i> &nbsp;';
    }
    ret += '<span data-whois-num="'+ num +'" data-whois-suf="  -  "></span>'+ num;
    if (name != num){
        ret += '<small> < '+ name +' ></small>';
    }
    ret += '<span class="pull-right">';
    ret += '<sub><i class="fa fa-phone"></i></sub><sup><i class="fa '+ faClass +'"></i></sup>';
    ret += '</span>';
    ret += '</li>';

    return ret;
}

function createPannel(exten, channels){
    if (Array.isArray(channels)) {
        var panel = ''; 
        panel += '<div class="col-xs-12 col-md-6">'
            panel += '<div class="panel panel-default">';
                panel += '<div class="panel-heading" role="tab" id="headingOne">';
                    panel += '<h4 class="panel-title">';
                        panel += '<a role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseOne" aria-expanded="true" aria-controls="collapseOne">';
                            panel += exten;
                            panel += '<span class="label label-default pull-right">'+ channels.length +'</span>';
                        panel += '</a>';
                    panel += '</h4>';
                panel += '</div>';
                panel += '<div id="collapseOne" class="panel-collapse collapse in" role="tabpanel" aria-labelledby="headingOne">';
                    panel += '<div class="panel-body">';
                        panel += '<ul class="list-group">';
                            channels.forEach(function(elt){
                                panel += rowChannel(elt);
                            })
                        panel += '</ul>';
                    panel += '</div>';
                panel += '</div>';
            panel += '</div>';
        panel += '</div>';
        return panel;
    } else {
        return ""
    }
    
}

function generateModalContent(view){
    var views = {}
    views.channels = function(){
        $('#mm-refresh i').removeClass('fa-refresh').addClass(LOADCALSS);
        $('#mm-refresh').attr('disabled', 'disabled');
        $('#main-modal .modal-header .modal-title').text('Appels en cours');
        getChannels(function(err, chan){
            if(!err){
                channels = {};
                chan.forEach(function(c){
                    var exten = c.exten;
                    // if(c.is_incomming_call){
                    //     if (!c.transfer_to) {
                    //         var exten = c.exten;
                    //     } else {
                    //         var exten = c.transfer_to;
                    //     }
                    // }
                    if (channels[exten] === undefined) {
                        channels[exten] = [];
                    }
                    channels[exten].push(c)
                })
                var body = '<div class="row">';
                $.each(channels, function(ext, value){
                    if (REG_INTERNAL_EXTEN.test(ext)) {
                        body += createPannel(ext, value)
                    }
                })
                body+= '</div'
                $('#main-modal .modal-body').html(body);
                $('#main-modal').modal('show');

            } else {
                toastr["warning"]("Réponse inattendue lors du chragement des appels", "Appels en cours");
            }
            $('#mm-refresh i').removeClass(LOADCALSS).addClass('fa-refresh');
            $('#mm-refresh').removeAttr('disabled')
            $('#show-channels > i ').removeClass(LOADCALSS).addClass('fa-volume-control-phone');
            findNAme();
        })
    }
    if (views[view]) {
        views[view]();
        $('#main-modal').attr('data-view', view)
    // } else {
        // $('#main-modal').attr('data-view', '')
    }
}


$(document).ready(function() {
    $("#show-channels").on('click', function(){
        $('#show-channels > i ').removeClass('fa-volume-control-phone').addClass(LOADCALSS);
        generateModalContent('channels');
    })

    $('#mm-refresh').on('click', function(){
        generateModalContent($('#main-modal').attr('data-view'))
    })

});