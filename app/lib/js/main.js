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

function whois(number, done){
    $.ajax({
        url: "/contacts/whois.json",
        method: "GET",
        data: {'number': number},
        success: function(d, status) {
            if (d.data) {
                done(null ,d.data)
            } else if(data.data.status === 500){
                done('No data in response' ,d.data)
            }
        },
        error: function(xhr, state, d){
            done('No data in responsz' ,d)
        }
    });
}

function getUriIfo(num){

    var dom = '<a href="https://www.google.fr/#q='+num+'" target="_blank" class="btn btn-link">';
    dom += '<i class="fa fa-share-square-o fa-fw"></i> Google search : '+num;
    dom += '</a>';
    return dom
}

var notify = {
    list: {},
    support:function(){
        return ("Notification" in window)
    },
    permited:function(){
        return Notification.permission === "granted"
    },
    showSettings: function(){
        Notification.requestPermission(function (permission) {
            if(!('permission' in Notification)) {
                Notification.permission = permission;
            }
        });
    },
    showMessage: function(id, title, message, uri){
        if (this.support() && this.permited()){
            this.list[id] = new Notification(title, {
                tag: id,
                icon: document.location.origin + $($('.header .img-logo')[0]).attr('src'),
                body: message,
                onclick: function(evt){evt.preventDefault(); window.open(uri, '_blank')}
            });
            this.list[id].message = message;
        }
    }
}

$(document).ready(function() {
    if (notify.support() && Notification.permission.toLowerCase() == "default") {
        notify.showSettings();
    }
    $('[data-toggle="tooltip"]').tooltip({
        container: 'body',
    })

    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": false,
        "positionClass": "toast-bottom-full-width",
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
    $('#callModal').on('hide.bs.modal',function(elt){$('#callModal form #telValue').blur();});

    $('#callModal form').on('submit', function(evt) {
        evt.preventDefault();
        evt.stopPropagation();
        generate_call($('#callModal form #telValue').val())
        $('#callModal form #telValue').val('')
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

    $(document).keypress(function(event) {
        if (!event.metaKey) {
            var tag = event.target.tagName.toLowerCase();
            // r
            if (tag != 'input' && event.charCode == 114 && typeof refreshState == 'function') {refreshState()}
            // c
            else if (tag != 'input' && event.charCode == 99) {$('#callModal').modal('show')}
        }
    });

});