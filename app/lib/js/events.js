$(document).ready(function() {
    var socket = io.connect('https://api.voxity.fr/', {
        path:'/event/v1',
        query:"access_token=" + token
    });

    socket.on('connected', function(data){
        
        socket.on('channels.ringing', create_incoming_call_message)

        socket.on('channels.up', function(callObj){
            whois(callObj, function(err, callerNameList){
                var name = callObj['caller_name'] 
                if (!err && contacts[0]) {
                    name = contacts[0]['cn']
                }
                var mess = "<strong>" + name + "</strong> <"+callObj['caller_num']+">";
                mess += '<br>';
                mess += getUriIfo(callObj['caller_num'])
                toastr["success"](mess, "You are communicating with " + callObj['caller_num'])
            });
        })

        socket.on('channels.hangup', function(data){

            var mess = "Call from "+data['caller_num']
            mess += ' is hangup.'
            toastr["error"](mess, "Hangup call")
        })
    })
    
    // to show all event
    // socket.onevent = function (packet) {
    //     console.log(packet)
    // }
});