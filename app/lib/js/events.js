$(document).ready(function() {
    var socket = io.connect('https://api.voxity.fr/', {
        path:'/event/v1',
        query:"access_token=" + token
    });

    socket.on('connected', function(data){
        
        socket.on('channels.ringing', function(callObj){
            if (callObj['caller_num'] != myExtension) {        
                whois(callObj['caller_num'], function(err, contacts){
                    var name = callObj['caller_name'] 
                    if (!err && contacts[0]) {
                        name = contacts[0]['cn']
                    }
                    var mess = "de <strong>" + name + "</strong> <"+callObj['caller_num']+">";
                    mess += '<br>';
                    mess += getUriIfo(callObj['caller_num'])
                    toastr["info"](mess, "Appel entrant");
                    notify.showMessage(callObj['id'], 'Appel entrant','de ' + name + ' <'+callObj['caller_num']+'>', getUriIfo(callObj['caller_num']))
                });
            }
        })

        socket.on('channels.up', function(callObj){
            whois(callObj['caller_num'], function(err, callerNameList){
                var name = callObj['caller_name'] 
                if (!err && contacts[0]) {
                    name = contacts[0]['cn']
                }
                var mess = "<strong>" + name + "</strong> <"+callObj['caller_num']+">";
                mess += '<br>';
                mess += getUriIfo(callObj['caller_num'])
                if (callObj['caller_num'] != myExtension) {        
                    toastr["success"](mess, "Vous etes en communication avec " + callObj['caller_num'])
                }
            });
        })

        socket.on('channels.hangup', function(data){
            if (notify.list[data['id']] && !notify.list[data['id']]['notSend']) {
                var mess = notify.list[data['id']].message;
                mess += ' est raccroché';    
            } else {
                var mess = "Fin d'appel avec " + callObj['caller_num']
            }
            
            if (data['caller_num'] != myExtension) {        
                toastr["error"](mess, "Fin d'appel");
            }
            notify.list[data['id']].close();
        })
    })
    
    // to show all event
    // socket.onevent = function (packet) {
    //     console.log(packet)
    // }
});