function initializeSizeSelector() {
  var savedSize = localStorage.getItem('thumbnailSize') || 'small';
  applySizeClass(savedSize);

  var buttons = document.querySelectorAll('.size-btn');
  buttons.forEach(function(btn) {
    if (btn.dataset.size === savedSize) {
      btn.classList.add('active');
    }
    btn.addEventListener('click', function() {
      var size = this.dataset.size;
      saveThumbnailSize(size);
      applySizeClass(size);
      updateActiveButton(buttons, this);
    });
  });
}

function saveThumbnailSize(size) {
  localStorage.setItem('thumbnailSize', size);
}

function applySizeClass(size) {
  document.body.className = 'size-' + size;
}

function updateActiveButton(buttons, activeBtn) {
  buttons.forEach(function(btn) {
    btn.classList.remove('active');
  });
  activeBtn.classList.add('active');
}

function saveScrollPosition() {
  localStorage.setItem('scrollPosition', window.scrollY.toString());
}

function restoreScrollPosition() {
  var savedScroll = localStorage.getItem('scrollPosition');
  if (savedScroll) {
    window.scrollTo(0, parseInt(savedScroll));
    localStorage.removeItem('scrollPosition');
  }
}

function setupImageLinks() {
  var links = document.querySelectorAll('.card-link');
  links.forEach(function(link) {
    link.addEventListener('click', function() {
      saveScrollPosition();
    });
  });
}

function deleteImage(event, name, skipConfirm) {
  event.preventDefault();
  event.stopPropagation();
  if (!skipConfirm && !confirm('Delete "' + name + '"?')) return;

  var card = event.target.closest('.card');

  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/delete', true);
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.onload = function() {
    if (xhr.status === 303 || xhr.status === 200) {
      if (card) {
        card.style.opacity = '0';
        setTimeout(function() {
          card.remove();
        }, 200);
      } else {
        window.location.href = '/';
      }
    }
  };
  xhr.send('name=' + encodeURIComponent(name));
}

document.addEventListener('DOMContentLoaded', function() {
  initializeSizeSelector();
  restoreScrollPosition();
  setupImageLinks();
});

