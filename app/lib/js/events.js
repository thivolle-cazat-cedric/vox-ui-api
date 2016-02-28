$(document).ready(function() {
    var socket = io.connect('https://api.voxity.fr/', {
        path:'/event/v1',
        query:"access_token=" + token
    });

    socket.on('connected', function(data){
        
        socket.on('channels.ringing', create_incoming_call_message})

        socket.on('channels.up', function(data){
            var mess = create_incoming_call_message(data).split('<br>')[1];
            toastr["success"](mess, "You are communicating with " + data['caller_num'])
        })

        socket.on('channels.hangup', function(data){
            var mess = "Call from" + data['caller_name'] + "</strong> <"+data['caller_num']+">"
            mess += "<br>"
            mess += 'is hangup.'
            toastr["error"](mess, "Hangup call")
        })
    })
    
    // to show all event
    // socket.onevent = function (packet) {
    //     console.log(packet)
    // }
});