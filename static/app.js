/* lyrumu's site — App JS */
(function () {
  'use strict';

  /* ===== Sidebar Toggle (mobile) ===== */
  var toggle = document.querySelector('.menu-toggle');
  var sidebar = document.querySelector('.sidebar');
  var overlay = document.querySelector('.sidebar-overlay');
  if (toggle) toggle.onclick = function () { sidebar.classList.toggle('open'); overlay.classList.toggle('open'); };
  if (overlay) overlay.onclick = function () { sidebar.classList.remove('open'); overlay.classList.remove('open'); };

  /* ===== Directory Expand/Collapse ===== */
  var tree = document.querySelector('.tree-container');
  if (tree) {
    tree.addEventListener('click', function (e) {
      var row = e.target.closest('.toggle-row');
      if (!row) return;
      var li = row.closest('.tree-item.dir');
      if (li) li.classList.toggle('open');
    });
  }

  /* ===== Mark current page active & open ancestors ===== */
  if (tree) {
    var path = location.pathname.replace(/\/+$/, '');
    var links = tree.querySelectorAll('a[href]');
    for (var i = 0; i < links.length; i++) {
      var href = links[i].getAttribute('href').replace(/\/+$/, '');
      if (href === path || href === path.replace('/knowledge-base', '')) {
        var li = links[i].closest('.tree-item');
        if (li) {
          li.classList.add('active');
          var p = li.parentElement;
          while (p && p !== tree) {
            if (p.classList && p.classList.contains('tree-item') && p.classList.contains('dir')) p.classList.add('open');
            p = p.parentElement;
          }
        }
        break;
      }
    }
  }

  /* ===== Search — save/restore original state ===== */
  var searchBox = document.querySelector('.search-box');
  if (searchBox && tree) {
    var items = tree.querySelectorAll('.tree-item');

    // Snapshot original state
    var origState = [];
    for (var i = 0; i < items.length; i++) {
      origState.push({
        display: items[i].style.display,
        open: items[i].classList.contains('open')
      });
    }

    searchBox.addEventListener('input', function () {
      var q = this.value.trim().toLowerCase();

      if (!q) {
        // Restore original state
        for (var i = 0; i < items.length; i++) {
          items[i].style.display = origState[i].display;
          if (origState[i].open) items[i].classList.add('open');
          else items[i].classList.remove('open');
        }
        return;
      }

      // Find matches
      var show = new Set();
      for (var i = 0; i < items.length; i++) {
        var text = items[i].textContent.toLowerCase();
        if (text.indexOf(q) !== -1) {
          show.add(items[i]);
          // Open ancestors
          var p = items[i].parentElement;
          while (p && p !== tree) {
            if (p.classList && p.classList.contains('tree-item')) {
              show.add(p);
              if (p.classList.contains('dir')) p.classList.add('open');
            }
            p = p.parentElement;
          }
          // If dir, show direct children
          if (items[i].classList.contains('dir')) {
            var ch = items[i].querySelectorAll(':scope > .tree-children > .tree-item');
            for (var c = 0; c < ch.length; c++) show.add(ch[c]);
          }
        }
      }

      for (var i = 0; i < items.length; i++) {
        items[i].style.display = show.has(items[i]) ? '' : 'none';
      }
    });

    // Ctrl+K
    document.addEventListener('keydown', function (e) {
      if ((e.ctrlKey && e.key === 'k') || (e.key === '/' && !/INPUT|TEXTAREA/.test(document.activeElement.tagName))) {
        e.preventDefault();
        searchBox.focus();
        searchBox.select();
      }
    });
  }

  /* ===== Image Zoom ===== */
  document.addEventListener('click', function (e) {
    if (e.target.tagName === 'IMG' && e.target.closest('.image-container')) e.target.classList.toggle('zoomed');
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { var z = document.querySelector('img.zoomed'); if (z) z.classList.remove('zoomed'); }
  });

  /* ===== Re-run Prism highlighting ===== */
  if (typeof Prism !== 'undefined') {
    Prism.highlightAll();
  }

})();
