/* =============================================================================
   store.js — 播放状态机（纯逻辑）
   ---------------------------------------------------------------------------
   只描述当前曲目 / 模式 / 随机顺序。提供 select / next / prev / cycleMode，
   不碰 DOM、不碰 audio，便于单独写单元测试。
   ============================================================================= */
(function (global) {
  'use strict';

  var MODES = ['list', 'one', 'shuffle'];

  // 随机播放时的历史记录长度（避免连续重复的曲目数）
  var SHUFFLE_HISTORY_SIZE = 5;

  /**
   * Fisher-Yates 洗牌算法（纯随机，不含历史排除）
   */
  function shuffle(indices) {
    var arr = indices.slice();
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
    }
    return arr;
  }

  /**
   * 增强随机选择：从可用曲目中随机选一首，排除 recentHistory 中的曲目
   * - 当可用曲目足够多时（> SHUFFLE_HISTORY_SIZE），确保不选最近播放过的
   * - 当曲目数不够时（如歌单很短），退化为普通随机
   */
  function smartShufflePick(enabled, recentHistory) {
    // 过滤掉最近播放过的曲目
    var historySet = {};
    for (var k = 0; k < recentHistory.length; k++) {
      historySet[recentHistory[k]] = true;
    }
    var candidates = [];
    for (var i = 0; i < enabled.length; i++) {
      if (!historySet[enabled[i]]) {
        candidates.push(enabled[i]);
      }
    }
    // 如果候选池空了（曲目太少），用全部可用曲目
    if (!candidates.length) candidates = enabled;
    // 从候选池随机选一首
    return candidates[Math.floor(Math.random() * candidates.length)];
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
      recentHistory: []   // 随机模式历史，用于避免连续重复
    };

    function select(i) {
      if (i < 0 || i >= items.length) return false;
      state.curIndex = i;
      // shuffle 模式：把选中的曲目从历史中移除（避免刚点选的歌马上又被随机到）
      if (state.mode === 'shuffle') {
        var hPos = state.recentHistory.indexOf(i);
        if (hPos >= 0) state.recentHistory.splice(hPos, 1);
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
        coverLqip: el.dataset.coverLqip || '',
        coverSrcset: el.dataset.coverSrcset || '',
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
        // 进入/切换到 shuffle 模式：重置历史，确保全新开始
        state.recentHistory = [];
      }
      return state.mode;
    }

    function _step(delta) {
      var enabled = enabledIndices(items);
      if (!enabled.length) return -1;
      if (state.mode === 'shuffle') {
        // 增强随机模式：记录当前曲到历史，再选下一曲
        if (state.curIndex >= 0) {
          state.recentHistory.push(state.curIndex);
          if (state.recentHistory.length > SHUFFLE_HISTORY_SIZE) {
            state.recentHistory.shift();
          }
        }
        return smartShufflePick(enabled, state.recentHistory);
      }
      // list / one 切歌
      if (state.curIndex < 0) {
        state.curIndex = enabled[0];
        return state.curIndex;
      }
      var pos = enabled.indexOf(state.curIndex);
      if (pos < 0) { state.curIndex = enabled[0]; return state.curIndex; }
      var nextPos = (pos + (delta > 0 ? 1 : -1) + enabled.length) % enabled.length;
      state.curIndex = enabled[nextPos];
      return state.curIndex;
    }

    function next() { return _step(1); }
    function prev() { return _step(-1); }

    /**
     * peekNext / peekPrev — 只读预测，不修改状态
     * 在增强随机模式下，模拟 next() 的历史行为来预测下一曲
     */
    function peekNext() {
      var enabled = enabledIndices(items);
      if (!enabled.length) return -1;
      if (state.mode === 'shuffle') {
        // 模拟 next() 会产生的历史：把当前曲加入历史
        var simHistory = state.recentHistory.slice();
        if (state.curIndex >= 0) {
          simHistory.push(state.curIndex);
          if (simHistory.length > SHUFFLE_HISTORY_SIZE) simHistory.shift();
        }
        return smartShufflePick(enabled, simHistory);
      }
      if (state.curIndex < 0) return enabled[0];
      var pos = enabled.indexOf(state.curIndex);
      if (pos < 0) return enabled[0];
      return enabled[(pos + 1 + enabled.length) % enabled.length];
    }

    function peekPrev() {
      var enabled = enabledIndices(items);
      if (!enabled.length) return -1;
      // prev 语义：当前曲已播 > 3s 时回到开头（由 controller 判断）
      // peek 只做最简单预测
      if (state.curIndex < 0) return enabled[enabled.length - 1];
      var pos = enabled.indexOf(state.curIndex);
      if (pos < 0) return enabled[enabled.length - 1];
      return enabled[(pos - 1 + enabled.length) % enabled.length];
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