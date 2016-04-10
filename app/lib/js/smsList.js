function newRespons(is_resp, messageObj){
    var panel = '';
    panel += '<div class="col-xs-9" id="'+messageObj.id+'">';
        panel += '<div class="panel panel-default">';
            panel += '<div class="panel-body">';
                panel += messageObj.content
            panel += '</div>';
            panel += '<div class="panel-footer">';
                panel += '<div class="row">';
                    panel += '<div class="col-xs-1 text-left small text-muted">';
                        panel += "Réponse"
                    panel += '</div>';
                    panel += '<div class="col-xs-8">';
                    panel += '</div>';
                    panel += '<div class="col-xs-3 text-right small text-muted">';
                        panel += messageObj.send_date;
                    panel += '</div>';
                panel += '</div>';    
            panel += '</div>';
        panel += '</div>';
    panel += '</div>';

    return panel
}

$(document).ready(function() {
    $('#sms-tabs a:first').tab('show');
});

$(window).load(function(){
    $.get('/sms/json/responses', function(d) {
        if (d.data){
            d.data.forEach(function(resp){
                $('#'+resp.id_sms_sent).after(newRespons(true, resp))
            });
        }
    }).always(function(){
        $('#loading-resp').fadeOut();
    });
});
