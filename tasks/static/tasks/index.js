$(document).ready(function() {
   var editor;
   $('.highlight').each(function( index ) {
     editor = ace.edit(this);
     editor.setTheme("ace/theme/textmate");
     editor.getSession().setMode("ace/mode/sql");
     editor.container.style.lineHeight = 2;
     editor.renderer.updateFontSize();
   });
    $('.open').on('click', function () {
       openNav();
    });

    $('.closebtn').on('click', function () {
        closeNav();
    })
});

$("input[id^='checkbox-']").on('click', function() {
   var index = $(this).attr('id').split("-")[1];
   if ($('#resultTable-' + index).is(":visible")) {
      $('#resultTable-' + index).css('display', 'none');
      $('#resultTable-' + index).css('visibility', 'hidden');
   } else {
      $('#resultTable-' + index).css('display', 'block');
      $('#resultTable-' + index).css('visibility', 'visible');
   }
});
function openNav() {
    $("#mySidenav").css('width', '200px');
    $(".open").css('visibility', 'hidden');
    //$(".sidenav").css('border-right', '5px solid green');

}

function closeNav() {
    $("#mySidenav").css('width', '0px');
    $(".open").css('visibility', 'visible');
    //$(".sidenav").css('border-right', '0px solid green');

}

