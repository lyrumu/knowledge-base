/* =============================================================================
   store.js — 播放状态机（纯逻辑）
   ---------------------------------------------------------------------------
   只描述当前曲目 / 模式 / 随机顺序。提供 select / next / prev / cycleMode，
   不碰 DOM、不碰 audio，便于单独写单元测试。
   ============================================================================= */
(function (global) {
  'use strict';

  var MODES = ['list', 'one', 'shuffle'];

  function shuffle(indices) {
    var arr = indices.slice();
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
    }
    return arr;
  }

  /**
   * enabledIndices(items) — 过滤掉 is-disabled 的曲目下标。
   */
  function enabledIndices(items) {
    var out = [];
    for (var i = 0; i < items.length; i++) {
      if (!items[i].classList.contains('is-disabled')) out.push(i);
    }
    return out;
  }

  function createStore(items, initial) {
    initial = initial || {};
    var state = {
      items: items,
      curIndex: -1,
      mode: initial.mode || 'list',
      shuffleOrder: [],
      shufflePos: 0
    };

    function select(i) {
      if (i < 0 || i >= items.length) return false;
      state.curIndex = i;
      // 进入 shuffle 模式且当前曲不在随机顺序里时，从当前位置重建顺序
      // —— 避免下次 next() 跳到一首"刚听过"的曲子
      if (state.mode === 'shuffle' && state.shuffleOrder.indexOf(i) < 0) {
        state.shuffleOrder = shuffle(enabledIndices(items));
        state.shufflePos = state.shuffleOrder.indexOf(i);
        if (state.shufflePos < 0) state.shufflePos = 0;
      }
      return true;
    }

    function current() {
      if (state.curIndex < 0) return null;
      var el = items[state.curIndex];
      if (!el) return null;
      return {
        index: state.curIndex,
        el: el,
        src: el.dataset.src || '',
        cover: el.dataset.cover || '',
        title: el.dataset.title || '',
        artist: el.dataset.artist || '',
        album: el.dataset.album || '',
        duration: el.dataset.duration || ''
      };
    }

    function cycleMode() {
      var idx = MODES.indexOf(state.mode);
      state.mode = MODES[(idx + 1) % MODES.length];
      if (state.mode === 'shuffle') {
        state.shuffleOrder = shuffle(enabledIndices(items));
        state.shufflePos = state.curIndex >= 0
          ? state.shuffleOrder.indexOf(state.curIndex)
          : 0;
        if (state.shufflePos < 0) state.shufflePos = 0;
      }
      return state.mode;
    }

    function _step(delta) {
      var enabled = enabledIndices(items);
      if (!enabled.length) return -1;
      if (state.mode === 'shuffle') {
        if (!state.shuffleOrder.length) {
          state.shuffleOrder = enabled;
          state.shufflePos = state.curIndex >= 0
            ? state.shuffleOrder.indexOf(state.curIndex)
            : 0;
          if (state.shufflePos < 0) state.shufflePos = 0;
        }
        var len = state.shuffleOrder.length;
        state.shufflePos = ((state.shufflePos + delta) % len + len) % len;
        return state.shuffleOrder[state.shufflePos];
      }
      // list / one 切歌：在 enabledIndices 数组里循环，禁用曲目直接跳过
      // —— 比"按 items.length 循环 + 检查 disabled"更直接，因为 enabled 已经过滤过
      if (!enabled.length) return -1;
      if (state.curIndex < 0) {
        // 还没选过曲时，next/prev 都从首曲开始（与原代码 j=0 起手行为一致）
        state.curIndex = enabled[0];
        return state.curIndex;
      }
      var pos = enabled.indexOf(state.curIndex);
      if (pos < 0) {
        // 当前曲被运行时标记为 disabled，回退到第一首
        state.curIndex = enabled[0];
        return state.curIndex;
      }
      var nextPos = (pos + (delta > 0 ? 1 : -1) + enabled.length) % enabled.length;
      state.curIndex = enabled[nextPos];
      return state.curIndex;
    }

    function next() { return _step(1); }
    function prev() { return _step(-1); }

    // peekNext / peekPrev 只读不写 —— 用于预取"下一首要播什么"，不影响 store 状态
    function peekNext() { return _peek(1); }
    function peekPrev() { return _peek(-1); }
    function _peek(delta) {
      var enabled = enabledIndices(items);
      if (!enabled.length) return -1;
      if (state.curIndex < 0) return enabled[0];
      var pos = enabled.indexOf(state.curIndex);
      if (pos < 0) return enabled[0];
      var p = (pos + (delta > 0 ? 1 : -1) + enabled.length) % enabled.length;
      return enabled[p];
    }

    function mode() { return state.mode; }

    function snapshot() {
      return {
        index: state.curIndex,
        mode: state.mode
      };
    }

    return {
      select: select,
      current: current,
      cycleMode: cycleMode,
      next: next,
      prev: prev,
      peekNext: peekNext,
      peekPrev: peekPrev,
      mode: mode,
      snapshot: snapshot
    };
  }

  global.MusicPlayer = global.MusicPlayer || {};
  global.MusicPlayer.store = {
    MODES: MODES,
    create: createStore
  };
})(window);