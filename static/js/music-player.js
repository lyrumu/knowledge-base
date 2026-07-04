/* =============================================================================
   music-player.js — 播放器入口
   ---------------------------------------------------------------------------
   只做依赖装配：拿到根节点 → 装配 store / view / storage / controller。
   业务逻辑在 controller.js，模板契约在 dom.js，持久化在 storage.js。
   入口：DOMContentLoaded；仅当页面同时存在 [data-music-playlist] 与 [data-music-player] 时激活。
   ============================================================================= */
(function () {
  'use strict';

  function init() {
    var MP = window.MusicPlayer;
    if (!MP || !MP.dom || !MP.store || !MP.view || !MP.storage || !MP.controller) {
      console.warn('[music-player] module not loaded');
      return;
    }

    var playlistRoot = document.querySelector('[data-music-playlist]');
    var playerRoot   = document.querySelector('[data-music-player]');
    if (!playlistRoot || !playerRoot) return;

    var dom = MP.dom.bind(playlistRoot, playerRoot);
    if (!dom) return;

    var initialMode = MP.storage.readMode();
    var store = MP.store.create(dom.items, { mode: initialMode });
    var view  = MP.view.create(dom);
    var controller = MP.controller.create({
      dom: dom,
      store: store,
      view: view,
      storage: MP.storage
    });

    controller.init();
    // 延迟 restore：让 audio metadata 先行
    setTimeout(function () { controller.restore(); }, 80);
  }

  // readyState 判断处理两种情况：
  //   - 脚本在 <head> 里加载（loading）→ 等 DOMContentLoaded
  //   - 脚本在 body 末尾（已 complete）→ 直接 init
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();