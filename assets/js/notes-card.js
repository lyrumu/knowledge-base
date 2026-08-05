/* notes-card.js — DOCS 卡片图片 blur-up 模糊占位
   ---------------------------------------------------------------
   - html 加 js-blurup：CSS 只在 .js-blurup 下启用模糊态，
     无 JS 时图片照常显示（不会永久模糊）。
   - img[data-lqip]：src 是 24px LQIP data URI，srcset 是 600/1200px WebP。
   - 主图加载完成 → .is-loaded → CSS 平滑褪模糊；失败 → 显示渐变底 + 图标降级。
   --------------------------------------------------------------- */
(function () {
  document.documentElement.classList.add("js-blurup");

  function markLoaded(img) {
    var cur = img.currentSrc || img.src || "";
    if (cur.indexOf("data:image") === 0) {
      // 无 srcset 支持的浏览器：currentSrc 仍是 LQIP，直接换成主图
      var full = img.getAttribute("data-full-src");
      if (full && img.src !== full) img.src = full;
      return;
    }
    img.classList.add("is-loaded");
  }

  function init() {
    // 失败降级：任何 cover-card 主图加载失败 → 渐变底 + 图标
    document.querySelectorAll(".cover-card__bg-img").forEach(function (img) {
      img.addEventListener("error", function () {
        var card = img.closest(".article-link--cover-card");
        if (!card) return;
        var fb = card.querySelector(".cover-card__icon-fallback");
        if (fb) fb.removeAttribute("hidden");
        img.classList.add("is-broken");
      });
    });

    // blur-up：只有带 LQIP 的图走模糊过渡
    document.querySelectorAll(".cover-card__bg-img[data-lqip]").forEach(function (img) {
      img.addEventListener("load", function () { markLoaded(img); });
      // 缓存命中 / 首屏已加载完成时直接收尾
      if (img.complete) markLoaded(img);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
