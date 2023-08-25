$('.detailprodoption').change(function () {
    doathing(this.id, this)
    console.log(this.id)
 });

function doathing(thing,item) {
    console.log(thing)
    $(`img[id=${thing}Image]`).attr("src", $( item ).find( "option:selected" ).data( "img-src" ));

    // Title functionality 
    var selected = document.getElementById(thing);
    var text = selected.options[selected.selectedIndex].getAttribute('data-title-var');
    var id = selected.options[selected.selectedIndex].getAttribute('data-title-id');
    document.getElementById(`title_text_${thing}`).innerHTML = text;
    
    // show div functionality 
    var e = document.getElementById(thing);
    var strUser = e.options[e.selectedIndex].getAttribute('data-title-var');
    // console.log(strUser)
    var $div =  $(`#title_${thing}`);
    if(strUser != "none")    {
        $div.show();
    }
    else
    {
        $div.hide();
    }

    $(`#titlematch_${thing}`).click(function() {
        if ($(this).prop("checked")) {
            $(this).val(id);
        } else {
            console.log('no');
            $(this).val('no');
        }
    });    
}