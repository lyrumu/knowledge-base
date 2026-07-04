/* =============================================================================
   storage.js — 本地持久化适配层
   ---------------------------------------------------------------------------
   体积、模式、播放位置三个键的读写都收敛在这里，控制器只看到 save/load/clear。
   后续要换成 IndexedDB 或 sessionStorage，只改这一层。
   ============================================================================= */
(function (global) {
  'use strict';

  var KEYS = {
    state:  'lyrumu:music-player:state-v1',
    mode:   'lyrumu:music-player:mode-v1',
    volume: 'lyrumu:music-player:volume-v1'
  };

  function safeGet(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }
  function safeSet(key, value) {
    try { localStorage.setItem(key, value); } catch (e) {}
  }
  function safeRemove(key) {
    try { localStorage.removeItem(key); } catch (e) {}
  }

  function readMode() {
    var v = safeGet(KEYS.mode);
    // 只接受三种合法值；storage 被外部污染或旧版本残留 → 退回默认 list
    return v === 'list' || v === 'one' || v === 'shuffle' ? v : 'list';
  }
  function writeMode(mode) { safeSet(KEYS.mode, mode); }

  function readVolume(defaults) {
    var raw = safeGet(KEYS.volume);
    var v = parseFloat(raw);
    if (!isFinite(v)) return defaults;
    return Math.max(0, Math.min(1, v));
  }
  function writeVolume(v) { safeSet(KEYS.volume, String(v)); }

  function readState() {
    var raw = safeGet(KEYS.state);
    if (!raw) return null;
    try {
      var s = JSON.parse(raw);
      if (!s || typeof s !== 'object') return null;
      return s;
    } catch (e) { return null; }
  }
  function writeState(snapshot) {
    if (!snapshot || !snapshot.src) return;
    safeSet(KEYS.state, JSON.stringify(snapshot));
  }
  function clearState() { safeRemove(KEYS.state); }

  global.MusicPlayer = global.MusicPlayer || {};
  global.MusicPlayer.storage = {
    KEYS: KEYS,
    readMode: readMode, writeMode: writeMode,
    readVolume: readVolume, writeVolume: writeVolume,
    readState: readState, writeState: writeState,
    clearState: clearState
  };
})(window);