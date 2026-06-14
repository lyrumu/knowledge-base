/* ============================================
   lyrumu's site — App JS
   Sidebar toggle, search (Fuse.js), Prism init
   ============================================ */

(function () {
  'use strict';

  // ========== Sidebar Toggle ==========
  function initSidebar() {
    var toggle = document.querySelector('.menu-toggle');
    var sidebar = document.querySelector('.sidebar');
    var overlay = document.querySelector('.sidebar-overlay');

    if (toggle && sidebar) {
      toggle.addEventListener('click', function () {
        sidebar.classList.toggle('open');
        if (overlay) overlay.classList.toggle('open');
      });
    }
    if (overlay) {
      overlay.addEventListener('click', function () {
        sidebar.classList.remove('open');
        overlay.classList.remove('open');
      });
    }
  }

  // ========== Directory Expand/Collapse ==========
  function initTree() {
    var tree = document.querySelector('.tree-container');
    if (!tree) return;

    tree.addEventListener('click', function (e) {
      var row = e.target.closest('.toggle-row');
      if (!row) return;
      e.preventDefault();
      e.stopPropagation();
      var li = row.closest('.tree-item');
      if (li && li.classList.contains('dir')) {
        li.classList.toggle('open');
      }
    });

    // Mark current page as active and open ancestors
    var currentPath = window.location.pathname;
    // Strip the site repo prefix to get the relative path
    var prefix = '/' + (typeof SITE_REPO !== 'undefined' ? SITE_REPO : 'knowledge-base') + '/';
    var relPath = currentPath.startsWith(prefix) ? currentPath.slice(prefix.length) : currentPath.slice(1);

    var links = tree.querySelectorAll('a[href]');
    for (var i = 0; i < links.length; i++) {
      var href = links[i].getAttribute('href');
      // Compare: strip prefix from href too
      var hrefRel = href.startsWith(prefix) ? href.slice(prefix.length) : href;
      if (hrefRel === relPath || hrefRel === relPath.replace(/^\//, '')) {
        var li = links[i].closest('.tree-item');
        if (li) {
          li.classList.add('active');
          // Open all ancestor tree-items
          var parent = li.parentElement;
          while (parent && parent !== tree) {
            if (parent.classList && parent.classList.contains('tree-item') && parent.classList.contains('dir')) {
              parent.classList.add('open');
            }
            parent = parent.parentElement;
          }
        }
        break;
      }
    }
  }

  // ========== Search (Fuse.js) ==========
  function initSearch() {
    var searchBox = document.querySelector('.search-box');
    if (!searchBox) return;
    if (typeof Fuse === 'undefined') return;

    var treeContainer = document.querySelector('.tree-container');
    var allItems = treeContainer ? treeContainer.querySelectorAll('.tree-item') : [];

    // Save original visibility
    var origDisplay = [];
    for (var i = 0; i < allItems.length; i++) {
      origDisplay.push(allItems[i].style.display);
    }

    // Build search index
    var searchData = [];
    for (var i = 0; i < allItems.length; i++) {
      var item = allItems[i];
      var link = item.querySelector(':scope > a, :scope > .toggle-row > a');
      if (!link) continue;
      // Get the text label (strip emoji prefix)
      var name = link.textContent.replace(/^[^\w\u4e00-\u9fff]+/, '').trim();
      searchData.push({ el: item, name: name.toLowerCase(), idx: i });
    }

    var fuse = new Fuse(searchData, {
      keys: ['name'],
      threshold: 0.4,
      ignoreLocation: true
    });

    searchBox.addEventListener('input', function () {
      var query = this.value.trim();

      if (!query) {
        // Reset
        for (var i = 0; i < allItems.length; i++) {
          allItems[i].style.display = origDisplay[i] || '';
        }
        // Close all dirs that weren't originally open
        for (var i = 0; i < allItems.length; i++) {
          if (allItems[i].classList.contains('dir') && origDisplay[i] === undefined) {
            // Don't touch dirs that were already open from initTree
          }
        }
        return;
      }

      var results = fuse.search(query);
      var showSet = new Set();

      // For each match, show it and all ancestors
      for (var j = 0; j < results.length; j++) {
        var el = results[j].item.el;
        showSet.add(el);

        // Show all ancestors
        var parent = el.parentElement;
        while (parent && parent !== treeContainer) {
          if (parent.classList && parent.classList.contains('tree-item')) {
            showSet.add(parent);
            parent.classList.add('open');
          }
          parent = parent.parentElement;
        }
      }

      // For matched dirs, also show their direct children
      for (var j = 0; j < results.length; j++) {
        var el = results[j].item.el;
        if (el.classList.contains('dir')) {
          var children = el.querySelectorAll(':scope > .tree-children > .tree-item');
          for (var c = 0; c < children.length; c++) {
            showSet.add(children[c]);
          }
        }
      }

      for (var k = 0; k < allItems.length; k++) {
        allItems[k].style.display = showSet.has(allItems[k]) ? '' : 'none';
      }
    });

    // Ctrl+K to focus search
    document.addEventListener('keydown', function (e) {
      if ((e.ctrlKey && e.key === 'k') || (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA')) {
        e.preventDefault();
        searchBox.focus();
        searchBox.select();
      }
    });
  }

  // ========== Image Zoom ==========
  function initImageZoom() {
    document.addEventListener('click', function (e) {
      if (e.target.tagName === 'IMG' && e.target.closest('.image-container')) {
        e.target.classList.toggle('zoomed');
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        var z = document.querySelector('img.zoomed');
        if (z) z.classList.remove('zoomed');
      }
    });
  }

  // ========== Init ==========
  document.addEventListener('DOMContentLoaded', function () {
    initSidebar();
    initTree();
    initSearch();
    initImageZoom();
  });
})();
