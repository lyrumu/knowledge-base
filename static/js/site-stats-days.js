/* =============================================================================
   site-stats-days.js
   ---------------------------------------------------------------------------
   站点在线天数前端实时计算
   - 读取 [data-site-days] 上的 data-launch-date
   - 按自然日计算：今天 - 上线日 + 1
   - 使用 UTC 日粒度，尽量避免跨时区出现 +1 / -1 偏差
   ============================================================================= */
(function () {
  'use strict';

  function toUtcDay(date) {
    return Date.UTC(date.getFullYear(), date.getMonth(), date.getDate());
  }

  document.addEventListener('DOMContentLoaded', function () {
    var nodes = document.querySelectorAll('[data-site-days]');

    Array.prototype.forEach.call(nodes, function (node) {
      var raw = node.getAttribute('data-launch-date');
      if (!raw) return;

      var start = new Date(raw + 'T00:00:00');
      if (Number.isNaN(start.getTime())) return;

      var today = new Date();
      var diffMs = toUtcDay(today) - toUtcDay(start);
      var days = Math.floor(diffMs / 86400000) + 1;

      if (days > 0) {
        node.textContent = String(days);
      }
    });
  });
})();
