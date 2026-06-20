/* =============================================================================
   music-player.js
   ---------------------------------------------------------------------------
   全局粘性音乐播放器
   - 点击 .music-item 切歌 + 自动播放
   - 上一首 / 下一首 / 播放-暂停
   - 进度条拖动跳转
   - 自动播放下一首（列表循环）
   - 当前曲目高亮 + 均衡器动画（CSS 已就位）
   - localStorage 记忆播放位置
   ---------------------------------------------------------------------------
   依赖：layouts/partials/music-player.html + layouts/shortcodes/music-list.html
   入口：DOMContentLoaded 时自动 init；只在页面存在 .music-item 时才激活
   ============================================================================= */
(function () {
  'use strict';

  // ---------- 工具 ----------
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  function fmtTime(sec) {
    if (!isFinite(sec) || sec < 0) return '0:00';
    var m = Math.floor(sec / 60);
    var s = Math.floor(sec % 60);
    return m + ':' + (s < 10 ? '0' + s : s);
  }

  // ---------- 入口 ----------
  document.addEventListener('DOMContentLoaded', function () {
    var items = $$('.music-item');
    var player = $('#music-player');
    if (!items.length || !player) return; // 没歌或没播放器，跳过

    var audio   = $('#music-player-audio');
    var btnPrev = $('#music-player-prev');
    var btnNext = $('#music-player-next');
    var btnTog  = $('#music-player-toggle');
    var btnCls  = $('#music-player-close');
    var prog    = $('#music-player-progress');
    var titleEl = $('#music-player-title');
    var artistEl = $('#music-player-artist');
    var coverEl = $('#music-player-cover');
    var curEl   = $('#music-player-current');
    var durEl   = $('#music-player-duration');

    // play / pause icon 缓存（按钮里第一个 svg）
    var PLAY_SVG  = btnTog.innerHTML;
    var PAUSE_SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>';
    function setIcon(playing) { btnTog.innerHTML = playing ? PAUSE_SVG : PLAY_SVG; }

    // 当前 index（-1 表示还没播过）
    var curIndex = -1;

    function itemData(i) {
      var el = items[i];
      if (!el) return null;
      return {
        el:      el,
        src:     el.dataset.src,
        cover:   el.dataset.cover,
        title:   el.dataset.title,
        artist:  el.dataset.artist,
        album:   el.dataset.album,
        duration: el.dataset.duration
      };
    }

    function highlight(i) {
      items.forEach(function (el, idx) { el.classList.toggle('is-current', idx === i); });
    }

    function showPlayer() { player.classList.add('is-visible'); }
    function hidePlayer() {
      player.classList.remove('is-visible', 'is-playing');
      audio.pause();
      curIndex = -1;
      highlight(-1);
    }

    function setProgressUI() {
      var pct = audio.duration ? (audio.currentTime / audio.duration) : 0;
      prog.value = Math.round(pct * 1000);
      prog.style.setProperty('--progress', (pct * 100).toFixed(2) + '%');
      curEl.textContent = fmtTime(audio.currentTime);
      if (isFinite(audio.duration)) durEl.textContent = fmtTime(audio.duration);
    }

    function loadIndex(i, autoplay) {
      var d = itemData(i);
      if (!d) return;
      curIndex = i;
      highlight(i);
      showPlayer();

      titleEl.textContent  = d.title || '未知曲目';
      artistEl.textContent = d.artist ? '· ' + d.artist : '';
      coverEl.src          = d.cover || '';
      coverEl.alt          = d.title || '';
      // 占位显示的时长
      durEl.textContent    = d.duration || '0:00';
      curEl.textContent    = '0:00';

      audio.src = d.src;
      // 加载完 metadata 后再显示真实时长
      audio.addEventListener('loadedmetadata', function once() {
        audio.removeEventListener('loadedmetadata', once);
        if (isFinite(audio.duration)) {
          durEl.textContent = fmtTime(audio.duration);
        }
      });

      if (autoplay) {
        audio.play().then(function () {
          player.classList.add('is-playing');
          setIcon(true);
          savePos();
        }).catch(function () {
          // 自动播放被浏览器拦截：保持暂停状态
          player.classList.remove('is-playing');
          setIcon(false);
        });
      } else {
        audio.pause();
        player.classList.remove('is-playing');
        setIcon(false);
      }
    }

    function play() {
      if (curIndex < 0 && items.length) { loadIndex(0, true); return; }
      audio.play().then(function () {
        player.classList.add('is-playing');
        setIcon(true);
      }).catch(function () {});
    }
    function pause() {
      audio.pause();
      player.classList.remove('is-playing');
      setIcon(false);
    }
    function toggle() {
      if (audio.paused) play(); else pause();
    }
    function next() {
      if (!items.length) return;
      // 跳过 disabled 项
      var j = curIndex;
      for (var k = 0; k < items.length; k++) {
        j = (j + 1) % items.length;
        if (!items[j].classList.contains('is-disabled')) break;
      }
      loadIndex(j, true);
    }
    function prev() {
      if (!items.length) return;
      // 当前曲目 > 3s 视为"回到本曲开头"，否则才切上一首
      if (audio.currentTime > 3) { audio.currentTime = 0; return; }
      var j = curIndex;
      for (var k = 0; k < items.length; k++) {
        j = (j - 1 + items.length) % items.length;
        if (!items[j].classList.contains('is-disabled')) break;
      }
      loadIndex(j, true);
    }

    // ---------- 事件绑定 ----------
    items.forEach(function (el, i) {
      el.addEventListener('click', function () {
        // 没有 src 的示例项 → 不响应
        if (el.classList.contains('is-disabled')) return;
        // 点击当前曲目 → 切换 播放/暂停
        if (i === curIndex) { toggle(); return; }
        loadIndex(i, true);
      });
    });

    btnPrev.addEventListener('click', prev);
    btnNext.addEventListener('click', next);
    btnTog.addEventListener('click', toggle);
    btnCls.addEventListener('click', function (e) {
      e.preventDefault();
      hidePlayer();
      clearPos();
    });

    prog.addEventListener('input', function () {
      if (!isFinite(audio.duration)) return;
      audio.currentTime = (prog.value / 1000) * audio.duration;
      setProgressUI();
    });

    audio.addEventListener('timeupdate', function () { setProgressUI(); savePos(); });
    audio.addEventListener('ended', next);
    audio.addEventListener('play',  function () { player.classList.add('is-playing'); setIcon(true); });
    audio.addEventListener('pause', function () { player.classList.remove('is-playing'); setIcon(false); });
    audio.addEventListener('error', function () {
      // 区分真错误 vs 用户主动 abort
      // - code=1 (MEDIA_ERR_ABORTED)：用户切歌/暂停触发的取消请求，不是真错误 → 静默
      // - code=2/3/4：网络/解码/格式问题 → 跳过到下一首
      var code = audio.error && audio.error.code;
      if (code === 1) return;          // 用户主动 abort，忽略
      console.warn('[music-player] audio load error (code=' + code + '), skipping to next');
      next();
    });

    // 键盘快捷键（仅当 music-list 区域 focus 时生效）
    document.addEventListener('keydown', function (e) {
      // 编辑控件里输入时不触发
      var t = e.target;
      if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable)) return;
      if (e.code === 'Space')  { e.preventDefault(); toggle(); }
      else if (e.key === 'ArrowRight' && e.shiftKey) { e.preventDefault(); next(); }
      else if (e.key === 'ArrowLeft'  && e.shiftKey) { e.preventDefault(); prev(); }
    });

    // ---------- 记忆播放位置（localStorage） ----------
    var STORAGE_KEY = 'lyrumu:music-player:state-v1';
    function savePos() {
      if (!audio.src) return;
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({
          index: curIndex,
          time:  audio.currentTime,
          src:   audio.src
        }));
      } catch (e) {}
    }
    function clearPos() { try { localStorage.removeItem(STORAGE_KEY); } catch (e) {} }
    function restorePos() {
      try {
        var raw = localStorage.getItem(STORAGE_KEY);
        if (!raw) return false;
        var s = JSON.parse(raw);
        // 根据 src 找回 index（避免 playlist 顺序改变时错位）
        var idx = items.findIndex(function (el) { return el.dataset.src === s.src; });
        if (idx < 0) return false;
        loadIndex(idx, false);
        if (isFinite(s.time)) audio.currentTime = s.time;
        setProgressUI();
        return true;
      } catch (e) { return false; }
    }
    // 延迟 restore：等 DOM / audio metadata 都就位
    setTimeout(restorePos, 80);
  });
})();