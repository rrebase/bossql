function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function() {
    $('.highlight').each(function(index) {
        let editor = ace.edit(this);
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
    });

    $('.checkBtn').on('click', function(event) {
        console.log("Do it...");
        let challengeId = $(event.target).data("challengeId");
        let attemptSql = ace.edit('editor-' + challengeId).getValue();
        fetch("/challenges/check-attempt/", {
            method: "POST",
            headers: {
                'x-csrftoken': getCookie("csrftoken")
            },
            body: JSON.stringify({
                challengeId,
                attemptSql
            }),
            credentials: "include"
        })
        .then(response => response.json())
        .then(json => {
            let alertDiv = $("#alert-" + challengeId);
            if (json[0]) {
                alertDiv.attr("class", "alert mb-1 alert-success");
                alertDiv.html("<strong>Correct!</strong>");
            } else {
                alertDiv.attr("class", "alert mb-1 alert-danger");
                alertDiv.html("<strong>Incorrect.</strong>");
            }
            // thanks to: https://www.htmlgoodies.com/beyond/css/working_w_tables_using_jquery.html
            let tbody = $("#resultTbody-" + challengeId);
            tbody.empty();
            let caption = $("#nothingToShowMsg-" + challengeId);
            if (json[1] && json[2]) {
                caption.attr("class", "d-none");
                let thRow = $("<tr/>");
                for (column of json[1]) {
                    thRow.append($("<th/>").text(column));
                }
                tbody.append(thRow);
                for (row of json[2]) {
                    let tdRow = $("<tr/>");
                    for (value of row) {
                        tdRow.append($("<td/>").text(value));
                    }
                    tbody.append(tdRow);
                }
            } else {
                caption.attr("class", "");
            }
        });
    });
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
