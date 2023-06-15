// selector funcitonality
$('.detailprodoption').change(function () {
    var image = document.getElementById("playerOneImage").src;
    $('img[id=playerOneImage]').attr("src", $( this ).find( "option:selected" ).data( "img-src" ));

    // Title functionality 
    var selected = document.getElementById("participant1");
    var text = selected.options[selected.selectedIndex].getAttribute('data-title-var');
    var id = selected.options[selected.selectedIndex].getAttribute('data-title-id');
    document.getElementById('title_text').innerHTML = text;
    
    // show div functionality 
    var e = document.getElementById("participant1");
    var strUser = e.options[e.selectedIndex].getAttribute('data-title-var');
    console.log(strUser)
    var $div =  $("#title_1");
    if(strUser != "none" && strUser.includes('Tag'))    {
        $div.show();
    }
    else
    {
        $div.hide();
    }

    $('#titlematch_1').click(function() {
        if ($(this).prop("checked")) {
            $(this).val(id);
        } else {
            console.log('no');
            $(this).val('no');
        }
    });

});

$('.detailprodoption_2').change(function () {
    var image = document.getElementById("playerTwoImage").src;
    $('img[id=playerTwoImage]').attr("src", $( this ).find( "option:selected" ).data( "img-src" ));
    
    // Title functionality
    var selected = document.getElementById("participant2");
    var text = selected.options[selected.selectedIndex].getAttribute('data-title-var');
    var id = selected.options[selected.selectedIndex].getAttribute('data-title-id');
    document.getElementById('title_2_text').innerHTML = text;
    
    // show div functionality 
    var e = document.getElementById("participant2");
    var strUser = e.options[e.selectedIndex].getAttribute('data-title-var');
    console.log(strUser)
    var $div =  $("#title_2");
    if(strUser != "none" && strUser.includes('Tag'))    {
        {
        $div.show();
    }
    else
    {
        $div.hide();
    }

    // Set the title value from the checkbox!
    $('#titlematch_2').click(function() {
        
        if ($(this).prop("checked")) {
            console.log(document.getElementById('title_2_text').innerHTML);
            $(this).val(id);
        } else {
            console.log('no');
            $(this).val('no');
        }
    });
});


$('.detailprodoption_3').change(function () {
    var image = document.getElementById("playerThreeImage").src;
    $('img[id=playerThreeImage]').attr("src", $( this ).find( "option:selected" ).data( "img-src" ));
    
    // Title functionality
    var selected = document.getElementById("participant3");
    var text = selected.options[selected.selectedIndex].getAttribute('data-title-var');
    var id = selected.options[selected.selectedIndex].getAttribute('data-title-id');
    document.getElementById('title_3_text').innerHTML = text;
    
    // show div functionality 
    var e = document.getElementById("participant3");
    var strUser = e.options[e.selectedIndex].getAttribute('data-title-var');
    console.log(strUser)
    var $div =  $("#title_3");
    if(strUser != "none" && strUser.includes('Tag'))    {
        $div.show();
    }
    else
    {
        $div.hide();
    }

    // Set the title value from the checkbox!
    $('#titlematch_3').click(function() {
        
        if ($(this).prop("checked")) {
            console.log(document.getElementById('title_3_text').innerHTML);
            $(this).val(id);
        } else {
            console.log('no');
            $(this).val('no');
        }
    });
});

$('.detailprodoption_4').change(function () {
    var image = document.getElementById("playerFourImage").src;
    $('img[id=playerFourImage]').attr("src", $( this ).find( "option:selected" ).data( "img-src" ));
    
    // Title functionality
    var selected = document.getElementById("participant4");
    var text = selected.options[selected.selectedIndex].getAttribute('data-title-var');
    var id = selected.options[selected.selectedIndex].getAttribute('data-title-id');
    document.getElementById('title_4_text').innerHTML = text;
    
    // show div functionality 
    var e = document.getElementById("participant4");
    var strUser = e.options[e.selectedIndex].getAttribute('data-title-var');
    console.log(strUser)
    var $div =  $("#title_4");
    if(strUser != "none" && strUser.includes('Tag'))    {
        $div.show();
    }
    else
    {
        $div.hide();
    }

    // Set the title value from the checkbox!
    $('#titlematch_4').click(function() {
        
        if ($(this).prop("checked")) {
            console.log(document.getElementById('title_4_text').innerHTML);
            $(this).val(id);
        } else {
            console.log('no');
            $(this).val('no');
        }
    });
});