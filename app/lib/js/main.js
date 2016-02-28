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
                toastr["info"]("your phone will ring.", "Click2 to call", {timeOut: 3500})

            },
            success: function(data, status) {
                if (data.data.status === 1) {
                    toastr["success"]("Call in progress to " + exten, "Click to call")
                } else if(data.data.status === 500){
                    toastr["error"]("You reject call to " + exten, "Click to call")
                }
            },
            error: function(xhr, state, data){
                if (xhr.status != 400) {
                    toastr["warning"]("Unknow error durring click2call (err : "+xhr.status+')', "Error")
                } else {
                    toastr["warning"]("Click to call error : "+xhr.responseJSON.data.message+')', "Error")
                }
            }
        });
    } else {
        toastr["error"]("The phone number [" + exten +"] is not coorectly formated.", "Error")
    }
}

function create_incoming_message(call_obj){
    var mess = "from <strong>" + call_obj['caller_name'] + "</strong> <"+call_obj['caller_num']+">";
    mess += '<br>';
    mess += '<a href="https://www.google.fr/#q='+call_obj['caller_num']+'" target="_blank" class="btn btn-link">';
    mess += '<i class="fa fa-share-square-o fa-fw"></i> Google search : '+call_obj['caller_num'];
    mess += '</a>';

    return mess
}


$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip({
        container: 'body',
    })

    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
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

});