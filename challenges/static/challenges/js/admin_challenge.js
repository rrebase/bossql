
document.addEventListener('DOMContentLoaded', function() {
  let topicSelect = document.getElementById('id_topic');
  if (!topicSelect) {
    return;
  }
  let targetElem = document.querySelector('.field-source_tables .readonly');
  topicSelect.addEventListener('change', function(event) {
    if (topicSelect.value !== '') {
      targetElem.textContent = 'Loading...';
      fetch('/challenges/' + topicSelect.value + '/admin-source-tables')
        .then(resp => resp.text())
        .then(html => {
          targetElem.innerHTML = html;
        })
        .catch(err => {
          targetElem.textContent = 'Loading source tables failed.';
        });
    } else {
      targetElem.textContent = '-';
    }
  });
});
