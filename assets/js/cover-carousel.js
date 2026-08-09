/* Homepage cover — finite Vertical sequential reveal controller. */
(function () {
  "use strict";

  const root = document.querySelector("[data-cover-carousel]");
  if (!root) return;

  const scrollScene = root.closest(".cover-page");
  const stickyContent = root.closest(".cover-content");
  const deck = root.querySelector(".cover-carousel-deck");
  const intro = root.querySelector("[data-cover-intro]");
  const explorePrompt = root.querySelector("[data-cover-explore]");
  const introLinks = intro ? Array.from(intro.querySelectorAll("a")) : [];
  const slides = Array.from(root.querySelectorAll("[data-cover-carousel-slide]"));
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const compactLayout = window.matchMedia("(max-width: 720px)");

  if (!scrollScene || !stickyContent || !deck || slides.length !== 3) return;

  const state = {
    frame: 0,
    railFrame: 0,
    resizeFrame: 0,
    railIndex: 0,
    measurements: null,
  };

  const clamp = (value, min, max) => Math.min(Math.max(value, min), max);
  const compact = () => compactLayout.matches || reduceMotion.matches;
  const easeInOutSine = (value) => -(Math.cos(Math.PI * value) - 1) / 2;
  const cardRevealDuration = 0.4;
  const cardRevealStagger = 0.22;
  const cardsReadyProgress = clamp(
    (slides.length - 1) * cardRevealStagger + cardRevealDuration,
    0,
    1
  );

  function setInert(element, inert) {
    if (!element) return;
    if (inert) {
      element.setAttribute("inert", "");
    } else {
      element.removeAttribute("inert");
    }
  }

  function measure() {
    const rect = scrollScene.getBoundingClientRect();
    const sceneTop = window.scrollY + rect.top;
    const headerOffset = parseFloat(getComputedStyle(root).getPropertyValue("--cover-header-offset")) || 0;
    const start = sceneTop - headerOffset;
    const distance = Math.max(scrollScene.offsetHeight - stickyContent.offsetHeight, 1);
    state.measurements = { start, distance };
  }

  function sceneProgress() {
    if (!state.measurements) measure();
    const { start, distance } = state.measurements;
    return clamp((window.scrollY - start) / distance, 0, 1);
  }

  function revealProgress(progress, start) {
    return easeInOutSine(clamp((progress - start) / cardRevealDuration, 0, 1));
  }

  function horizontalSpacing() {
    return clamp(deck.clientWidth * 0.3, 180, 470);
  }

  function applyVerticalProgress(progress) {
    const spacing = horizontalSpacing();
    const centre = (slides.length - 1) / 2;
    const entryX = Math.max(deck.clientWidth * 0.72, spacing * 1.8);
    const promptFade = clamp(progress / 0.16, 0, 1);
    const introFade = easeInOutSine(clamp(progress / 0.2, 0, 1));
    const fieldsReveal = easeInOutSine(clamp((progress - 0.08) / 0.16, 0, 1));

    root.style.setProperty("--cover-scene-progress", String(progress));
    root.style.setProperty("--cover-explore-opacity", String(1 - promptFade));
    root.style.setProperty("--cover-explore-y", `${promptFade * 0.65}rem`);
    root.style.setProperty("--cover-intro-opacity", String(1 - introFade));
    root.style.setProperty("--cover-intro-y", `${introFade * -0.7}rem`);
    root.style.setProperty("--cover-fields-opacity", String(fieldsReveal));
    root.style.setProperty("--cover-fields-y", `${(1 - fieldsReveal) * 0.5}rem`);
    introLinks.forEach((link) => setInert(link, introFade >= 0.94));
    setInert(explorePrompt, promptFade >= 0.94);

    slides.forEach((slide, index) => {
      const entry = revealProgress(progress, index * cardRevealStagger);
      const finalX = (index - centre) * spacing;
      const x = entryX + (finalX - entryX) * entry;
      const surface = slide.querySelector(".cover-carousel-card-surface");

      slide.style.setProperty("--cover-reveal-x", `${x}px`);
      slide.style.setProperty("--cover-reveal-opacity", String(entry));
      slide.style.setProperty("--cover-reveal-scale", String(0.965 + entry * 0.035));
      slide.style.setProperty("--cover-reveal-saturation", String(0.7 + entry * 0.3));
      slide.style.setProperty("--cover-reveal-layer", String(10 + index));
      slide.dataset.state = entry >= 0.995 ? "revealed" : entry > 0 ? "revealing" : "pending";
      // 只在卡片完全不可见时禁用链接；一旦进入画面，整张卡片都应可点击。
      setInert(surface, entry <= 0);
    });
  }

  function updateFromScroll() {
    state.frame = 0;
    if (compact()) return;
    applyVerticalProgress(sceneProgress());
  }

  function scheduleScrollUpdate() {
    if (state.frame) return;
    state.frame = window.requestAnimationFrame(updateFromScroll);
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
      slide.dataset.state = active ? "active" : slideIndex < state.railIndex ? "previous" : "next";
      setInert(slide.querySelector(".cover-carousel-card-surface"), false);
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

  function refreshLayout() {
    state.resizeFrame = 0;
    measure();
    if (compact()) {
      introLinks.forEach((link) => setInert(link, false));
      setRailIndex(closestRailIndex());
    } else {
      applyVerticalProgress(sceneProgress());
    }
  }

  function scheduleRefresh() {
    if (state.resizeFrame) return;
    state.resizeFrame = window.requestAnimationFrame(refreshLayout);
  }

  function showAllCards(event) {
    event.preventDefault();

    if (compact()) {
      deck.scrollIntoView({ block: "start", behavior: "auto" });
      return;
    }

    measure();
    const targetScroll = state.measurements.start + state.measurements.distance * cardsReadyProgress;
    window.scrollTo({ top: targetScroll, behavior: "auto" });
    applyVerticalProgress(cardsReadyProgress);
  }

  window.addEventListener("scroll", scheduleScrollUpdate, { passive: true });
  window.addEventListener("resize", scheduleRefresh, { passive: true });
  window.addEventListener("orientationchange", scheduleRefresh);
  window.addEventListener("load", scheduleRefresh, { once: true });
  window.addEventListener("pageshow", scheduleRefresh);
  if (explorePrompt) explorePrompt.addEventListener("click", showAllCards);
  deck.addEventListener("scroll", scheduleRailUpdate, { passive: true });
  compactLayout.addEventListener("change", scheduleRefresh);
  reduceMotion.addEventListener("change", scheduleRefresh);

  if ("ResizeObserver" in window) {
    const observer = new ResizeObserver(scheduleRefresh);
    observer.observe(stickyContent);
    observer.observe(deck);
  }

  root.classList.add("is-enhanced", "is-vertical");
  scrollScene.classList.add("is-carousel-enhanced");
  measure();

  const navigation = performance.getEntriesByType("navigation")[0];
  if (!compact() && navigation && navigation.type === "reload") {
    window.scrollTo({ top: state.measurements.start, behavior: "auto" });
    applyVerticalProgress(0);
  } else {
    refreshLayout();
  }
})();
