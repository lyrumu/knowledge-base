/* =============================================================================
   custom-cursor.js — 光晕圆环 + 延迟跟随光标
   ----------------------------------------------------------------------------
   仅在满足以下条件时启用：
     - 非触摸主输入设备 (pointer: fine)
     - 未开启 prefers-reduced-motion
     - 视口宽度 > 720px
   满足条件时复用 body 末尾的光标 DOM，并在真实指针事件后接管系统光标。
   ============================================================================= */

(function () {
  'use strict';

  const mq = window.matchMedia;
  const isCoarse = mq('(pointer: coarse)').matches;
  const isReduced = mq('(prefers-reduced-motion: reduce)').matches;
  const isSmall = mq('(max-width: 720px)').matches;

  if (isCoarse || isReduced || isSmall) {
    return;
  }

  const root = document.documentElement;
  let container = document.querySelector('.custom-cursor');

  // 模板通常已经输出容器；保留兜底，避免 partial 被移除后脚本直接失效。
  if (!container) {
    container = document.createElement('div');
    container.className = 'custom-cursor';
    container.setAttribute('aria-hidden', 'true');
    container.innerHTML =
      '<div class="cursor-ring-wrapper"><div class="cursor-ring"></div></div>';
    document.body.appendChild(container);
  }

  const ringWrapper = container.querySelector('.cursor-ring-wrapper');
  if (!ringWrapper) return;

  const followTime = 18;

  let mouseX = 0;
  let mouseY = 0;
  let ringX = 0;
  let ringY = 0;
  let hasPosition = false;
  let isPageVisible = !document.hidden;
  let rafId = null;
  let lastFrameTime = 0;

  const render = () => {
    ringWrapper.style.transform =
      `translate3d(${ringX.toFixed(2)}px, ${ringY.toFixed(2)}px, 0)`;
  };

  const cancelLoop = () => {
    if (rafId) {
      cancelAnimationFrame(rafId);
      rafId = null;
    }
    lastFrameTime = 0;
  };

  const hide = () => {
    cancelLoop();
    container.classList.add('is-hidden');
    root.classList.remove('custom-cursor-active', 'custom-cursor-click', 'custom-cursor-hover');
  };

  const activate = () => {
    if (!hasPosition || !isPageVisible) return;
    root.classList.add('custom-cursor-active');
    container.classList.add('is-ready');
    container.classList.remove('is-hidden');
  };

  const tick = (time) => {
    rafId = null;
    if (!hasPosition || !isPageVisible) return;

    const elapsed = lastFrameTime ? Math.min(time - lastFrameTime, 50) : 16.67;
    const follow = 1 - Math.exp(-elapsed / followTime);
    lastFrameTime = time;
    ringX += (mouseX - ringX) * follow;
    ringY += (mouseY - ringY) * follow;

    const distanceX = mouseX - ringX;
    const distanceY = mouseY - ringY;
    const settled = distanceX * distanceX + distanceY * distanceY < 0.01;
    if (settled) {
      ringX = mouseX;
      ringY = mouseY;
    }
    render();

    if (settled) {
      lastFrameTime = 0;
    } else {
      rafId = requestAnimationFrame(tick);
    }
  };

  const scheduleTick = () => {
    if (!rafId) rafId = requestAnimationFrame(tick);
  };

  const setPosition = (x, y, snap) => {
    if (!Number.isFinite(x) || !Number.isFinite(y)) return;
    const scroller = document.scrollingElement || root;
    const isScrollbarEdge =
      (scroller.scrollHeight > scroller.clientHeight && x >= scroller.clientWidth - 16) ||
      (scroller.scrollWidth > scroller.clientWidth && y >= scroller.clientHeight - 16);
    if (isScrollbarEdge) {
      hide();
      return;
    }
    mouseX = x;
    mouseY = y;

    if (snap || !hasPosition) {
      ringX = x;
      ringY = y;
      hasPosition = true;
      render();
    }

    activate();
    scheduleTick();
  };

  // hover 检测：给常见交互元素及项目卡片加 class
  const hoverSelectors = [
    'a',
    'button',
    'input',
    'textarea',
    'select',
    '[role="button"]',
    'label',
    'summary',
    '.project-card',
    '.module-card',
    '.article-link',
    '.life-sub-card',
    '.resource-card',
    '.music-item',
    '.about-contact-btn',
    '.site-brand-badge'
  ].join(', ');

  const syncHoverState = (target) => {
    const interactive = target instanceof Element && target.closest(hoverSelectors);
    root.classList.toggle('custom-cursor-hover', Boolean(interactive));
  };

  document.addEventListener('pointermove', (event) => {
    if (event.pointerType && event.pointerType !== 'mouse') return;
    const samples = typeof event.getCoalescedEvents === 'function'
      ? event.getCoalescedEvents()
      : [];
    const latest = samples.length ? samples[samples.length - 1] : event;
    const snap = !hasPosition || container.classList.contains('is-hidden');
    setPosition(latest.clientX, latest.clientY, snap);
  }, { passive: true });

  document.addEventListener('pointerover', (event) => syncHoverState(event.target));
  document.addEventListener('pointerout', (event) => {
    syncHoverState(event.relatedTarget);
    if (!event.relatedTarget) hide();
  });

  document.addEventListener('pointerdown', (event) => {
    if (event.pointerType && event.pointerType !== 'mouse') return;
    setPosition(event.clientX, event.clientY, false);
    root.classList.add('custom-cursor-click');
  }, { passive: true });

  document.addEventListener('pointerup', () => root.classList.remove('custom-cursor-click'));
  document.addEventListener('pointercancel', () => root.classList.remove('custom-cursor-click'));
  document.addEventListener('mouseleave', () => {
    hide();
  });
  document.addEventListener('mouseenter', (event) => {
    setPosition(event.clientX, event.clientY, true);
    syncHoverState(document.elementFromPoint(event.clientX, event.clientY));
  });

  // 页面可见性变化时暂停/恢复，避免切回页面时跳变
  document.addEventListener('visibilitychange', () => {
    isPageVisible = !document.hidden;
    if (document.hidden) {
      hide();
    }
  });

  window.addEventListener('pagehide', hide);
  window.addEventListener('pageshow', () => {
    isPageVisible = true;
  });
  window.addEventListener('blur', hide);
})();
