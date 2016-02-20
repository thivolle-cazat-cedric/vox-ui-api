function filter_exten(exten){
    return exten.replace(/(\ |\-|\.|\_|\s)/g, '')
}

function generate_call(exten){
    exten = filter_exten(exten)

    var regTel = /^\+?(\d|[\(\)]){3,}$/;

    if(regTel.test(exten))
    {
        $.ajax({
            url: "/calls/generate",
            method: "POST",
            data: {'exten': exten},
            beforeSend : function(){
                toastr["info"]("Votre téléphone va sonner.", "Appel en cours")

            },
            success: function(data, status) {
                console.log(data)
                if (data.data.status === 1) {
                    toastr["success"]("Votre téléphone va sonner pour joindre le " + exten, "Appel en cours")
                } else if(data.data.status === 500){
                    toastr["error"]("Vous avez rejetez l'appel vers : " + exten, "Appel rejeté")
                }
            },
            error: function(xhr, state, data){
                console.log(xhr)
                console.log(state)
                console.log(data)
                if (xhr.status != 400) {
                    toastr["warning"]("Une erreur c'est produite, Veuillez résailler ultérieurement. (err : "+xhr.status+')', "Erreur")
                } else {
                    toastr["warning"]("Une erreur c'est produite. (err : "+xhr.responseJSON.data.message+')', "Erreur")
                }
            }
        });
    } else {
        toastr["error"]("Le numéro de téléphone [" + exten +"] n'est pas au bon format.", "Erreur")
    }
}


$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip({
        container: 'body',
    })

    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": true,
        "positionClass": "toast-bottom-right",
        "preventDuplicates": true,
        "onclick": null,
        "showDuration": "100",
        "hideDuration": "1000",
        "timeOut": "7000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "slideDown",
        "hideMethod": "slideUp"
    }

    $('#callModal').on('show.bs.modal',function(elt){$('#callModal form #telValue').val('');});
    $('#callModal').on('shown.bs.modal',function(elt){$('#callModal form #telValue').focus();});

    $('#callModal form').on('submit', function(evt) {
        evt.preventDefault();
        evt.stopPropagation();
        generate_call($('#callModal form #telValue').val())
        return false;
    });

    $('.callable').tooltip({
        title : 'Click2call',
        container: 'body',
    })

    $(document).on('click', '.callable', function(event){
        if (filter_exten($(this).text()).length > 1) {
            generate_call($(this).text());
        };
    });

    // socket.io
    var socket = io('https://api.voxity.fr/', {
        forceNew: true,
        path:'/event/v1',
        query:"access_token=" + token
    });

    socket.on('*', function(data){
        console.log(data)
    })

    socket.on('connected', function(data){
        console.log('connected', data);
    })

    socket.on('error', function(data){
        console.log('errors', data);
    })

    socket.on('calls.bridged', function(data){
        console.log('new_state.ringing', data);
    })

    socket.on('calls.ringing', function(data){
        console.log('calls.ringing', data);
    })

    socket.on('calls.hangup', function(data){
        console.log('calls.hangup', data);
    })

});