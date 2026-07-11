/* =============================================================================
   controller.js — 播放控制器
   ---------------------------------------------------------------------------
   把 store / view / storage / audio 串起来：
   - 接收 UI 事件 → 推进 store → 渲染 view → 写 storage
   - 不再同时直接读写 DOM 与 localStorage
   优化：事件委托 + 分页加载
   ============================================================================= */
(function (global) {
  'use strict';

  function createController(opts) {
    var dom = opts.dom;
    var store = opts.store;
    var view = opts.view;
    var storage = opts.storage;
    var audio = dom.audio;

    var volume = storage.readVolume(0.8);
    var isMuted = false;
    var prevVol = volume;

    // 预取用的隐藏 audio：浏览器对 src 的 Range 请求会进磁盘缓存，
    // 切到对应曲目时直接从缓存读，几乎瞬时
    var prebuffer = document.createElement('audio');
    prebuffer.preload = 'auto';
    prebuffer.hidden = true;
    // 放进 player 根节点外（避免被 view 的 class 操作影响）
    document.body.appendChild(prebuffer);

    // ========== 分页加载逻辑 ==========
    var pageSize = parseInt(dom.playlistRoot.dataset.pageSize, 10) || 7;
    var total = parseInt(dom.playlistRoot.dataset.total, 10) || dom.items.length;
    var currentLoaded = pageSize;
    var loadMoreBtn = dom.playlistRoot.querySelector('[data-role="load-more"]');
    var loadMoreCount = dom.playlistRoot.querySelector('[data-role="load-more-count"]');

    function updateLoadMoreBtn() {
      var remaining = total - currentLoaded;
      if (remaining <= 0) {
        loadMoreBtn.hidden = true;
        return;
      }
      loadMoreBtn.hidden = false;
      loadMoreCount.textContent = '(' + remaining + ')';
    }

    function loadMore() {
      var count = 0;
      for (var i = currentLoaded; i < Math.min(currentLoaded + pageSize, total); i++) {
        dom.items[i].classList.add('is-revealed');
        dom.items[i].hidden = false;
        count++;
      }
      currentLoaded += count;
      updateLoadMoreBtn();
    }

    function prefetchNext() {
      // 用 peekNext 只读不写，避免破坏 store 状态
      var idx = store.peekNext();
      if (idx < 0) return;
      var src = dom.items[idx].dataset.src;
      if (!src) return;
      var abs = src;
      try { abs = new URL(src, window.location.href).href; } catch (e) {}
      if (prebuffer.src !== abs) prebuffer.src = abs;
    }

    function snapshotForStorage() {
      var cur = store.current();
      return {
        index: cur ? cur.index : -1,
        time:  audio.currentTime || 0,
        src:   audio.currentSrc || (cur ? cur.src : ''),
        playing: !audio.paused
      };
    }

    function saveState() {
      var cur = store.current();
      if (!cur) return;
      storage.writeState(snapshotForStorage());
    }

    function loadIndex(i, autoplay) {
      if (!store.select(i)) return;
      var track = store.current();
      view.renderTrack(track, track.duration);
      view.show();
      view.highlight(store.snapshot().index);

      // 切歌期间 UI 给个"加载中"反馈，避免按钮看上去像卡死
      view.showLoading(true);
      audio.src = track.src;
      audio.addEventListener('loadedmetadata', function once() {
        audio.removeEventListener('loadedmetadata', once);
        if (isFinite(audio.duration)) {
          view.setProgress(audio.currentTime, audio.duration, track.duration);
        }
      });
      audio.addEventListener('canplay', function onceC() {
        audio.removeEventListener('canplay', onceC);
        view.showLoading(false);
      });
      // 5s 兜底：万一 canplay 不触发（断网/异常），强制解除 loading 避免永久卡住
      audio.addEventListener('error', function onceE() {
        audio.removeEventListener('error', onceE);
        view.showLoading(false);
      });

      if (autoplay) {
        audio.play().then(function () {
          view.setPlaying(true);
          saveState();
          // 播放开始 1s 后再预取，给当前歌曲的 canplay 留出带宽
          setTimeout(prefetchNext, 1000);
        }).catch(function () {
          view.setPlaying(false);
        });
      } else {
        audio.pause();
        view.setPlaying(false);
      }
    }

    function play() {
      var snap = store.snapshot();
      if (snap.index < 0 && dom.items.length) {
        loadIndex(store.next(), true);
        return;
      }
      audio.play().then(function () {
        view.setPlaying(true);
        saveState();
      }).catch(function () {});
    }

    function pause() {
      audio.pause();
      view.setPlaying(false);
    }

    function toggle() { audio.paused ? play() : pause(); }

    function next() {
      var i = store.next();
      if (i >= 0) loadIndex(i, true);
    }

    // prev() 的二次点击语义：当前曲已播 > 3s 时回到开头（不切曲）
    // —— 这条规则与 macOS Music / Spotify 的"上一首"一致，区分"重听本曲"和"切到上一首"
    function prev() {
      if (audio.currentTime > 3) { audio.currentTime = 0; return; }
      var i = store.prev();
      if (i >= 0) loadIndex(i, true);
    }

    // 拖动 slider 始终取消静音（因为用户主动调整音量 = 解除静音意图）
    function setVolume(v, persist) {
      v = Math.max(0, Math.min(1, v));
      volume = v;
      isMuted = false;
      view.renderVolume(volume, false);
      if (persist !== false) storage.writeVolume(v);
    }

    // 静音切换：记住当前音量，恢复时用 prevVol 而非直接置 0
    function toggleMute() {
      if (isMuted) {
        setVolume(prevVol || 0.8);
      } else {
        prevVol = volume;
        isMuted = true;
        view.renderVolume(0, true);
      }
    }

    function cycleMode() {
      var mode = store.cycleMode();
      view.renderMode(mode);
      storage.writeMode(mode);
    }

    function onProgressInput() {
      if (!isFinite(audio.duration)) return;
      audio.currentTime = (dom.sliders.progress.value / 1000) * audio.duration;
      view.setProgress(audio.currentTime, audio.duration);
    }

    function onTimeUpdate() {
      view.setProgress(audio.currentTime, audio.duration);
      saveState();
    }

    // 'one' 模式由 audio.ended 自行回放（不调 next()），其它模式交给 next() 切下一首
    function onEnded() {
      if (store.mode() === 'one') {
        audio.currentTime = 0;
        audio.play().catch(function () {});
      } else {
        next();
      }
    }

    // MEDIA_ERR_ABORTED (code=1) = 用户主动 abort（切歌、暂停触发的取消请求），不是真错误
    // code 2/3/4 = 网络/解码/格式问题，跳过当前曲避免死循环卡住
    function onAudioError() {
      var code = audio.error && audio.error.code;
      if (code === 1) return;
      console.warn('[music-player] audio load error (code=' + code + '), skipping to next');
      next();
    }

    function onItemClick(i, e) {
      // 点击下载按钮时不切歌（事件冒泡时拦截）
      if (e && e.target && e.target.closest('.music-item-download')) return;
      // 没有 src 的占位项不响应
      var el = dom.items[i];
      if (el && el.classList.contains('is-disabled')) return;
      // 点击当前曲 = 切换播放/暂停（而不是重新从头开始）
      if (i === store.snapshot().index) { toggle(); return; }
      loadIndex(i, true);
    }

    function close() {
      audio.pause();
      view.hide();
      storage.clearState();
    }

    // 键盘快捷键：Space 切播放、Shift+← / Shift+→ 切歌。
// 在 INPUT/TEXTAREA/contenteditable 里输入时放行，避免吞掉用户输入。
// 故意不限制焦点必须在播放器内 —— 与原行为一致（用户已习惯全站快捷键）。
function onKey(e) {
      var t = e.target;
      if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
      if (e.code === 'Space') { e.preventDefault(); toggle(); }
      else if (e.key === 'ArrowRight' && e.shiftKey) { e.preventDefault(); next(); }
      else if (e.key === 'ArrowLeft'  && e.shiftKey) { e.preventDefault(); prev(); }
    }

    function bind() {
      dom.buttons.prev.addEventListener('click', prev);
      dom.buttons.next.addEventListener('click', next);
      dom.buttons.toggle.addEventListener('click', toggle);
      if (dom.buttons.close) dom.buttons.close.addEventListener('click', function (e) { e.preventDefault(); close(); });
      if (dom.buttons.mode) dom.buttons.mode.addEventListener('click', cycleMode);
      if (dom.buttons.mute) dom.buttons.mute.addEventListener('click', toggleMute);
      if (dom.sliders.volume) {
        dom.sliders.volume.addEventListener('input', function () {
          setVolume(parseInt(dom.sliders.volume.value, 10) / 100);
        });
      }
      dom.sliders.progress.addEventListener('input', onProgressInput);

      audio.addEventListener('timeupdate', onTimeUpdate);
      audio.addEventListener('ended', onEnded);
      audio.addEventListener('error', onAudioError);

      // ========== 事件委托（替代 forEach 监听器）==========
      dom.playlistRoot.addEventListener('click', function (e) {
        // 加载更多按钮
        if (e.target.closest('[data-role="load-more"]')) {
          loadMore();
          return;
        }
        // 歌曲项点击
        var item = e.target.closest('[data-track]');
        if (item) {
          var idx = parseInt(item.dataset.index, 10);
          if (!isNaN(idx)) onItemClick(idx, e);
        }
      });

      document.addEventListener('keydown', onKey);
    }

    function init() {
      view.renderMode(store.mode());
      view.renderVolume(volume, false);
      bind();

      // ========== 初始化分页状态 ==========
      // 初始只显示第一页
      for (var i = 0; i < dom.items.length; i++) {
        if (i >= pageSize) {
          dom.items[i].classList.add('is-revealed');
          dom.items[i].hidden = true;
        } else {
          dom.items[i].classList.add('is-revealed');
          dom.items[i].hidden = false;
        }
      }
      updateLoadMoreBtn();
    }

    // 恢复上次播放位置：按 src 匹配（而不是按 index）—— 歌单顺序变了也不会错播。
// loadedmetadata 事件分两段：loadIndex() 自己监听一次拿真实时长；restore 也可能
// 监听一次恢复 currentTime。两段互不冲突，因为 once() 会自摘除。
function restore() {
      var saved = storage.readState();
      if (!saved || !saved.src) return false;
      var savedSrc = global.MusicPlayer.dom.normSrc(saved.src);
      var items = dom.items;
      for (var i = 0; i < items.length; i++) {
        if (global.MusicPlayer.dom.normSrc(items[i].dataset.src) === savedSrc) {
          loadIndex(i, false);
          function apply() {
            if (isFinite(saved.time)) audio.currentTime = saved.time;
            view.setProgress(audio.currentTime, audio.duration);
            if (saved.playing) {
              audio.play().then(function () {
                view.setPlaying(true);
                saveState();
              }).catch(function () {});
            }
          }
          if (audio.readyState >= 1) apply();
          else {
            audio.addEventListener('loadedmetadata', function onceR() {
              audio.removeEventListener('loadedmetadata', onceR);
              apply();
            });
          }
          return true;
        }
      }
      return false;
    }

    return {
      init: init,
      restore: restore,
      // 暴露给测试或外部扩展
      _internal: { loadIndex: loadIndex, setVolume: setVolume, next: next, prev: prev, cycleMode: cycleMode }
    };
  }

  global.MusicPlayer = global.MusicPlayer || {};
  global.MusicPlayer.controller = { create: createController };
})(window);