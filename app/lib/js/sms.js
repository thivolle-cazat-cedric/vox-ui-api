var MAX_CONTENT_LENGTH = 160;
var  MOBILE_LIST = [];

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
    return '<span class="label label-default label-tel" data-telnum="'+number+'">'+ name +' <i class="fa fa-times-circle"></i></span>'
}

function init(d, status) {
    var regTel = /^(\+33|0)[6-7]\d{8}$/; 
    MOBILE_LIST = [];
    $.ajax({
        url: "/contacts/all.json",
        method: "GET",
        success: function(d, status) {
            if (d.data) {
                d.data.forEach(function(el) {
                    if (regTel.test(el['telephoneNumber'])) {
                        MOBILE_LIST.push({
                            name: el['cn'],
                            num: el['telephoneNumber']
                        });
                    }
                    if (regTel.test(el['mobile'])) {
                        MOBILE_LIST.push({
                            name: el['cn'],
                            num: el['mobile']
                        });
                    }
                });
                initLabelField()
            }
        }
    });
}
function initLabelField(){
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
    $('#tagsnum').on('itemAdded', function(event) {addNum(event.item.num, event.item.name)});
    $('#tagsnum').on('itemRemoved', function(event) {$('#destnum-label [data-telnum="'+event.item.num+'"] .fa').click()});
    refreshLabelList();
    $('#destnum-label .label').each(function(){
        var $this = $(this);
        if ($this.attr('data-telnum').trim() != $this.text().trim()) {
            $('#tagsnum').tagsinput('add', {
                num:$this.attr('data-telnum'),
                name: $this.text()
            });
        }
    })
    refreshLabelList()
}

function refreshLabelList(){
    var regTel = /^\+?(\d|[\(\)]){3,}$/;
    var value = $("form #phone_number").val();
    var destList = [];
    if (value.trim().length > 1) {
        var content = '';
        value.split(',').forEach(function(num){
            if (regTel.test(num.trim()) && destList.indexOf(num.trim()) == -1){
                content += labelRemovable(num.trim());
                destList.push(num.trim())
            }
        });
        $('#destnum-label').html(content);
        $("form #phone_number").val(destList.join(','));
    } else {
        $("form #phone_number").val('');
    }
}

function addNum(num, name){
    refreshLabelList();
    var value = $("form #phone_number").val();
    var content = $('#destnum-label').html();

    if (value.trim().length > 1) {
        $("form #phone_number").val(value +','+num);
    } else {
        $("form #phone_number").val(num);
    }
    content += labelRemovable(num, name);
    $('#destnum-label').html(content);
}

$(document).ready(function() {

    $('form #phone_number').blur(refreshLabelList);
    $('#contactListModal').on('shown.bs.modal', function (e) {$('#tagsnum').tagsinput('focus')})

    $(document).on('click', '.label-tel > .fa', function() {
        var num = $(this).parent().attr('data-telnum');
        var nums=$('form #phone_number').val().split(',');
        var content = '';

        nums.splice(nums.indexOf(num),1);
        nums.forEach(function(num){content += labelRemovable(num)});
        $('form #phone_number').val(nums.join(','));
        $('#destnum-label').html(content);
        $('#tagsnum').tagsinput('remove', {num:num})
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
