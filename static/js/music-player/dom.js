/* =============================================================================
   dom.js — DOM 绑定与工具
   ---------------------------------------------------------------------------
   把模板契约从固定 ID 收敛为「根节点 + data-role / data-track」。
   bootstrap 阶段只拿一次引用，避免散落在函数里的 querySelector。
   ============================================================================= */
(function (global) {
  'use strict';

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(sel));
  }

  function fmtTime(sec) {
    if (!isFinite(sec) || sec < 0) return '0:00';
    var m = Math.floor(sec / 60);
    var s = Math.floor(sec % 60);
    return m + ':' + (s < 10 ? '0' + s : s);
  }

  function normSrc(src) {
    if (!src) return '';
    try { return new URL(src, window.location.href).pathname; }
    catch (e) { return src; }
  }
  // normSrc 用处：localStorage 里的 src 可能是绝对 URL，
  // 而模板 dataset.src 是相对路径，比较前必须统一成 pathname。

  /**
   * 绑定播放器 DOM。返回所有视图层句柄 + 曲目列表。
   * 必要节点缺失时打印一次告警并返回 null，让 bootstrap 决定是否继续。
   */
  function bindDom(playlistRoot, playerRoot) {
    if (!playlistRoot || !playerRoot) return null;

    var items = $$('[data-track]', playlistRoot);
    if (!items.length) return null;

    var audio = $('[data-role="audio"]', playerRoot);
    var prev  = $('[data-role="prev"]', playerRoot);
    var next  = $('[data-role="next"]', playerRoot);
    var tog   = $('[data-role="toggle"]', playerRoot);
    var cls   = $('[data-role="close"]', playerRoot);

    var coverEl  = $('[data-role="cover"]', playerRoot);
    var titleEl  = $('[data-role="title"]', playerRoot);
    var artistEl = $('[data-role="artist"]', playerRoot);
    var curEl    = $('[data-role="current"]', playerRoot);
    var durEl    = $('[data-role="duration"]', playerRoot);
    var progEl   = $('[data-role="progress"]', playerRoot);

    var modeBtn   = $('[data-role="mode"]', playlistRoot);
    var modeLabel = $('[data-role="mode-label"]', playlistRoot);
    var muteBtn   = $('[data-role="mute"]', playlistRoot);
    var volSlider = $('[data-role="volume"]', playlistRoot);
    var volLabel  = $('[data-role="volume-value"]', playlistRoot);

    var required = {
      audio: audio, prev: prev, next: next, toggle: tog,
      cover: coverEl, title: titleEl, progress: progEl
    };
    var missing = Object.keys(required).filter(function (k) { return !required[k]; });
    if (missing.length) {
      console.warn('[music-player] missing nodes: ' + missing.join(', '));
      return null;
    }

    return {
      items: items,
      audio: audio,
      cover: coverEl,
      buttons: {
        prev: prev, next: next, toggle: tog, close: cls,
        mode: modeBtn, mute: muteBtn
      },
      text: {
        title: titleEl, artist: artistEl,
        current: curEl, duration: durEl,
        mode: modeLabel, volume: volLabel
      },
      sliders: {
        progress: progEl, volume: volSlider
      }
    };
  }

  global.MusicPlayer = global.MusicPlayer || {};
  global.MusicPlayer.dom = {
    bind: bindDom,
    fmtTime: fmtTime,
    normSrc: normSrc
  };
})(window);