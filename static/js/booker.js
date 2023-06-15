$('select').on('change', function(){
    $('select option').prop("disabled", false);
    $("select").not(this).find("option[value='"+ $(this).val() + "']").prop('disabled', true);
});

var pro = $('#properties').find("option[value='"+user_property.replace(' ','-')+"']");

