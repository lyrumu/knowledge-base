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
    var treeContainer = document.querySelector('.tree-container');
    if (!treeContainer) return;

    // Toggle on click the toggle-row or icon
    treeContainer.addEventListener('click', function (e) {
      var toggleRow = e.target.closest('.toggle-row');
      var toggleIcon = e.target.closest('.toggle-icon');

      if (toggleRow || toggleIcon) {
        e.preventDefault();
        e.stopPropagation();
        var li = (toggleRow || toggleIcon).closest('.tree-item');
        if (li && li.classList.contains('dir')) {
          li.classList.toggle('open');
        }
        return;
      }
    });

    // Mark current page as active
    var currentPath = window.location.pathname;
    var links = treeContainer.querySelectorAll('a');
    for (var i = 0; i < links.length; i++) {
      if (links[i].getAttribute('href') === currentPath) {
        var li = links[i].closest('.tree-item');
        if (li) li.classList.add('active');
        // Open all parent directories
        var parent = li ? li.parentElement : null;
        while (parent) {
          if (parent.classList && parent.classList.contains('tree-item')) {
            parent.classList.add('open');
          }
          parent = parent.parentElement;
        }
      }
    }
  }

  // ========== Search (Fuse.js) ==========
  function initSearch() {
    var searchBox = document.querySelector('.search-box');
    if (!searchBox) return;

    var treeContainer = document.querySelector('.tree-container');
    var allItems = treeContainer ? treeContainer.querySelectorAll('.tree-item') : [];

    // Build search index from tree items
    var searchData = [];
    for (var i = 0; i < allItems.length; i++) {
      var item = allItems[i];
      var link = item.querySelector('a');
      if (!link) continue;
      searchData.push({
        el: item,
        name: link.textContent.trim().toLowerCase(),
        isDir: item.classList.contains('dir')
      });
    }

    var fuse = new Fuse(searchData, {
      keys: ['name'],
      threshold: 0.4,
      ignoreLocation: true
    });

    searchBox.addEventListener('input', function () {
      var query = this.value.trim();

      if (!query) {
        // Reset: show all, collapse
        for (var i = 0; i < allItems.length; i++) {
          allItems[i].style.display = '';
        }
        return;
      }

      var results = fuse.search(query);
      var matches = new Set();

      // Add matching items and all their ancestors
      for (var j = 0; j < results.length; j++) {
        var el = results[j].item.el;
        matches.add(el);

        // Also show all descendants
        var descendants = el.querySelectorAll('.tree-item');
        for (var d = 0; d < descendants.length; d++) {
          matches.add(descendants[d]);
        }

        // Open parent directories
        var parent = el.parentElement;
        while (parent) {
          if (parent.classList && parent.classList.contains('tree-item')) {
            parent.classList.add('open');
            matches.add(parent);
          }
          parent = parent.parentElement;
        }
      }

      // Hide/show
      for (var k = 0; k < allItems.length; k++) {
        allItems[k].style.display = matches.has(allItems[k]) ? '' : 'none';
      }
    });

    // Keyboard shortcut: Ctrl+K or / to focus search
    document.addEventListener('keydown', function (e) {
      if ((e.ctrlKey && e.key === 'k') || (e.key === '/' && document.activeElement.tagName !== 'INPUT')) {
        e.preventDefault();
        searchBox.focus();
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

    // Close zoomed image on Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        var zoomed = document.querySelector('img.zoomed');
        if (zoomed) zoomed.classList.remove('zoomed');
      }
    });
  }

  // ========== Init ==========
  document.addEventListener('DOMContentLoaded', function () {
    initSidebar();
    initTree();
    initSearch();
    initImageZoom();

    // Re-run Prism if loaded
    if (typeof Prism !== 'undefined') {
      Prism.highlightAll();
    }
  });
})();
