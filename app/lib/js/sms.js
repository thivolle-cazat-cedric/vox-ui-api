var MAX_CONTENT_LENGTH = 160;
var  MOBILE_LIST = [];

/**
 * Retrun
 * @param  {String} number the number associate in this tag
 * @param  {String} name   *optional* - The name diaplay on tag (if undefined, search in MOBILE_LIST, if nothing match number is display)
 * @return {object}        Dom object (span.label)
 */
function labelRemovable(number, name){

    var findeName = MOBILE_LIST.filter(function(obj) {return (obj.num == number);});
    if (name === undefined && !findeName) {
        name = number;
    } else {
        var i = 0;
        var loop = true;
        while (findeName.length > i && loop){
            if (findeName[i].num == number) {
                name = findeName[i].name;
                loop = false;
            } else {i++}
        }
        if (loop) {name = number;}
    }
    return $('<span>',{'class': 'label label-primary label-tel','data-telnum': number}).text(name).append($('<i>', {class:'fa fa-times-circle'}));
}

/**
 * init contact autocompletion
 * @return {[type]} [description]
 */
function init() {
    $('[data-target="#contactListModal"]').attr('disabled', 'disabled');
    var mobileReg = /^(\+33|0)[6-7]\d{8}$/; 
    MOBILE_LIST = [];
    $.ajax({
        url: "/contacts/all.json",
        method: "GET",
        success: function(d, status) {
            if (d.data) {
                d.data.forEach(function(el) {
                    if (mobileReg.test(el['telephoneNumber'])) {
                        MOBILE_LIST.push({
                            name: el['cn'],
                            num: el['telephoneNumber']
                        });
                    }
                    if (mobileReg.test(el['mobile'])) {
                        MOBILE_LIST.push({
                            name: el['cn'],
                            num: el['mobile']
                        });
                    }
                });
                var contactSrc = new Bloodhound({
                    local: MOBILE_LIST,
                    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
                    queryTokenizer: Bloodhound.tokenizers.whitespace,
                });
                contactSrc.initialize();

                $('#tagsnum').tagsinput({
                    itemValue: 'num',
                    itemText: 'name',
                    freeInput: true,
                    typeaheadjs: {
                        freeInput: true,
                        displayKey: 'name',
                        source: contactSrc.ttAdapter(),
                        itemText: 'name',
                        itemValue: 'num',
                    }
                });
                refreshLabelList();
                $('#tagsnum').on('itemAdded', function(event) {
                    if($('#destnum-label [data-telnum="'+event.item.num+'"]').length == 0){
                        addNum(event.item.num, event.item.name);
                    }
                });
                $('#tagsnum').on('itemRemoved', function(event) {try{ $('#destnum-label [data-telnum="'+event.item.num+'"] .fa').click()} catch(e){}});
                $('#destnum-label .label').each(function(){
                    var $this = $(this);
                    if ($this.attr('data-telnum').trim() != $this.text().trim()) {
                        $('#tagsnum').tagsinput('add', {
                            num:$this.attr('data-telnum'),
                            name: $this.text()
                        });
                    }
                })
                $('[data-target="#contactListModal"]').removeAttr('disabled');
            } else {
                toastr["warning"]("Réponse innatendu lors du chargement des contact", "Chargement des contacts")
            }
        },
        error: function(){
            toastr["warning"]("Réponse innatendu lors du chargement des contact", "Chargement des contacts")
        }
    });
}

function refreshLabelList(){
    var regTel = /^\+?(\d|[\(\)]){3,}$/;
    var value = $("form #phone_number").val();
    var destList = [];
    $('#destnum-label').html('');
    $('#tagsnum').tagsinput('removeAll')
    if (value.trim().length > 0) {
        value.split(',').forEach(function(num){
            num = num.trim();
            if (regTel.test(num) && destList.indexOf(num) == -1){
                $('#destnum-label').append(labelRemovable(num));
                destList.push(num)
            }
        });
        $('#destnum-label .label').each(function() {
            var $this = $(this);
            if($this.attr('data-telnum') != $this.text().trim()){
                $('#tagsnum').tagsinput('add', {num:$this.attr('data-telnum') , name: $this.text().trim()});
            }
        });
        $("form #phone_number").val(destList.join(','));
    } else {$("form #phone_number").val('');}
    refreshSmsLength();
}

function refreshSmsLength(){
    var smsLengthTxt = '';
    var smsLength = $('#destnum-label .label').length;
    if (smsLength) {
        smsLengthTxt += smsLength + ' message';
        if (smsLength > 1) {
            smsLengthTxt += 's';
        }
        $("#sms-length").text(smsLengthTxt);
        $("#sms-length").fadeIn();
    } else {
        $("#sms-length").fadeOut();
    }
       
}

function addNum(num, name){
    if($('#destnum-label [data-telnum="'+num+'"]').length == 0) {
        var value = $("form #phone_number").val();
        if (value.trim().length > 1) {
            $("form #phone_number").val(value +','+num);
        } else {
            $("form #phone_number").val(num);
        }
        refreshLabelList();
        refreshSmsLength();        
    }

}

function removeNum(num){
    var nums = $('form #phone_number').val().split(',');

    if (nums.indexOf(num) > -1) {
        nums.splice(nums.indexOf(num),1);
        $('form #phone_number').val(nums.join(','));
        $('#tagsnum').tagsinput('remove', {num:num})
        refreshLabelList();
    }
    
}

$(document).ready(function() {

    $('form #phone_number').blur(refreshLabelList);
    $('#contactListModal').on('shown.bs.modal', function (e) {
        $('#tagsnum').tagsinput('focus');
        $('[data-target="#contactListModal"]').addClass('active');
    })
    $('#contactListModal').on('hide.bs.modal', function (e) {$('[data-target="#contactListModal"]').removeClass('active');})

    $('form[method="POST"] [type="submit"]').click(function(){
        $(this).attr('disabled', 'disabled');
        $('form[method="POST"] [type="submit"] .fa').removeClass('fa-paper-plane-o').addClass('fa-spinner fa-spin');
        $('form[method="POST"]').submit();
    })

    $(document).on('click', '.label-tel > .fa', function() {
        removeNum($(this).parent().attr('data-telnum'));
    });

    $('form #content').keyup(function(){
        $('#content-length').text($(this).val().length + " / " + MAX_CONTENT_LENGTH);
        if ($(this).val().length  > MAX_CONTENT_LENGTH){
            $(this).parent().addClass('has-error');
        } else {
            $(this).parent().removeClass('has-error');
        }
    })
});

init();
