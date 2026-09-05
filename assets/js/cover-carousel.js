/* Homepage cover — threshold-triggered music-orbit controller. */
(function () {
  "use strict";

  const root = document.querySelector("[data-cover-carousel]");
  if (!root) return;

  const scrollScene = root.closest(".cover-page");
  const stickyContent = root.closest(".cover-content");
  const deck = root.querySelector(".cover-carousel-deck");
  const intro = root.querySelector("[data-cover-intro]");
  const explorePrompt = root.querySelector("[data-cover-explore]");
  const musicCamera = scrollScene?.querySelector(".cover-music-camera");
  const musicField = scrollScene?.querySelector(".cover-music-field");
  const ambientSpinners = musicField
    ? Array.from(musicField.querySelectorAll(".cover-music-field__disc, .cover-music-field__orbit"))
    : [];
  const introLinks = intro ? Array.from(intro.querySelectorAll("a")) : [];
  const slides = Array.from(root.querySelectorAll("[data-cover-carousel-slide]"));
  const cardImages = Array.from(root.querySelectorAll("[data-cover-src]"));
  const decodedImages = [];
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const compactLayout = window.matchMedia("(max-width: 720px)");

  if (!scrollScene || !stickyContent || !deck || !musicCamera || !musicField || slides.length !== 3) return;

  const state = {
    activeIndex: 0,
    cardExitTimer: 0,
    gestureDelta: 0,
    imagesStarted: false,
    imageRevealTimer: 0,
    open: false,
    railFrame: 0,
    railIndex: 0,
    resetFrame: 0,
    resizeFrame: 0,
    settleTimer: 0,
    touchStartY: null,
    visible: true,
  };

  const GESTURE_THRESHOLD = 72;
  const SETTLE_FALLBACK = 1400;
  const clamp = (value, min, max) => Math.min(Math.max(value, min), max);
  const compact = () => compactLayout.matches || reduceMotion.matches;

  function revealDecodedImages() {
    if (state.imageRevealTimer && !compact()) return;
    decodedImages.splice(0).forEach((img) => {
      img.closest(".blur-img-wrapper")?.classList.add("is-loaded");
    });
  }

  function deferImageReveal() {
    // 覆盖整个镜头/三卡过渡；反向操作或切换侧卡都会重新计时。
    window.clearTimeout(state.imageRevealTimer);
    state.imageRevealTimer = window.setTimeout(() => {
      state.imageRevealTimer = 0;
      revealDecodedImages();
    }, SETTLE_FALLBACK);
  }

  function warmCardImages() {
    if (state.imagesStarted) return;
    state.imagesStarted = true;
    scrollScene.classList.add("is-images-warming");
    cardImages.forEach((img) => {
      img.srcset = img.dataset.coverCandidates;
      img.src = img.dataset.coverSrc;
      img.decode().then(() => {
        decodedImages.push(img);
        revealDecodedImages();
      }).catch(() => {
        // 加载或解码失败保留 LQIP，不能阻塞其他图片或卡片交互。
      });
    });
  }

  function warmAfterCoverPaint() {
    const engraving = musicField.querySelector("img");
    Promise.allSettled([engraving?.decode(), document.fonts.ready]).then(() => {
      // 留出首屏绘制机会后立即预热，不等全站 load 或不确定的空闲回调。
      window.requestAnimationFrame(() => window.requestAnimationFrame(warmCardImages));
    });
  }

  function setInert(element, inert) {
    if (!element) return;
    if (inert) {
      element.setAttribute("inert", "");
    } else {
      element.removeAttribute("inert");
    }
  }

  function cardName(slide) {
    return slide.querySelector("h2")?.textContent.trim() || "section";
  }

  function setActiveIndex(index, force = false) {
    const next = (index + slides.length) % slides.length;
    if (!force && next === state.activeIndex) return;

    if (next !== state.activeIndex) deferImageReveal();
    state.activeIndex = next;
    root.dataset.activeIndex = String(next);

    slides.forEach((slide, slideIndex) => {
      const offset = (slideIndex - next + slides.length) % slides.length;
      const active = offset === 0;
      const surface = slide.querySelector(".cover-carousel-card-surface");

      slide.dataset.state = active ? "active" : offset === 1 ? "next" : "previous";
      if (active) {
        slide.setAttribute("aria-current", "true");
      } else {
        slide.removeAttribute("aria-current");
      }

      setInert(surface, false);
      if (surface) {
        surface.setAttribute("aria-label", `${active ? "Open" : "Select"} ${cardName(slide)}`);
      }
    });
  }

  function resetDesktopCards() {
    state.activeIndex = 0;
    root.dataset.activeIndex = "0";
    slides.forEach((slide) => {
      slide.dataset.state = "pending";
      slide.removeAttribute("aria-current");
      const surface = slide.querySelector(".cover-carousel-card-surface");
      setInert(surface, true);
      surface?.removeAttribute("aria-label");
    });
  }

  function markSettled() {
    window.clearTimeout(state.settleTimer);
    state.settleTimer = 0;
    if (!state.open || compact()) return;
    root.classList.add("is-orbit-settled");
    scrollScene.classList.add("is-orbit-settled");
    syncAmbientLoop();
  }

  function syncAmbientLoop() {
    scrollScene.classList.toggle(
      "is-orbit-looping",
      state.open && state.visible
    );
  }

  function finishCardExit() {
    window.clearTimeout(state.cardExitTimer);
    state.cardExitTimer = 0;
    if (state.open || compact()) return;
    root.classList.remove("is-orbit-open");
    resetDesktopCards();
    void deck.offsetWidth;
    root.classList.remove("is-orbit-closing");
  }

  function resetAmbientMotion() {
    if (state.resetFrame) {
      window.cancelAnimationFrame(state.resetFrame);
      state.resetFrame = 0;
    }

    if (!scrollScene.classList.contains("is-orbit-looping")) {
      scrollScene.classList.remove("is-orbit-looping");
      ambientSpinners.forEach((element) => element.style.removeProperty("transform"));
      return;
    }

    const transforms = ambientSpinners.map((element) => getComputedStyle(element).transform);
    scrollScene.classList.remove("is-orbit-looping");
    ambientSpinners.forEach((element, index) => {
      element.style.transform = transforms[index];
    });
    void musicField.offsetWidth;

    state.resetFrame = window.requestAnimationFrame(() => {
      ambientSpinners.forEach((element) => element.style.removeProperty("transform"));
      state.resetFrame = 0;
    });
  }

  function setOrbitOpen(open) {
    if (compact() || open === state.open) return;

    state.open = open;
    state.gestureDelta = 0;
    deferImageReveal();
    if (open) warmCardImages();
    window.clearTimeout(state.cardExitTimer);
    state.cardExitTimer = 0;
    window.clearTimeout(state.settleTimer);
    state.settleTimer = 0;
    root.classList.remove("is-orbit-settled");
    if (open) {
      if (state.resetFrame) {
        window.cancelAnimationFrame(state.resetFrame);
        state.resetFrame = 0;
      }
      ambientSpinners.forEach((element) => element.style.removeProperty("transform"));
      scrollScene.classList.remove("is-orbit-looping");
    } else {
      resetAmbientMotion();
    }
    scrollScene.classList.remove("is-orbit-settled");
    scrollScene.classList.toggle("is-orbit-open", open);

    introLinks.forEach((link) => setInert(link, open));
    setInert(explorePrompt, open);

    if (open) {
      root.classList.remove("is-orbit-closing");
      root.classList.add("is-orbit-open");
      setActiveIndex(0, true);
      syncAmbientLoop();
      state.settleTimer = window.setTimeout(markSettled, SETTLE_FALLBACK);
    } else {
      root.classList.add("is-orbit-closing");
      slides.forEach((slide) => setInert(slide.querySelector(".cover-carousel-card-surface"), true));
      state.cardExitTimer = window.setTimeout(finishCardExit, 240);
    }
  }

  function closestRailIndex() {
    const deckRect = deck.getBoundingClientRect();
    const centre = deckRect.left + deck.clientWidth / 2;
    let closest = 0;
    let distance = Number.POSITIVE_INFINITY;

    slides.forEach((slide, index) => {
      const rect = slide.getBoundingClientRect();
      const current = Math.abs(rect.left + rect.width / 2 - centre);
      if (current < distance) {
        closest = index;
        distance = current;
      }
    });

    return closest;
  }

  function setRailIndex(index) {
    state.railIndex = clamp(index, 0, slides.length - 1);
    slides.forEach((slide, slideIndex) => {
      const active = slideIndex === state.railIndex;
      const surface = slide.querySelector(".cover-carousel-card-surface");
      slide.dataset.state = active ? "active" : slideIndex < state.railIndex ? "previous" : "next";
      slide.removeAttribute("aria-current");
      setInert(surface, false);
      surface?.removeAttribute("aria-label");
    });
  }

  function updateFromRail() {
    state.railFrame = 0;
    if (!compact()) return;
    setRailIndex(closestRailIndex());
  }

  function scheduleRailUpdate() {
    if (state.railFrame) return;
    state.railFrame = window.requestAnimationFrame(updateFromRail);
  }

  function updateOrbitGeometry() {
    const width = window.innerWidth;
    const height = window.innerHeight;
    const rootFontSize = parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;
    const headerHeight =
      parseFloat(getComputedStyle(scrollScene).getPropertyValue("--cover-header-height")) || rootFontSize * 5.1;
    const baseDiameter = Math.min(width * 0.29, rootFontSize * 21);
    const radius = (2 * width * width) / (9 * height) + height / 8;
    const scale = (2 * radius) / baseDiameter;
    const baseCentreY = headerHeight + (height - headerHeight) * 0.53;
    const targetCentreY = height * 0.75 + radius;

    scrollScene.style.setProperty("--cover-orbit-scale", scale.toFixed(4));
    scrollScene.style.setProperty("--cover-orbit-y", `${(targetCentreY - baseCentreY).toFixed(2)}px`);
  }

  function refreshLayout() {
    state.resizeFrame = 0;
    document.body.classList.toggle("is-cover-gesture-mode", !compact());

    if (compact()) {
      state.open = false;
      warmCardImages();
      revealDecodedImages();
      window.clearTimeout(state.cardExitTimer);
      state.cardExitTimer = 0;
      window.clearTimeout(state.settleTimer);
      resetAmbientMotion();
      root.classList.remove("is-orbit-open", "is-orbit-closing", "is-orbit-settled");
      scrollScene.classList.remove("is-orbit-open", "is-orbit-settled");
      introLinks.forEach((link) => setInert(link, false));
      setInert(explorePrompt, false);
      setRailIndex(closestRailIndex());
      return;
    }

    updateOrbitGeometry();

    if (state.open) {
      setActiveIndex(state.activeIndex, true);
    } else {
      resetDesktopCards();
      introLinks.forEach((link) => setInert(link, false));
      setInert(explorePrompt, false);
    }
  }

  function scheduleRefresh() {
    if (state.resizeFrame) return;
    state.resizeFrame = window.requestAnimationFrame(refreshLayout);
  }

  function showOrbit(event) {
    event.preventDefault();

    if (compact()) {
      deck.scrollIntoView({ block: "start", behavior: "auto" });
      return;
    }

    setOrbitOpen(true);
  }

  function onWheel(event) {
    if (compact()) return;
    event.preventDefault();

    const direction = Math.sign(event.deltaY);
    if (!direction || (direction > 0) === state.open) {
      state.gestureDelta = 0;
      return;
    }

    if (Math.sign(state.gestureDelta) !== direction) state.gestureDelta = 0;
    state.gestureDelta += event.deltaY;
    if (Math.abs(state.gestureDelta) >= GESTURE_THRESHOLD) setOrbitOpen(direction > 0);
  }

  function onTouchStart(event) {
    if (!compact() && event.touches.length === 1) state.touchStartY = event.touches[0].clientY;
  }

  function onTouchEnd(event) {
    if (compact() || state.touchStartY === null || !event.changedTouches.length) return;
    const distance = state.touchStartY - event.changedTouches[0].clientY;
    state.touchStartY = null;
    if (Math.abs(distance) >= 48 && (distance > 0) !== state.open) setOrbitOpen(distance > 0);
  }

  function onCardClick(event) {
    if (compact() || !state.open) return;
    const index = slides.findIndex((slide) => slide.contains(event.currentTarget));
    if (index < 0 || index === state.activeIndex) return;
    event.preventDefault();
    setActiveIndex(index);
  }

  function onKeydown(event) {
    if (compact() || !state.open || event.defaultPrevented) return;
    if (event.metaKey || event.ctrlKey || event.altKey) return;
    if (!root.contains(document.activeElement)) return;

    if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
      event.preventDefault();
      setActiveIndex(state.activeIndex + (event.key === "ArrowRight" ? 1 : -1));
      slides[state.activeIndex].querySelector(".cover-carousel-card-surface")?.focus();
    }
  }

  function onMusicCameraTransitionEnd(event) {
    if (event.target === musicCamera && event.propertyName === "transform") markSettled();
  }

  window.addEventListener("wheel", onWheel, { passive: false });
  window.addEventListener("touchstart", onTouchStart, { passive: true });
  window.addEventListener("touchend", onTouchEnd, { passive: true });
  window.addEventListener("resize", scheduleRefresh, { passive: true });
  window.addEventListener("orientationchange", scheduleRefresh);
  window.addEventListener("load", scheduleRefresh, { once: true });
  window.addEventListener("pageshow", scheduleRefresh);
  root.addEventListener("keydown", onKeydown);
  musicCamera.addEventListener("transitionend", onMusicCameraTransitionEnd);
  if (explorePrompt) explorePrompt.addEventListener("click", showOrbit);
  deck.addEventListener("scroll", scheduleRailUpdate, { passive: true });
  compactLayout.addEventListener("change", scheduleRefresh);
  reduceMotion.addEventListener("change", scheduleRefresh);
  slides.forEach((slide) => {
    slide.querySelector(".cover-carousel-card-surface")?.addEventListener("click", onCardClick);
  });

  if ("ResizeObserver" in window) {
    const observer = new ResizeObserver(scheduleRefresh);
    observer.observe(stickyContent);
    observer.observe(deck);
  }

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(([entry]) => {
      state.visible = entry.isIntersecting;
      syncAmbientLoop();
    });
    observer.observe(scrollScene);
  }

  root.classList.add("is-enhanced", "is-orbit");
  scrollScene.classList.add("is-carousel-enhanced");

  if (!compact()) {
    updateOrbitGeometry();
    document.body.classList.add("is-cover-gesture-mode");
    resetDesktopCards();
    warmAfterCoverPaint();
  } else {
    refreshLayout();
  }

  /* 先让隐藏槽位稳定一帧，再开放正常动效，避免刷新时播放收起动画。 */
  window.requestAnimationFrame(() => {
    window.requestAnimationFrame(() => root.classList.add("is-ready"));
  });
})();
