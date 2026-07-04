/* =============================================================================
   view.js — 视图层
   ---------------------------------------------------------------------------
   只负责把状态写到 DOM。控制器调度，视图渲染。
   ============================================================================= */
(function (global) {
  'use strict';

  var MODES = window.MusicPlayer.store.MODES;
  var MODE_ICONS = {
    list: '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4 4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/></svg>',
    one:  '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4 4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/><text x="12" y="14" font-size="8" font-weight="600" fill="currentColor" stroke="none" text-anchor="middle" dominant-baseline="middle" font-family="sans-serif">1</text></svg>',
    shuffle: '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 18h1.4c1.3 0 2.5-.6 3.3-1.7l6.1-8.6c.7-1.1 2-1.7 3.3-1.7H22"/><path d="m18 2 4 4-4 4"/><path d="M2 6h1.9c1.5 0 2.9.9 3.6 2.2"/><path d="M22 18h-5.9c-1.3 0-2.6-.7-3.3-1.8l-.5-.8"/><path d="m18 14 4 4-4 4"/></svg>'
  };
  var MODE_TITLES = { list: 'Loop All', one: 'Loop One', shuffle: 'Shuffle' };

  var PAUSE_SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>';

  function fmt(sec) { return window.MusicPlayer.dom.fmtTime(sec); }

  function createView(dom) {
    var player = dom.buttons.toggle.closest('[data-music-player]') || document;
    var items = dom.items;
    var buttons = dom.buttons;
    var text = dom.text;
    var sliders = dom.sliders;
    var cover = dom.cover;
    var audio = dom.audio;

    // 把模板里渲染出的播放图标缓存下来，setIcon(playing=false) 时再回填
    // —— 避免播放图标丢失（每次 setIcon 都重新生成 SVG 字符串会绕一圈）
    var cachedPlaySvg = buttons.toggle.innerHTML;

    function highlight(i) {
      for (var k = 0; k < items.length; k++) {
        items[k].classList.toggle('is-current', k === i);
      }
    }

    function show() { player.classList.add('is-visible'); }
    function hide() {
      player.classList.remove('is-visible', 'is-playing');
      highlight(-1);
    }

    function renderTrack(track, fallbackDuration) {
      if (!track) return;
      if (text.title)  text.title.textContent  = track.title  || '未知曲目';
      if (text.artist) text.artist.textContent = track.artist ? '· ' + track.artist : '';
      if (cover) {
        cover.src = track.cover || '';
        cover.alt = track.title || '';
      }
      if (text.duration) text.duration.textContent = fallbackDuration || track.duration || '0:00';
      if (text.current)  text.current.textContent  = '0:00';
    }

    function setProgress(currentTime, duration, fallbackDuration) {
      var dur = isFinite(duration) ? duration : 0;
      var pct = dur ? (currentTime / dur) : 0;
      sliders.progress.value = Math.round(pct * 1000);
      sliders.progress.style.setProperty('--progress', (pct * 100).toFixed(2) + '%');
      if (text.current)  text.current.textContent  = fmt(currentTime);
      if (text.duration) text.duration.textContent = fmt(isFinite(duration) ? duration : (fallbackDuration || 0));
    }

    function setIcon(playing) {
      buttons.toggle.innerHTML = playing ? PAUSE_SVG : (cachedPlaySvg || '');
    }

    function setPlaying(playing) {
      player.classList.toggle('is-playing', !!playing);
      setIcon(!!playing);
    }

    function renderMode(mode) {
      if (buttons.mode) {
        buttons.mode.innerHTML = MODE_ICONS[mode] || '';
        buttons.mode.setAttribute('title', MODE_TITLES[mode] || '');
        buttons.mode.setAttribute('aria-label', '播放模式: ' + (MODE_TITLES[mode] || ''));
        buttons.mode.classList.toggle('is-active', mode !== 'list');
      }
      if (text.mode) text.mode.textContent = MODE_TITLES[mode] || '';
    }

    function renderVolume(volume, isMuted) {
      var v = isMuted ? 0 : volume;
      var pct = Math.round(v * 100);
      if (sliders.volume) {
        sliders.volume.value = pct;
        sliders.volume.style.setProperty('--vol', pct + '%');
      }
      if (text.volume) text.volume.textContent = pct + '%';
      if (audio) audio.volume = v;
      if (buttons.mute) {
        var icon15 = '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">';
        var icon;
        if (v === 0) {
          icon = icon15 + '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><line x1="22" y1="9" x2="16" y2="15"/><line x1="16" y1="9" x2="22" y2="15"/></svg>';
        } else if (v < 0.5) {
          icon = icon15 + '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>';
        } else {
          icon = icon15 + '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>';
        }
        buttons.mute.innerHTML = icon;
      }
    }

    return {
      highlight: highlight,
      show: show, hide: hide,
      renderTrack: renderTrack,
      setProgress: setProgress,
      setIcon: setIcon,
      setPlaying: setPlaying,
      renderMode: renderMode,
      renderVolume: renderVolume
    };
  }

  global.MusicPlayer = global.MusicPlayer || {};
  global.MusicPlayer.view = { create: createView };
})(window);