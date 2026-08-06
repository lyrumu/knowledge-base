/* =============================================================================
   custom-cursor.js — 光晕圆环 + 延迟跟随光标
   ----------------------------------------------------------------------------
   仅在满足以下条件时启用：
     - 非触摸主输入设备 (pointer: fine)
     - 未开启 prefers-reduced-motion
     - 视口宽度 > 720px
   满足条件时给 <html> 加 custom-cursor-active 类，并在 body 末尾注入光标 DOM。
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
  root.classList.add('custom-cursor-active');

  const container = document.createElement('div');
  container.className = 'custom-cursor';
  container.setAttribute('aria-hidden', 'true');
  container.innerHTML =
    '<div class="cursor-ring-wrapper"><div class="cursor-ring"></div></div>';
  document.body.appendChild(container);

  let mouseX = -100;
  let mouseY = -100;
  let ringX = -100;
  let ringY = -100;
  let isRunning = false;
  let rafId = null;
  let hoverCount = 0;

  const lerp = (a, b, n) => (1 - n) * a + n * b;

  const updateVars = () => {
    container.style.setProperty('--ring-x', ringX.toFixed(2));
    container.style.setProperty('--ring-y', ringY.toFixed(2));
  };

  const tick = () => {
    if (!isRunning) {
      rafId = null;
      return;
    }
    ringX = lerp(ringX, mouseX, 0.43);
    ringY = lerp(ringY, mouseY, 0.43);
    updateVars();
    rafId = requestAnimationFrame(tick);
  };

  const start = () => {
    if (!isRunning) {
      isRunning = true;
      container.classList.remove('is-hidden');
      tick();
    }
  };

  const stop = () => {
    isRunning = false;
    if (rafId) {
      cancelAnimationFrame(rafId);
      rafId = null;
    }
    container.classList.add('is-hidden');
  };

  document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    if (!isRunning) {
      start();
    }
  }, { passive: true });

  document.addEventListener('mouseleave', stop);
  document.addEventListener('mouseenter', start);

  // 点击时的短暂收紧
  document.addEventListener('mousedown', () => root.classList.add('custom-cursor-click'));
  document.addEventListener('mouseup', () => root.classList.remove('custom-cursor-click'));

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

  document.addEventListener('mouseover', (e) => {
    if (e.target.closest(hoverSelectors)) {
      hoverCount += 1;
      root.classList.add('custom-cursor-hover');
    }
  });

  document.addEventListener('mouseout', (e) => {
    if (e.target.closest(hoverSelectors)) {
      hoverCount = Math.max(0, hoverCount - 1);
      if (hoverCount === 0) {
        root.classList.remove('custom-cursor-hover');
      }
    }
  });

  // 页面可见性变化时暂停/恢复，避免切回页面时跳变
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      stop();
    } else {
      start();
    }
  });

  // 初始化一次位置，避免首次进入时光标从左上角闪过
  updateVars();
  start();
})();