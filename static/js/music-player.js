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

  function normSrc(src) {
    if (!src) return '';
    try { return new URL(src, window.location.href).pathname; }
    catch (e) { return src; }
  }

  // ---------- 播放模式定义 ----------
  var MODES = ['list', 'one', 'shuffle']; // 列表循环 / 单曲循环 / 随机播放
  var MODE_ICONS = {
    list:    '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/></svg>',
    one:     '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/><text x="12" y="14" font-size="8" font-weight="600" fill="currentColor" stroke="none" text-anchor="middle" dominant-baseline="middle" font-family="sans-serif">1</text></svg>',
    shuffle: '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 18h1.4c1.3 0 2.5-.6 3.3-1.7l6.1-8.6c.7-1.1 2-1.7 3.3-1.7H22"/><path d="m18 2 4 4-4 4"/><path d="M2 6h1.9c1.5 0 2.9.9 3.6 2.2"/><path d="M22 18h-5.9c-1.3 0-2.6-.7-3.3-1.8l-.5-.8"/><path d="m18 14 4 4-4 4"/></svg>'
  };
  var MODE_TITLES = {
    list:    'Loop All',
    one:     'Loop One',
    shuffle: 'Shuffle'
  };

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
    // 页面控制栏（播放模式和音量）
    var btnMode = $('#music-mode-btn');
    var modeLabel = $('#music-mode-label');
    var btnMute = $('#music-mute-btn');
    var volSlider = $('#music-volume-slider');
    var volLabel = $('#music-volume-value');
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

    // ---------- 音量控制 ----------
    var VOL_KEY = 'lyrumu:music-player:volume-v1';
    var lastVol = parseFloat(localStorage.getItem(VOL_KEY)) || 0.8;
    var isMuted = false;
    var prevVol = lastVol;

    function setVolume(v) {
      v = Math.max(0, Math.min(1, v));
      audio.volume = v;
      lastVol = v;
      var pct = Math.round(v * 100);
      volSlider.value = pct;
      volSlider.style.setProperty('--vol', pct + '%');
      if (volLabel) volLabel.textContent = pct + '%';
      try { localStorage.setItem(VOL_KEY, v); } catch(e) {}
      isMuted = false;
      updateVolumeIcon();
    }

    function updateVolumeIcon() {
      var vol = isMuted ? 0 : lastVol;
      var icon15 = '<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">';
      var icon;
      if (vol === 0 || vol === '0') {
        icon = icon15 + '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><line x1="22" y1="9" x2="16" y2="15"/><line x1="16" y1="9" x2="22" y2="15"/></svg>';
      } else if (vol < 0.5) {
        icon = icon15 + '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>';
      } else {
        icon = icon15 + '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>';
      }
      btnMute.innerHTML = icon;
      if (volLabel) volLabel.textContent = Math.round(vol * 100) + '%';
    }

    volSlider.addEventListener('input', function () {
      setVolume(parseInt(volSlider.value) / 100);
    });

    btnMute.addEventListener('click', function () {
      if (isMuted) {
        setVolume(prevVol || 0.8);
      } else {
        prevVol = lastVol;
        isMuted = true;
        audio.volume = 0;
        volSlider.value = 0;
        updateVolumeIcon();
      }
    });

    // 初始化音量
    audio.volume = lastVol;
    volSlider.value = Math.round(lastVol * 100);
    volSlider.style.setProperty('--vol', Math.round(lastVol * 100) + '%');
    updateVolumeIcon();

    // ---------- 播放模式 ----------
    var MODE_KEY = 'lyrumu:music-player:mode-v1';
    var curMode = localStorage.getItem(MODE_KEY) || 'list';
    var shuffleOrder = []; // 随机播放时的顺序
    var shufflePos = 0;

    function shuffleGenerate() {
      // Fisher-Yates 洗牌
      var arr = [];
      items.forEach(function (el, i) {
        if (!el.classList.contains('is-disabled')) arr.push(i);
      });
      for (var i = arr.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
      }
      return arr;
    }

    function updateModeUI() {
      btnMode.innerHTML = MODE_ICONS[curMode];
      btnMode.setAttribute('title', MODE_TITLES[curMode]);
      btnMode.setAttribute('aria-label', '播放模式: ' + MODE_TITLES[curMode]);
      btnMode.classList.toggle('is-active', curMode !== 'list');
      if (modeLabel) modeLabel.textContent = MODE_TITLES[curMode];
    }

    btnMode.addEventListener('click', function () {
      var idx = MODES.indexOf(curMode);
      curMode = MODES[(idx + 1) % MODES.length];
      try { localStorage.setItem(MODE_KEY, curMode); } catch(e) {}
      if (curMode === 'shuffle') {
        shuffleOrder = shuffleGenerate();
        // 如果当前曲目在 shuffle 顺序里，从它的位置继续
        var pos = shuffleOrder.indexOf(curIndex);
        shufflePos = pos >= 0 ? pos : 0;
      }
      updateModeUI();
    });

    // 初始化模式
    if (curMode === 'shuffle') {
      shuffleOrder = shuffleGenerate();
      shufflePos = 0;
    }
    updateModeUI();

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

    function getNextIndex() {
      if (curMode === 'shuffle') {
        // 随机模式：从 shuffle 顺序取下一首
        shufflePos = (shufflePos + 1) % shuffleOrder.length;
        return shuffleOrder[shufflePos];
      } else {
        // 列表循环 / 单曲循环
        var j = curIndex;
        for (var k = 0; k < items.length; k++) {
          j = (j + 1) % items.length;
          if (!items[j].classList.contains('is-disabled')) break;
        }
        return j;
      }
    }

    function getPrevIndex() {
      if (curMode === 'shuffle') {
        shufflePos = (shufflePos - 1 + shuffleOrder.length) % shuffleOrder.length;
        return shuffleOrder[shufflePos];
      } else {
        var j = curIndex;
        for (var k = 0; k < items.length; k++) {
          j = (j - 1 + items.length) % items.length;
          if (!items[j].classList.contains('is-disabled')) break;
        }
        return j;
      }
    }

    function next() {
      if (!items.length) return;
      loadIndex(getNextIndex(), true);
    }
    function prev() {
      if (!items.length) return;
      // 当前曲目 > 3s 视为"回到本曲开头"，否则才切上一首
      if (audio.currentTime > 3) { audio.currentTime = 0; return; }
      loadIndex(getPrevIndex(), true);
    }

    // ---------- 事件绑定 ----------
    items.forEach(function (el, i) {
      el.addEventListener('click', function (e) {
        if (e.target && e.target.closest('.music-item-download')) return;
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
    audio.addEventListener('ended', function () {
      if (curMode === 'one') {
        // 单曲循环：重播当前曲目
        audio.currentTime = 0;
        audio.play().catch(function () {});
      } else {
        next();
      }
    });
    audio.addEventListener('play',  function () {
      savePos();
      player.classList.add('is-playing'); setIcon(true);
    });
    audio.addEventListener('pause', function () {
      savePos();
      player.classList.remove('is-playing'); setIcon(false);
    });
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
          src:   audio.currentSrc || audio.src,
          playing: !audio.paused
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
        var savedSrc = normSrc(s.src);
        var idx = items.findIndex(function (el) { return normSrc(el.dataset.src) === savedSrc; });
        if (idx < 0) return false;
        loadIndex(idx, false);
        function applyRestore() {
          if (isFinite(s.time)) audio.currentTime = s.time;
          setProgressUI();
          if (s.playing) {
            audio.play().then(function () {
              player.classList.add('is-playing');
              setIcon(true);
              savePos();
            }).catch(function () {});
          }
        }
        if (audio.readyState >= 1) applyRestore();
        else {
          audio.addEventListener('loadedmetadata', function onceRestore() {
            audio.removeEventListener('loadedmetadata', onceRestore);
            applyRestore();
          });
        }
        return true;
      } catch (e) { return false; }
    }
    // 延迟 restore：等 DOM / audio metadata 都就位
    setTimeout(restorePos, 80);
  });
})();
