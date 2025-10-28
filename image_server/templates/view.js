document.addEventListener('keydown', function(e) {
  if (e.key === 'ArrowLeft') {
    e.preventDefault();
    var prevLink = document.querySelector('.nav.prev');
    if (prevLink) {
      window.location = prevLink.href;
    }
  } else if (e.key === 'ArrowRight') {
    e.preventDefault();
    var nextLink = document.querySelector('.nav.next');
    if (nextLink) {
      window.location = nextLink.href;
    }
  } else if (e.key === 'd' || e.key === 'D' || e.key === 'Delete') {
    e.preventDefault();
    var form = document.querySelector('form');
    if (form) {
      form.submit();
    }
  }
});

