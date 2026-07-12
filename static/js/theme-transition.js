/*
 * theme-transition.js
 * --------------------------------------------------------------------------
 * DeepWiki / Vercel 风格主题切换动画（View Transition API + mask-image 斜向擦除）
 *
 * 工作流程：
 *   1. capture 阶段拦截 #appearance-switcher / #appearance-switcher-mobile 的 click，
 *      stopImmediatePropagation 阻止 appearance.js 的 bubble 监听器触发，避免双 toggle。
 *   2. 切换前在 <html> 上挂方向 class（vt-down / vt-up），CSS 据此选用不同方向的
 *      @keyframes；动画结束后清掉，避免污染下次切换。
 *      - 深色 → 浅色：.vt-down（左上 → 右下，135deg）
 *      - 浅色 → 深色：.vt-up  （右下 → 左上，315deg）
 *   3. document.startViewTransition 包裹真正的 toggle；不支持时降级为直接 toggle。
 *   4. transitioning 锁防止动画期间重复点击造成叠加。
 *
 * 加载顺序：必须在 appearance.js 之后加载（defer + head 末尾即可保证执行顺序）。
 * --------------------------------------------------------------------------
 */

(function () {
  "use strict";

  // 防止动画期间连续点击导致旧 transition 叠加（race condition）
  let transitioning = false;

  /**
   * 执行一次完整的主题切换（与 blowfish appearance.js 的 click 逻辑等价）。
   * 切换前在 <html> 上挂方向 class，动画结束后由 wrappedToggle 的 transition.finished
   * 钩子统一清理（避免散落 setTimeout 与 Promise 兜底逻辑分裂）。
   */
  function toggleTheme() {
    var html = document.documentElement;

    // 浅色 → 深色：vt-up（右下 → 左上）；深色 → 浅色：vt-down（左上 → 右下）
    var goingDark = !html.classList.contains("dark");
    html.classList.add(goingDark ? "vt-up" : "vt-down");

    html.classList.toggle("dark");

    var targetAppearance = window.getTargetAppearance
      ? window.getTargetAppearance()
      : (html.classList.contains("dark") ? "dark" : "light");

    try {
      localStorage.setItem("appearance", targetAppearance);
    } catch (e) {
      // private mode 等场景 localStorage 不可用，静默忽略
    }

    // 复用 appearance.js 的副作用更新，保证主题切换行为完全一致
    if (typeof window.updateMeta === "function") window.updateMeta();
    if (typeof window.updateMermaidTheme === "function") window.updateMermaidTheme();
    if (typeof window.updateLogo === "function") window.updateLogo(targetAppearance);
  }

  /**
   * View Transition 包裹 toggleTheme：触发斜向擦除动画，动画结束（含被中断）
   * 后清掉方向 class 并释放 transitioning 锁。
   */
  function wrappedToggle() {
    if (transitioning) return;
    transitioning = true;

    // 不支持 View Transition API → 直接 toggle，无动画
    if (typeof document.startViewTransition !== "function") {
      toggleTheme();
      document.documentElement.classList.remove("vt-up", "vt-down");
      transitioning = false;
      return;
    }

    var transition = document.startViewTransition(toggleTheme);

    // finished 在动画正常完成 / 异常 / 被新 transition 替换时都会 resolve/catch
    transition.finished
      .catch(function () {})
      .finally(function () {
        document.documentElement.classList.remove("vt-up", "vt-down");
        transitioning = false;
      });
  }

  /**
   * capture 阶段拦截指定 id 按钮的 click：
   *   - 比 appearance.js 的 bubble 监听器更早触发
   *   - stopImmediatePropagation 阻止 appearance.js 收到事件，避免双 toggle
   */
  function captureSwitcher(id) {
    var btn = document.getElementById(id);
    if (!btn) return;

    btn.addEventListener(
      "click",
      function (e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        wrappedToggle();
      },
      true // useCapture
    );
  }

  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  ready(function () {
    captureSwitcher("appearance-switcher");
    captureSwitcher("appearance-switcher-mobile");
  });
})();