/* blur-image.js — 通用 LQIP blur-up 加载
   ---------------------------------------------------------------
   - 给 html 加 js-blurup class
   - 监听 .blur-img[data-lqip] 和 .cover-card__bg-img[data-lqip] 的 load/error
   - 加载完成：给 img 和 .blur-img-wrapper 加 .is-loaded
   - 加载失败：给 img 加 .is-broken
   - 暴露 window.BlurImage.markLoaded(img) 供动态切换封面时调用
   --------------------------------------------------------------- */
(function () {
  document.documentElement.classList.add("js-blurup");

  function markLoaded(img) {
    var cur = img.currentSrc || img.src || "";
    if (cur.indexOf("data:image") === 0) {
      // 当前仍是 LQIP：高清图由 srcset 异步加载，不手动改 src
      if (!img.getAttribute("srcset")) {
        var full = img.getAttribute("data-full-src");
        if (full && img.src !== full) img.src = full;
      }
      return;
    }
    img.classList.add("is-loaded");
    var wrapper = img.closest(".blur-img-wrapper");
    if (wrapper) wrapper.classList.add("is-loaded");
    // 兼容 DOCS 卡片的旧容器名
    var bg = img.closest(".cover-card__bg");
    if (bg) bg.classList.add("is-loaded");
  }

  function markBroken(img) {
    img.classList.add("is-broken");
    var wrapper = img.closest(".blur-img-wrapper");
    if (wrapper) wrapper.classList.add("is-broken");
  }

  function init() {
    // 封面延后图片由轮播脚本负责解码和揭示，失败时继续保留 LQIP。
    document.querySelectorAll(".blur-img:not([data-cover-src]), .cover-card__bg-img").forEach(function (img) {
      img.addEventListener("error", function () {
        markBroken(img);
        // DOCS 卡片兼容：显示图标降级
        var card = img.closest(".article-link--cover-card");
        if (card) {
          var fb = card.querySelector(".cover-card__icon-fallback");
          if (fb) fb.removeAttribute("hidden");
        }
      });

      img.addEventListener("load", function () {
        // 只有带 LQIP 的图才走 blur-up 收尾
        if (!img.dataset.lqip) return;
        markLoaded(img);
      });

      if (img.complete && img.dataset.lqip) markLoaded(img);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  window.BlurImage = { markLoaded: markLoaded };
})();
