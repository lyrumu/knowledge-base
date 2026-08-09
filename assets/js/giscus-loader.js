/*
  giscus-loader.js — 评论区按需加载
  --------------------------------------------------------------------------
  原 inline 脚本从 layouts/partials/extend-footer.html 外置到这里（2026-07-25），
  行为完全一致：路径白名单 + notes 文章页自动识别 + 深浅主题切换。
  改为外部指纹文件后，每页 HTML 变薄，且可跨页缓存。
*/
(function () {
  const path = window.location.pathname.replace(/\/+$/, "") || "/";
  const pathParts = path.split("/").filter(Boolean);

  // 首页是聚焦式入口，不在轮播结束后追加第二个评论目的地。
  const allowedPaths = ["/about", "/works/projects", "/life/music"];
  const articleSections = ["notes"];

  const isAllowedPath = allowedPaths.includes(path);
  const isArticlePage =
    pathParts.length >= 2 &&
    articleSections.includes(pathParts[0]) &&
    !!document.querySelector("article");

  if (!isArticlePage && !isAllowedPath) return;

  function getGiscusTheme() {
    return document.documentElement.classList.contains("dark") ? "dark" : "light";
  }

  function updateGiscusTheme() {
    const giscus = document.querySelector("iframe.giscus-frame");
    if (giscus) {
      giscus.contentWindow.postMessage(
        { giscus: { setConfig: { theme: getGiscusTheme() } } },
        "https://giscus.app"
      );
    }
  }

  const observer = new MutationObserver(function (mutations) {
    mutations.forEach(function (mutation) {
      if (mutation.attributeName === "class") {
        updateGiscusTheme();
      }
    });
  });
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });

  const script = document.createElement("script");
  script.src = "https://giscus.app/client.js";
  script.setAttribute("data-repo", "lyrumu/knowledge-base");
  script.setAttribute("data-repo-id", "R_kgDOSCENwg");
  script.setAttribute("data-category", "Announcements");
  script.setAttribute("data-category-id", "DIC_kwDOSCENws4DAnhH");
  script.setAttribute("data-mapping", "pathname");
  script.setAttribute("data-strict", "0");
  script.setAttribute("data-reactions-enabled", "1");
  script.setAttribute("data-emit-metadata", "0");
  script.setAttribute("data-input-position", "top");
  script.setAttribute("data-theme", getGiscusTheme());
  script.setAttribute("data-lang", "zh-CN");
  script.setAttribute("data-loading", "lazy");
  script.crossOrigin = "anonymous";
  script.async = true;
  document.body.appendChild(script);
})();
