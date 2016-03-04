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
                    var mess = "from <strong>" + name + "</strong> <"+callObj['caller_num']+">";
                    mess += '<br>';
                    mess += getUriIfo(callObj['caller_num'])
                    toastr["info"](mess, "Icomming Call");
                    notify.showMessage(callObj['id'], 'Icomming call','from ' + name + ' <'+callObj['caller_num']+'>', getUriIfo(callObj['caller_num']))
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
                    toastr["success"](mess, "You are communicating with " + callObj['caller_num'])
                }
            });
        })

        socket.on('channels.hangup', function(data){
            var mess = notify.list[data['id']].message;
            mess += ' is hangup.';
            if (data['caller_num'] != myExtension) {        
                toastr["error"](mess, "Hangup call");
            }
            notify.list[data['id']].close();
        })
    })
    
    // to show all event
    // socket.onevent = function (packet) {
    //     console.log(packet)
    // }
});