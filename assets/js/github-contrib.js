/* github-contrib.js — About 页 GitHub 年度贡献图（可切换年份 + 当年贡献数）
   ---------------------------------------------------------------
   - 数据源：github-contributions-api.jogruber.de（CORS 全开，可前端直连）
     GET /v4/{user}?y=all
     → { total: { "2025": 3, "2026": 255 },
         contributions: [{ date: "YYYY-MM-DD", count: n, level: 0-4 }, ...] }
   - 注意：返回数组按年份分块、非全局时间序（2026 全年在前），必须按 date 排序
   - 渲染：年份 tab（新年在前，默认当年）+ 贡献数行（当年显示 "this year"）+
     GitHub 官方绿格子图（53 周 × 7 天，周日开头；当年含未来日期的 0 值格，与 GitHub 一致）
   - 降级：fetch 失败 / JSON 异常时不做任何渲染，保留 shortcode 里的
     ghchart.rshah.org 兜底图（最近一年）
   --------------------------------------------------------------- */
(function () {
  "use strict";

  var root = document.querySelector(".gh-contrib");
  if (!root) return;

  var user = root.getAttribute("data-user") || "lyrumu";
  var API = "https://github-contributions-api.jogruber.de/v4/" + user + "?y=all";
  var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  var WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  fetch(API)
    .then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status);
      return res.json();
    })
    .then(render)
    .catch(function (err) {
      // 静默降级：保留 shortcode 里的 ghchart 兜底图
      if (window.console) {
        console.warn("[github-contrib] API failed, keep ghchart fallback:", err);
      }
    });

  function render(data) {
    var totals = data.total || {};
    var days = (data.contributions || []).slice().sort(function (a, b) {
      return a.date < b.date ? -1 : a.date > b.date ? 1 : 0;
    });
    var years = Object.keys(totals)
      .map(Number)
      .sort(function (a, b) { return b - a; }); // 新年份在前
    if (!years.length || !days.length) return;

    var currentYear = new Date().getFullYear();
    var selected = years.indexOf(currentYear) !== -1 ? currentYear : years[0];

    // 渲染成功才清掉兜底图
    root.textContent = "";
    root.classList.add("is-ready");

    var tabs = buildTabs(years, selected);
    var count = buildCount(selected, totals, currentYear);
    var chart = buildChart(days, selected);
    var legend = buildLegend();

    root.appendChild(tabs);
    root.appendChild(count);
    root.appendChild(chart);
    root.appendChild(legend);

    // 年份切换：替换计数行 + 格子图（filter 重建，量级 ≤400 格，无需虚拟化）
    tabs.addEventListener("click", function (e) {
      var btn = e.target.closest(".gh-contrib-tab");
      if (!btn || btn.classList.contains("is-active")) return;
      var year = Number(btn.getAttribute("data-year"));
      var active = tabs.querySelector(".gh-contrib-tab.is-active");
      if (active) {
        active.classList.remove("is-active");
        active.setAttribute("aria-pressed", "false");
      }
      btn.classList.add("is-active");
      btn.setAttribute("aria-pressed", "true");

      var nextCount = buildCount(year, totals, currentYear);
      root.replaceChild(nextCount, count);
      count = nextCount;

      var nextChart = buildChart(days, year);
      root.replaceChild(nextChart, chart);
      chart = nextChart;
    });
  }

  /* 年份 tab（新年份在前） */
  function buildTabs(years, selected) {
    var wrap = document.createElement("div");
    wrap.className = "gh-contrib-tabs";
    years.forEach(function (y) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "gh-contrib-tab" + (y === selected ? " is-active" : "");
      b.setAttribute("data-year", y);
      b.setAttribute("aria-pressed", y === selected ? "true" : "false");
      b.textContent = y;
      wrap.appendChild(b);
    });
    return wrap;
  }

  /* 贡献数行：当年 → "this year"，往年 → "in YYYY" */
  function buildCount(year, totals, currentYear) {
    var p = document.createElement("p");
    p.className = "gh-contrib-count";
    var n = totals[year];
    if (typeof n !== "number") n = 0;
    var label = year === currentYear ? "this year" : "in " + year;
    p.innerHTML =
      "<strong>" + Number(n).toLocaleString("en-US") + "</strong> contributions " + label;
    return p;
  }

  /* 格子图：53 周 × 7 天，CSS Grid 显式定位（列 1 = 周几标签，行 1 = 月份标签） */
  function buildChart(days, year) {
    var wrap = document.createElement("div");
    wrap.className = "gh-contrib-scroll";

    var yearDays = days.filter(function (d) {
      return Number(d.date.slice(0, 4)) === year;
    });
    if (!yearDays.length) {
      var empty = document.createElement("p");
      empty.className = "gh-contrib-count";
      empty.textContent = "No contribution data for " + year + ".";
      wrap.appendChild(empty);
      return wrap;
    }

    // 起点回退到第一天的本周周日（与 GitHub 日历对齐）
    var start = parseDate(yearDays[0].date);
    start.setDate(start.getDate() - start.getDay());

    var first = parseDate(yearDays[0].date);
    var last = parseDate(yearDays[yearDays.length - 1].date);
    var weeks = Math.floor((last - start) / 86400000 / 7) + 1;

    var grid = document.createElement("div");
    grid.className = "gh-contrib-chart";
    grid.setAttribute("aria-hidden", "true");
    grid.style.gridTemplateColumns = "auto repeat(" + weeks + ", var(--gh-cell))";

    // 月份标签：某列首格进入新月份时标注；最后一列放不下就跳过（只同步月份）
    var colFirst = {}; // col -> 该列第一天的 Date
    yearDays.forEach(function (d) {
      var dt = parseDate(d.date);
      var col = weekCol(dt, start);
      if (!(col in colFirst)) colFirst[col] = dt;
    });
    var lastMonth = -1;
    Object.keys(colFirst).map(Number).forEach(function (col) {
      var m = colFirst[col].getMonth();
      if (m !== lastMonth) {
        if (col < weeks - 1) {
          addLabel(grid, MONTHS[m], "gh-contrib-month", 1, col + 2);
        }
        lastMonth = m;
      }
    });

    // 周几标签：Mon / Wed / Fri（窄屏由 CSS 隐藏）
    [1, 3, 5].forEach(function (row) {
      addLabel(grid, WEEKDAYS[row], "gh-contrib-wday", row + 2, 1);
    });

    yearDays.forEach(function (d) {
      var dt = parseDate(d.date);
      var cell = document.createElement("span");
      cell.className = "gh-day";
      cell.setAttribute("data-level", d.level);
      cell.title =
        (d.count === 0
          ? "No contributions"
          : d.count + (d.count === 1 ? " contribution" : " contributions")) +
        " on " + MONTHS[dt.getMonth()] + " " + dt.getDate() + ", " + dt.getFullYear();
      cell.style.gridRow = dt.getDay() + 2;
      cell.style.gridColumn = weekCol(dt, start) + 2;
      grid.appendChild(cell);
    });

    wrap.appendChild(grid);
    return wrap;
  }

  /* Less / More 图例（复用 .gh-day 配色） */
  function buildLegend() {
    var wrap = document.createElement("div");
    wrap.className = "gh-contrib-legend";
    wrap.innerHTML =
      '<span class="gh-contrib-legend-label">Less</span>' +
      '<span class="gh-day" data-level="0"></span>' +
      '<span class="gh-day" data-level="1"></span>' +
      '<span class="gh-day" data-level="2"></span>' +
      '<span class="gh-day" data-level="3"></span>' +
      '<span class="gh-day" data-level="4"></span>' +
      '<span class="gh-contrib-legend-label">More</span>';
    return wrap;
  }

  function addLabel(grid, text, cls, row, col) {
    var el = document.createElement("span");
    el.className = cls;
    el.textContent = text;
    el.style.gridRow = row;
    el.style.gridColumn = col;
    grid.appendChild(el);
  }

  function weekCol(dt, start) {
    return Math.floor((dt - start) / 86400000 / 7);
  }

  // 本地时区解析，避免 Date 构造器按 UTC 解析日期串造成的偏移
  function parseDate(s) {
    return new Date(s + "T00:00:00");
  }
})();
