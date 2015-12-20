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
            dataType: "text/json",
            data: {'exten': exten},
            success: function(data, status) {
                console.log(data)
                toastr["success"]("Votre téléphone va sonner pour joindre le " + exten, "Numérotation en cours")
            },
            error: function(xhr, state, data){
                if (xhr.status != 400) {
                    toastr["warning"]("Une erreur c'est produite, Veuillez résailler ultérieurement. (err : "+xhr.status+')', "Erreur")
                } else {
                    console.log('nop')
                }
            }
        });
    } else {
        toastr["error"]("Le numéro de téléphone [" + exten +"] n'est pas au bon format.", "Erreur")
    }
}


$(document).ready(function() {

    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": true,
        "positionClass": "toast-bottom-center",
        "preventDuplicates": true,
        "onclick": null,
        "showDuration": "300",
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

    $(document).on('click', '.callable', function(event){
        if (filter_exten($(this).text()).length > 1) {
            generate_call($(this).text());
        };
    })
});