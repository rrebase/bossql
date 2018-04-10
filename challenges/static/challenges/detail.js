$.fn.extend({
  animateCss: function (animationName, callback) {
    let animationEnd = (function (el) {
      let animations = {
        animation: 'animationend',
        OAnimation: 'oAnimationEnd',
        MozAnimation: 'mozAnimationEnd',
        WebkitAnimation: 'webkitAnimationEnd',
      };

      for (let t in animations) {
        if (el.style[t] !== undefined) {
          return animations[t];
        }
      }
    })(document.createElement('div'));

    this.addClass('animated ' + animationName).one(animationEnd, function () {
      $(this).removeClass('animated ' + animationName);

      if (typeof callback === 'function') callback();
    });

    return this;
  },
});


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      let cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


$(document).ready(function () {

  $('.editor').each(function () {
    let editor = ace.edit(this);
    editor.setOptions({
      fontSize: '12pt',
      theme: 'ace/theme/chrome',
      mode: 'ace/mode/sql',
      showPrintMargin: false,
      highlightActiveLine: false,
      indentedSoftWrap: false,
    });
    editor.renderer.updateFontSize();
    editor.getSession().setUseWrapMode(true);
    editor.setValue(this.dataset.initialContent, -1);
  });

  $('body').on('mouseenter mouseleave', '.dropdown', function (e) {
    let _d = $(e.target).closest('.dropdown');
    _d.addClass('show');
    _d[_d.is(':hover') ? 'addClass' : 'removeClass']('show');
  });

  $('.checkBtn').on('click', function (event) {
    let challengeId = $(event.target).data('challengeId');
    let attemptSql = ace.edit('editor-' + challengeId).getValue();
    fetch('/challenges/check-attempt/', {
      method: 'POST',
      headers: {
        'x-csrftoken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
        challengeId,
        attemptSql,
      }),
      credentials: 'include',
    })
      .then(response => response.json())
      .then(json => {
        let alertDiv = $('#alert-' + challengeId);
        if (json[0]) {
          alertDiv.attr('class', 'alert mb-1 alert-success');
          alertDiv.animateCss('tada');
          alertDiv.html('<strong>Correct!</strong>');
        } else {
          alertDiv.attr('class', 'alert mb-1 alert-danger');
          alertDiv.animateCss('bounceIn');
          alertDiv.html('<strong>Incorrect.</strong>');
        }
        // thanks to: https://www.htmlgoodies.com/beyond/css/working_w_tables_using_jquery.html
        let tbody = $('#resultTbody-' + challengeId);
        tbody.empty();
        let caption = $('#nothingToShowMsg-' + challengeId);
        if (json[1] && json[2]) {
          caption.attr('class', 'd-none');
          let thRow = $('<tr/>');
          for (column of json[1]) {
            thRow.append($('<th/>').text(column));
          }
          tbody.append(thRow);
          for (row of json[2]) {
            let tdRow = $('<tr/>');
            for (value of row) {
              tdRow.append($('<td/>').text(value));
            }
            tbody.append(tdRow);
          }
        } else {
          caption.attr('class', '');
        }
      });
  });
});
