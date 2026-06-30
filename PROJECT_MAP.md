# 项目地图 — 个人网站 `f:\Notes\`

> 最后更新：2026-06-30 · Music 播放器新增播放模式（Loop All/One/Shuffle）与音量控制（位于页面列表上方）· Hugo v0.163.2 · Blowfish v2

---

## 1. 这是什么

一个基于 **本地 Obsidian Vault** 驱动的 **Hugo 静态站点**，部署在 **Cloudflare Pages**。
所有文章用 Obsidian 写 → 跑同步脚本 → `git push` → 自动部署上线。

---

## 2. 快速查阅：我想改什么 → 改哪个文件

| 我想…… | 改这个文件 |
|---------|-----------|
| 改封面的标题 / subtitle / avatar / 统计开关 / 顶栏 GitHub 链接 | [`data/cover.yaml`](file:///f:/Notes/data/cover.yaml) |
| 改首页三组精选内容 | [`data/home_highlights.yaml`](file:///f:/Notes/data/home_highlights.yaml)（Daily / Docs / Works 三组精选都在这里；现在只维护 `sections` 即可） |
| 改封面的颜色 | [`assets/css/_01_tokens.css`](file:///F:/Notes/assets/css/_01_tokens.css) 顶部 `:root` / `html.dark` 的 `--bg-base / --line / --accent`（首页颜色已不再单独存进 `cover.yaml`） |
| 改封面的字距 / 大小 / 花边位置 | [`assets/css/_08_cover.css`](file:///F:/Notes/assets/css/_08_cover.css) |
| 改内页"小封面"的文案 | 对应 `content/xxx/_index.md` 的 frontmatter `kicker / subtitle` |
| 改 /notes/ 入口展示方式（单列 / 3 列等）| `content/notes/_index.md` frontmatter `cardColumns`（1/2/3） |
| 改 `notes` 文章的 taxonomy / Edit Link / 上一篇下一篇规则 | [`content/notes/_index.md`](file:///f:/Notes/content/notes/_index.md) 的 `cascade`（只对 `notes` 下文章生效） |
| 改 `notes` 文章里 tags / categories / series 的维护规范 | [`BLOWFISH_FEATURE_AUDIT.md`](file:///f:/Notes/BLOWFISH_FEATURE_AUDIT.md) 末尾的 `Taxonomies 后续维护约定` |
| 微调上一篇 / 下一篇的视觉样式 | [`layouts/partials/article-pagination.html`](file:///f:/Notes/layouts/partials/article-pagination.html) + [`assets/css/_02_chrome.css`](file:///f:/Notes/assets/css/_02_chrome.css) |
| 改网站存在时间 / 静态统计摘要的起点日期 | [`data/site.yaml`](file:///f:/Notes/data/site.yaml) 的 `launch_date` |
| 改站点统计里显示哪些数字 | [`layouts/partials/site-stats.html`](file:///f:/Notes/layouts/partials/site-stats.html) |
| 换 /life/ 的子模块卡 | [`data/life.yaml`](file:///f:/Notes/data/life.yaml)（加图片 / 读书 / 旅行…都改这里） |
| 换 /life/music/ 的歌单 | [`data/music.yaml`](file:///f:/Notes/data/music.yaml)（加一首填一个 `- title/artist/cover/src/duration/size/...` 条目） |
| 换 /life/music/ 的封面/SVG 动画 | [`assets/css/_05_cards.css`](file:///F:/Notes/assets/css/_05_cards.css) 的 `.life-sub-cover-*` 规则 |
| 换 /works/ 的子模块卡 | [`data/works.yaml`](file:///f:/Notes/data/works.yaml)（projects / resources / tools…） |
| 换 /works/projects/ 的项目卡 | [`data/projects.yaml`](file:///f:/Notes/data/projects.yaml)（加一条填 `- name/title/desc/cover/href/repo/tags/date/featured`） |
| 换 /works/resources/ 的资源卡 | [`data/resources.yaml`](file:///f:/Notes/data/resources.yaml)（加一条填 `- name/title/desc/cover/file/format/size/tags/date/source`） |
| 改 /works/projects/ 的 3D 倾斜角度 | [`assets/css/_06_works-cards.css`](file:///F:/Notes/assets/css/_06_works-cards.css) 的 `.project-card` 或 shortcode 里的 `data-tilt-*` |
| 加一个 Lucide icon | [`layouts/partials/cover/icon.html`](file:///f:/Notes/layouts/partials/cover/icon.html) 加 `else if` 分支 |
| 改 /about/ 个人内容块（Now / Focus / Path） | [`content/about/_index.md`](file:///f:/Notes/content/about/_index.md) |
| 改 /about/ 联系方式图标 / 邮箱 | [`content/about/_index.md`](file:///f:/Notes/content/about/_index.md) + [`layouts/partials/about-contact.html`](file:///f:/Notes/layouts/partials/about-contact.html)（base64 邮箱解码 + Toast） |
| 改全站分隔符规则 | [`assets/css/_03_prose.css`](file:///f:/Notes/assets/css/_03_prose.css) + [`assets/css/_05_cards.css`](file:///f:/Notes/assets/css/_05_cards.css) + [`assets/css/_04_hero.css`](file:///f:/Notes/assets/css/_04_hero.css) + [`assets/css/_08_cover.css`](file:///f:/Notes/assets/css/_08_cover.css) |
| 改 /about/ 图标玻璃效果 | [`assets/css/_09_about.css`](file:///F:/Notes/assets/css/_09_about.css)（`.about-contact-glass` / `.about-contact-btn` / `.copy-toast`） |
| 调首页 / about 首屏图片预加载 | [`layouts/partials/head.html`](file:///f:/Notes/layouts/partials/head.html)（按页面条件 preload 关键图片和字体） |
| 改顶栏的菜单项 | [`hugo.toml`](file:///f:/Notes/hugo.toml) 的 `[[menu.main]]` 段 |
| 改 Umami 统计配置 | [`hugo.toml`](file:///f:/Notes/hugo.toml) 的 `[params.umamiAnalytics]` |
| 以后要启用 Blowfish 原生阅读数 / 点赞 | [`hugo.toml`](file:///f:/Notes/hugo.toml) 的 `showViews / showLikes` + `[firebase]`（原生方案推荐 Firebase） |
| 看 Firebase 安全规则怎么配 | [`FIREBASE_SECURITY.md`](file:///f:/Notes/FIREBASE_SECURITY.md) |
| 加一篇新文章 | 见下方 §4 |
| 写 CSS（字体 / 颜色 / 间距） | 见下方 §3 · 选对模块文件 |
| 改文章内容样式 | [`assets/css/_03_prose.css`](file:///F:/Notes/assets/css/_03_prose.css) |
| 改"亮色" / "暗色" 主题的 CSS | [`assets/css/_01_tokens.css`](file:///F:/Notes/assets/css/_01_tokens.css) 顶部 `:root`（亮）和 `html.dark`（暗）— **v3 后是唯一调色数据源**，改一处全局生效（封面 + 卡片 + blowfish utility 全部跟着变） |
| 部署 / 更新站点 | 见 [`DEPLOY.md`](file:///f:/Notes/DEPLOY.md) |

---



## 3. 文件结构总览

```
f:\Notes\
├── hugo.toml                       # 全局 Hugo 配置
├── DEPLOY.md                       # 部署与维护指南
├── BLOWFISH_FEATURE_AUDIT.md       # Blowfish / Hugo 原生能力审计与 taxonomy 维护约定
├── FIREBASE_SECURITY.md            # Firebase views / likes 的安全配置说明
├── data/site.yaml                  # 站点级元数据（当前用于 site-stats 的 launch_date）
├── PROJECT_MAP.md                  # ← 你正在看（本地保留）
│
├── assets/
│   ├── css/
│   │   ├── custom.css              # 文档索引（不再被加载，仅记录文件清单 + 加新文件 SOP）
│   │   ├── custom.css.bak.v1       # 历史备份（v1 版本，已不再使用）
│   │   ├── custom.css.bak.v2       # 历史备份（v2 = 拆分前的 3514 行原文件，紧急回滚用）
│   │   ├── _01_tokens.css          # ★ @font-face + CSS 变量 (light/dark) + html/body 基线
│   │   ├── _02_chrome.css          # ★ footer / 主菜单 / scroll-to-top / 分页 / TOC
│   │   ├── _03_prose.css           # ★ 长文章 .prose + reveal 滚动入场
│   │   ├── _04_hero.css            # ★ 内页 page-hero + 面包屑 + single 页头
│   │   ├── _05_cards.css           # ★ module / vault / article-link / life / music-list / works-sub / file-tree / section-rule
│   │   ├── _06_works-cards.css     # ★ projects (3D 倾斜) + resources (瀑布流)
│   │   ├── _07_music-player.css    # ★ 全局音乐播放器 + copy-toast
│   │   ├── _08_cover.css           # ★ 首页封面（真 header + masthead + highlights + 花边）
│   │   └── _09_about.css           # ★ About 页（profile + Now/Focus/Path + 标签 + 液态玻璃联系方式）
│   └── icons/                      # Simple Icons 品牌色 SVG（github/gmail/qq 等联系方式图标）
│
├── archetypes/
│   └── default.md                  # `hugo new` 模板
│
├── content/                        # ★ 所有页面内容
│   ├（待整理）
│   ├── notes/                      # /notes/ 文章入口（layout:list + list.html 卡片列表）
│   │   └── _index.md               # notes 入口页（正文 + 自动文章列表 + cascade 控制后代文章的 taxonomy/edit/pagination）
│   ├── works/                      # /works/ 相关（作品 / 资源 / 工具）
│   │   ├── _index.md               # 入口（works-grid 短代码）
│   │   ├── projects/_index.md      # 项目子页（projects-list 短代码 + 3D 倾斜）
│   │   ├── resources/_index.md     # 资源子页（resources-list 短代码 + 瀑布流）
│   │   └── tools/_index.md         # 工具子页（占位 + 计划收录）
│   ├── life/                       # /life/ 生活（可扩展子模块网格）
│   │   ├── _index.md               # 子模块入口（life-grid 短代码）
│   │   └── music/_index.md         # /life/music/ 子页
│   └── about/_index.md             # /about/ 关于（avatar + Now/Focus/Path + 联系方式 + 技术栈 + GitHub 热力图）
│
├── data/                           # ★ 数据驱动（改这里就能改 UI）
│   ├── cover.yaml                  # 首页 masthead 基础信息 / avatar / show_stats / 顶栏 GitHub repo_url
│   ├── home_highlights.yaml        # 首页三组精选（Daily / Docs / Works）数据源；当前只维护 sections
│   ├── about_timeline.yaml         # ABOUT ME 的 Path so far 里程碑（文字 / 顺序 / 可选图片）
│   ├── start_here.yaml             # 旧版首页 Start Here 数据（当前首页已不再使用，保留作历史参考）
│   ├── vault.yaml                  # 旧版 /notes/ 分类卡数据（当前前台未使用，保留作历史参考）
│   ├── life.yaml                   # /life/ 子模块清单（music / 图片 / 读书…）
│   ├── music.yaml                  # /life/music/ 歌单
│   ├── site.yaml                   # 站点 launch_date（只填一次；site-stats 用它计算在线天数）
│   ├── works.yaml                  # /works/ 子模块清单（projects / resources / tools…）
│   ├── projects.yaml               # /works/projects/ 项目清单
│   └── resources.yaml              # /works/resources/ 资源清单
│
├── layouts/                        # ★ 自定义模板（覆写主题）
│   ├── _default/list.html          # section 主页 → page-hero + 正文 + 子页面列表（notes/about 当前走这里）
│   ├── home.json                   # home kind 的 JSON 输出（消 build WARN；内容同主题 _default/index.json）
│   ├── page.html                   # kind=page 的项目级模板；当前 notes 普通文章也命中这里，taxonomy/edit/pagination 需在此补回
│   ├── partials/
│   │   ├── head.html               # ⚠️ [lyrumu 改造] 覆盖 Blowfish 主题版本
│   │   │                           #  原因：CSS `@import` 在 Hugo Pipes 不展开（详见 §8 踩坑提醒）
│   │   │                           #  改为：resources.Match "css/_*.css" + Concat
│   │   ├── article-pagination.html  # 项目级覆写上一篇/下一篇结构（保留逻辑，只改样式挂钩）
│   │   ├── cover/icon.html         # Lucide SVG icon 字典
│   │   ├── cover/page-hero.html    # 内页"小封面" partial
│   │   ├── home/custom.html        # 封面 partial
│   │   ├── site-stats.html         # 站点统计 partial（供 shortcode 与封面共用；当前显示 notes / projects / music / days online / last updated）
│   │   ├── header/components/
│   │   │   ├── desktop-menu.html   # 加 GitHub 按钮
│   │   │   └── mobile-menu.html    # 加 GitHub 按钮
│   │   ├── extend-head.html        # 第三方库（Splitting.js + AOS.js + VanillaTilt.js）
│   │   ├── music-player.html       # 粘性音乐播放器（被 music-list 自动注入）
│   │   └── about-contact.html      # /about/ 联系方式图标卡 partial（被 about-contact shortcode 调）
│   └── shortcodes/
│       ├── page-hero.html          # {{< page-hero >}} 短代码
│       ├── vault-sections.html     # 旧版 /notes/ 分类网格（当前前台未使用）
│       ├── life-grid.html          # /life/ 子模块网格
│       ├── music-list.html         # /life/music/ 歌曲列表
│       ├── works-grid.html         # /works/ 子模块网格
│       ├── projects-list.html      # /works/projects/ 项目列表（3D 倾斜）
│       ├── resources-list.html     # /works/resources/ 资源列表（瀑布流）
│       ├── file-tree.html          # 可折叠文件树
│       ├── about-contact.html      # /about/ 联系方式图标卡（壳）
│       ├── site-stats.html         # 站点统计 shortcode 壳（实际渲染委托给 partial）
│       └── section-rule.html       # ✦ 分隔符
├── scripts/                        # ★ 运维脚本
│   └── vault-to-hugo.ps1           # Vault → Hugo 同步（日常使用）
│
├── static/                         # 静态资源
│   ├── fonts/                      # 字体文件（本地化）
│   ├── css/aos.css                 # ★ AOS.js 样式（2026-06-25 本地化，原 jsDelivr CDN）
│   ├── js/                         # ★ 第三方 JS + 项目级轻交互脚本
│   │   ├── aos.js                  # AOS.js 滚动入场
│   │   ├── splitting.min.js        # Splitting.js 字符分割
│   │   ├── vanilla-tilt.min.js     # VanillaTilt.js 3D 倾斜
│   │   ├── music-player.js         # 音乐播放器逻辑
│   │   └── site-stats-days.js      # 站点在线天数前端实时计算
│   ├── image/                      # 装饰 PNG（花边 / 花朵 / musicheart）
│   │   ├── life/music/             # /life/music/ 封面（用户自行放入）
│   │   └── works/                  # /works/ 子模块封面
│   │       ├── projects/           # /works/projects/ 项目封面（用户自行放入）
│   │       └── resources/          # /works/resources/ 资源封面（用户自行放入）
│   ├── life/music/                 # /life/music/ 音频文件（用户自行放入）
│   ├── works-resources/            # /works/resources/ 下载文件（用户自行放入）
│   └── notes-assets/               # 可下载资源（aipython, minecraft, tools）
│
├── themes/blowfish/                # 主题本体（一般不改）
│                                # ⚠️ 例外 1：layouts/_default/baseof.html
│                                # 加了 is-cover-page 类（[lyrumu 改造] 注释标记）
│                                # 升级主题时若被覆盖，按注释重新加这一段
│                                # ⚠️ 例外 2：layouts/partials/head.html
│                                # 被项目级 layouts/partials/head.html 覆盖（改 CSS 加载方式）
│                                # 升级主题时优先看 [lyrumu 改造] 段，对比后再决定
│
├── DONE.md                         # 开发日志
└── .trae/rules/个人网站开发规则.md   # 项目宪法
```

---

## 4. 部件对应速查

### 封面（`/_index.md`）

| 元素 | 数据源 | 模板 |
|------|--------|------|
| 封面排版 / 花边 / 上方 masthead | [`data/cover.yaml`](file:///f:/Notes/data/cover.yaml)（基础文案 / 头像 / 统计开关 / repo_url） | [`layouts/partials/home/custom.html`](file:///f:/Notes/layouts/partials/home/custom.html) |
| 封面 CSS（字体 / 调色 / 布局） | — | [`assets/css/_08_cover.css`](file:///F:/Notes/assets/css/_08_cover.css) |
| 封面主题切换 | — | 直接复用主题原生顶栏按钮；首页不再保留封面专属切换器 |
| 首页首屏关键图 / 字体预加载 | — | [`layouts/partials/head.html`](file:///f:/Notes/layouts/partials/head.html) |
| 封面装饰元素（上下流动花边 + 左右黑花） | — | 直接用 `static/image/` 下的 png |
| 封面调色（明 / 暗） | [`assets/css/_01_tokens.css`](file:///f:/Notes/assets/css/_01_tokens.css) 的全局变量 | [`custom.html`](file:///f:/Notes/layouts/partials/home/custom.html) 的 `<style>` 块只负责把全局变量派生到封面局部变量 |
| 首页 `Daily / Docs / Works Highlights` | [`data/home_highlights.yaml`](file:///f:/Notes/data/home_highlights.yaml) | 由 [`layouts/partials/home/custom.html`](file:///f:/Notes/layouts/partials/home/custom.html) 循环渲染；支持 section 级入口和 1-3 条手动精选 |

**以后如何更新首页 Highlights：**

1. **改分组文案**
   - 直接改 [`data/home_highlights.yaml`](file:///f:/Notes/data/home_highlights.yaml) 各组里的 `kicker / title / desc / cta_label / cta_path`

2. **改单条精选跳转**
   - 改对应条目的 `items[].path`
   - 站内页可直接写 `/notes/xxx/`、`/life/xxx/`、`/works/xxx/`
   - 外链也可直接写完整 `https://...`

3. **控制每组显示数量**
   - 每组 `items` 建议维护 1-3 条
   - 首页不会自动抓“最新内容”，而是严格按这个文件里手动挑选的顺序渲染

4. **模板职责**
   - [`layouts/partials/home/custom.html`](file:///f:/Notes/layouts/partials/home/custom.html) 现在只负责循环渲染和按 `path` 解析站内页 / 外链
   - 日常改字、改链接，优先不要再直接改模板

### 内页"小封面"（section 主页顶部）

| 元素 | 数据源 | 模板 |
|------|--------|------|
| kicker / subtitle / eyebrow | 各 `_index.md` frontmatter | [`layouts/partials/cover/page-hero.html`](file:///f:/Notes/layouts/partials/cover/page-hero.html) |
| 短代码调用 | — | [`layouts/shortcodes/page-hero.html`](file:///f:/Notes/layouts/shortcodes/page-hero.html) |
| CSS | — | [`assets/css/_04_hero.css`](file:///F:/Notes/assets/css/_04_hero.css) |

### /notes/ 文章入口页

| 元素 | 数据源 | 模板 |
|------|--------|------|
| notes 入口页正文 | [`content/notes/_index.md`](file:///f:/Notes/content/notes/_index.md) | [`layouts/_default/list.html`](file:///f:/Notes/layouts/_default/list.html) |
| 文章卡列表 | `content/notes/**` 下的文章 | [`layouts/_default/list.html`](file:///f:/Notes/layouts/_default/list.html) + `article-link/card.html` |
| 列数控制 | `content/notes/_index.md` frontmatter `cardColumns` | [`layouts/_default/list.html`](file:///f:/Notes/layouts/_default/list.html) |
| 后代文章的 `taxonomy / Edit Link / 上一篇下一篇` 默认规则 | [`content/notes/_index.md`](file:///f:/Notes/content/notes/_index.md) 的 `cascade` | [`layouts/page.html`](file:///f:/Notes/layouts/page.html) + `article-meta/basic.html` + `article-pagination.html` |

**说明：**

- 当前前台的 `/notes/` 已不再使用 `data/vault.yaml + vault-sections.html` 这条旧链路
- `vault.yaml` / `vault-sections.html` 目前保留在仓库里，主要用于历史参考；若以后确认不再回退，可再统一清理
- `notes` 的 taxonomy / Edit Link / 上一篇下一篇不靠全局配置硬开，而是通过 `content/notes/_index.md` 的 `cascade` 只作用到 `notes` 后代文章
- 后续维护 tags / categories / series 的约定见 [`BLOWFISH_FEATURE_AUDIT.md`](file:///f:/Notes/BLOWFISH_FEATURE_AUDIT.md) 末尾 `Taxonomies 后续维护约定`

### /life/ 子模块网格

| 元素 | 数据源 | 模板 |
|------|--------|------|
| 子模块卡列表（music / 图片 / 读书…） | [`data/life.yaml`](file:///f:/Notes/data/life.yaml) | [`layouts/shortcodes/life-grid.html`](file:///f:/Notes/layouts/shortcodes/life-grid.html) |
| 封面 hover 动画（PNG 旋转 / SVG 呼吸 / emoji 翻转） | — | [`assets/css/_05_cards.css`](file:///F:/Notes/assets/css/_05_cards.css) 的 `.life-sub-cover-*` |
| 加新子模块 | 在 `data/life.yaml` 加一条 + 在 `content/life/<id>/_index.md` 建子页 | — |

### /life/music/ 歌曲列表 + 粘性播放器

| 元素 | 数据源 | 模板 |
|------|--------|------|
| 歌曲列表 | [`data/music.yaml`](file:///f:/Notes/data/music.yaml) | [`layouts/shortcodes/music-list.html`](file:///f:/Notes/layouts/shortcodes/music-list.html) |
| 播放模式/音量控制栏 | — | [`layouts/shortcodes/music-list.html`](file:///f:/Notes/layouts/shortcodes/music-list.html) 的 `.music-controls-bar` |
| 粘性播放器 HTML | — | [`layouts/partials/music-player.html`](file:///f:/Notes/layouts/partials/music-player.html) |
| 播放器逻辑（点击切歌 / 进度跳转 / 记忆位置 / 键盘 / 关闭清状态 / 播放模式 / 音量） | — | [`static/js/music-player.js`](file:///f:/Notes/static/js/music-player.js) |
| 歌曲下载入口 + 文件信息 | `data/music.yaml` 的 `src / size` | [`layouts/shortcodes/music-list.html`](file:///f:/Notes/layouts/shortcodes/music-list.html) + [`assets/css/_05_cards.css`](file:///F:/Notes/assets/css/_05_cards.css) |
| 列表样式 + 控制栏样式 + 播放器样式 | — | [`assets/css/_05_cards.css`](file:///F:/Notes/assets/css/_05_cards.css) 的 `.music-item*` + `.music-controls-bar` + [`_07_music-player.css`](file:///F:/Notes/assets/css/_07_music-player.css) 的 `.music-player` |
| 资源存放约定 | `static/life/music/<slug>.mp3` + `static/image/life/music/<slug>.jpg` | — |

### /about/ 页面内容

| 元素 | 数据源 | 模板 |
|------|--------|------|
| 头像 + 个人信息 + 联系方式的整体排版 | [`content/about/_index.md`](file:///f:/Notes/content/about/_index.md) | markdown（`.about-profile` 容器 + `{{< about-contact >}}` 短代码） |
| `Technical stack` 下方的 `Current focus / Path so far` | [`content/about/_index.md`](file:///f:/Notes/content/about/_index.md) + [`data/about_timeline.yaml`](file:///f:/Notes/data/about_timeline.yaml) | markdown + data + [`layouts/shortcodes/about-timeline.html`](file:///f:/Notes/layouts/shortcodes/about-timeline.html) + [`assets/css/_09_about.css`](file:///F:/Notes/assets/css/_09_about.css) 的 `.about-focus-* / .about-timeline-group-* / .about-milestone-* / .about-timeline-*` |
| about 首屏头像 / 字体预加载 | — | [`layouts/partials/head.html`](file:///f:/Notes/layouts/partials/head.html) |
| 联系方式短代码壳 | — | [`layouts/shortcodes/about-contact.html`](file:///f:/Notes/layouts/shortcodes/about-contact.html)（仅调 partial） |
| 联系方式 partial：3 个图标按钮 + base64 邮箱 + Toast + 解码 JS | 邮箱 base64 直接硬编码在 partial 里 | [`layouts/partials/about-contact.html`](file:///f:/Notes/layouts/partials/about-contact.html) |
| 邮箱按钮图标（GitHub / Gmail / QQ） | — | [`assets/icons/github.svg`](file:///f:/Notes/assets/icons/github.svg) / [gmail.svg](file:///f:/Notes/assets/icons/gmail.svg) / [qq.svg](file:///f:/Notes/assets/icons/qq.svg)（Simple Icons 品牌色填充） |
| 液态玻璃效果 + 应用图标按钮 + 顶部 Toast | — | [`assets/css/_09_about.css`](file:///F:/Notes/assets/css/_09_about.css) |

**点击行为**：

| 按钮 | 跳转目标 | 额外动作 |
|------|---------|---------|
| GitHub | `https://github.com/lyrumu` | 新标签页打开 |
| Gmail | `https://mail.google.com/mail/?view=cm&fs=1&to=llyrumu@gmail.com`（URL 预填收件人） | 新标签页打开 |
| QQ Mail | `https://mail.qq.com`（QQ 已下线 cgi-bin/write 接口） | 新标签页打开 + 邮箱写入剪贴板 + 顶部 Toast 提示 |

**邮箱 base64 防爬**：HTML 中只有 `data-contact-b64="bGx5cnVtdUBnbWFpbC5jb20="`，JS 用 `atob` 解码后写入 `href`。无 JS 时降级到 `<noscript>` 块明文邮箱 + 跳转链接。

**加新联系方式**（如 Twitter / Bilibili）：

1. 从 `https://cdn.simpleicons.org/<name>` 下载 SVG → [`assets/icons/`](file:///f:/Notes/assets/icons/)
2. [`layouts/partials/about-contact.html`](file:///f:/Notes/layouts/partials/about-contact.html) 复制一个 `<a>` 块，改类名 + `href` + 调 `{{< icon >}}`
3. 邮箱类按钮还需要加 `data-contact-b64` + `data-contact-platform`，并在 JS 里加平台 URL 拼装分支

**调整 about 新增内容块**：

1. `Current focus` 和 `Path so far` 现在统一放在 `Technical stack` 下方，中间用 `{{< section-rule >}}` 分隔
2. `Path so far` 的正文现在不直接写在 markdown 或 shortcode 里，而是通过 [`data/about_timeline.yaml`](file:///f:/Notes/data/about_timeline.yaml) 提供内容，由 [`layouts/shortcodes/about-timeline.html`](file:///f:/Notes/layouts/shortcodes/about-timeline.html) 输出
3. `about_timeline.yaml` 现在支持 `groups`：每组都有自己的 `title / meta / default_open / items`
4. 每组内部的里程碑顺序按对应 `items` 顺序维护；当前约定仍是倒叙：最新阶段放最上面，最早阶段放最下面
5. 如果以后想给某个里程碑加左图：
   - 在对应条目里补 `image` 和 `image_alt`
   - 可选补 `image_caption`
   - 不填这些字段时，会自动保持纯文字卡片
   - 当前图片规则是“原比例优先 + 统一最大尺寸范围”：不会强制裁成同一比例，但会等比缩放到相近的视觉大小

### 全站分隔符规则

| 类型 | 来源 | 当前规则 |
|------|------|----------|
| 正文里的 `---` | markdown `hr` | 统一走 [`_03_prose.css`](file:///f:/Notes/assets/css/_03_prose.css) 的“横线 + ✦ + 横线”样式 |
| `{{< section-rule >}}` | [`layouts/shortcodes/section-rule.html`](file:///f:/Notes/layouts/shortcodes/section-rule.html) | 作为显式插入的块级分隔符，外观与正文 `hr`、hero divider 对齐 |
| 首页 / 内页 hero 分隔符 | [`custom.html`](file:///f:/Notes/layouts/partials/home/custom.html) / [`page-hero.html`](file:///f:/Notes/layouts/partials/cover/page-hero.html) | 基础视觉样式由 [`_05_cards.css`](file:///f:/Notes/assets/css/_05_cards.css) 统一，页面文件只保留位置和宽度差异 |

**维护规则：**

1. 全站只保留一种块级分隔语言：`横线 + ✦ + 横线`
2. 如果已经写了 `{{< section-rule >}}`，就不要在它前后再紧跟 `---`
3. [`_03_prose.css`](file:///f:/Notes/assets/css/_03_prose.css) 里有相邻分隔符去重规则：`section-rule + hr`、`hr + section-rule`、`section-rule + section-rule`、`hr + hr` 会自动隐藏后一个
4. `h2` 默认带顶部细线；但如果它前面紧挨着 `section-rule` 或 `hr`，[`_03_prose.css`](file:///f:/Notes/assets/css/_03_prose.css) 会自动取消这条线，避免看起来像“分隔符后又跟一条默认横线”
5. 想插一个显式分隔时，优先用 `{{< section-rule >}}`；`---` 更适合普通文章正文里的语义分段

**写作约定（最常用）**

- 正文里想分段：直接写 `---`
- 想插一个更明确的块级分隔：用 `{{< section-rule >}}`
- 不要把 `---` 和 `{{< section-rule >}}` 紧挨着写
- 如果分隔符后面马上是 `##`，系统会自动去掉标题自带的顶部细线，不需要手动处理

### 顶栏

| 元素 | 数据源 | 模板 |
|------|--------|------|
| 菜单项 | `hugo.toml` → `[[menu.main]]` | 主题默认 |
| GitHub 按钮 | `data/cover.yaml` → `repo_url` | [`desktop-menu.html`](file:///f:/Notes/layouts/partials/header/components/desktop-menu.html) / [mobile-menu.html](file:///f:/Notes/layouts/partials/header/components/mobile-menu.html) |

### /works/ 子模块网格

| 元素 | 数据源 | 模板 |
|------|--------|------|
| 子模块卡列表（projects / resources / tools…） | [`data/works.yaml`](file:///f:/Notes/data/works.yaml) | [`layouts/shortcodes/works-grid.html`](file:///f:/Notes/layouts/shortcodes/works-grid.html) |
| 视觉 | **与 about/ 主入口的 module-card 同源**（完全复用 `_05_cards.css` 的 `.module-card` 样式） | — |
| 独有元素 | `works-sub-tags`（标签列表）/ `works-sub-draft-badge`（准备中徽章） | [`assets/css/_05_cards.css`](file:///F:/Notes/assets/css/_05_cards.css) |
| icon | `works.yaml` → `icon` | 走 `cover/icon.html` 解释为 Lucide SVG |
| 加新子模块 | 在 `data/works.yaml` 加一条 + 在 `content/works/<id>/_index.md` 建子页 | — |

### /works/projects/ 项目列表

| 元素 | 数据源 | 模板 |
|------|--------|------|
| 项目卡列表 | [`data/projects.yaml`](file:///f:/Notes/data/projects.yaml) | [`layouts/shortcodes/projects-list.html`](file:///f:/Notes/layouts/shortcodes/projects-list.html) |
| 3D 倾斜 + 鼠标反光 | shortcode 里的 `data-tilt*` 属性（VanillaTilt.js） | [`assets/css/_06_works-cards.css`](file:///F:/Notes/assets/css/_06_works-cards.css) 的 `.project-card` + `.project-card::after`（含 `mix-blend-mode: multiply` 防反光洗文字）|
| hover 揭示（tags + actions） | — | [`_06_works-cards.css`](file:///F:/Notes/assets/css/_06_works-cards.css) 的 `.project-card:hover .project-card-tags` 等 |
| 项目按钮（在线 / 源码） | `href` / `repo` 字段 | [`_06_works-cards.css`](file:///F:/Notes/assets/css/_06_works-cards.css) 的 `.project-card-btn`（**v3 修复后是独立 `<a>`**，各自跳对应地址；默认 + hover 对比度均 ≥ AA 4.5:1）|
| 入场淡入 | `data-aos="fade-up"`（应用到 `.project-card-cover` + `.project-card-body`，避开外层 VanillaTilt 的 transform 冲突） | [extend-head.html](file:///f:/Notes/layouts/partials/extend-head.html)（AOS.js） |
| 资源存放约定 | `static/image/works/projects/<slug>.png` | — |

### /works/resources/ 资源列表

| 元素 | 数据源 | 模板 |
|------|--------|------|
| 资源卡列表 | [`data/resources.yaml`](file:///f:/Notes/data/resources.yaml) | [`layouts/shortcodes/resources-list.html`](file:///f:/Notes/layouts/shortcodes/resources-list.html) |
| 瀑布流（CSS columns） | — | [`assets/css/_06_works-cards.css`](file:///F:/Notes/assets/css/_06_works-cards.css) 的 `.resources-masonry` |
| 格式徽章 / 元信息 / 下载按钮 | `resources.yaml` → `format / size / date / file` | [`_06_works-cards.css`](file:///F:/Notes/assets/css/_06_works-cards.css) 的 `.resource-card-*` |
| 入场淡入 | `data-aos="fade-up"`（应用到 `.resource-card`） | extend-head.html（AOS.js） |
| 资源存放约定 | `static/works-resources/<file>` + `static/image/works/resources/<slug>.png` | — |

### 第三方动画库（works 用）

| 库 | 版本 | 用途 | 初始化 |
|---|---|---|---|
| AOS.js + aos.css | 2.3.4 | 滚动入场淡入 | `extend-head.html` 的 `window.load` 回调里 `AOS.init()`，prefers-reduced-motion 时自动禁用 |
| VanillaTilt.js | 1.8.1 | 项目卡 3D 鼠标倾斜 | `extend-head.html` 的 `window.load` 回调里，IntersectionObserver 延迟挂载 |
| AOS 与 VanillaTilt 冲突规避 | — | AOS 应用于卡片内部子元素，VanillaTilt 管外层 transform | — |
| AOS `transition` 接管 hover 修复 | — | `aos:in` 后 1s 清除 inline transition | extend-head.html |

---

## 5. 调试 / 部署

| 事项 | 说明 |
|------|------|
| 本地预览 | `hugo server --themesDir themes --theme blowfish --config hugo.toml --bind 127.0.0.1 --port 1313` |
| 生产构建 | `hugo --minify --themesDir themes --theme blowfish --config hugo.toml` |
| vault 同步 | `powershell -File scripts/vault-to-hugo.ps1` 或加 `-Watch` 持续监听 |
| 部署到 Cloudflare Pages | 详见 [DEPLOY.md](file:///f:/Notes/DEPLOY.md) |
| 已知警告（Hugo + Blowfish 不兼容） | 正常，可忽略；详见 `.trae/rules/个人网站开发规则.md` |

---

## 6. 常见修改路径

### 换字体

1. 下载字体文件 → 丢进 `static/fonts/`
2. [`assets/css/_01_tokens.css`](file:///F:/Notes/assets/css/_01_tokens.css) 顶部的 `@font-face` 块里加一行
3. 想改正文就改 `--font-sans`，想改标题就改 `--font-serif`

### 换颜色主题（v3 统一调色板）

**所有颜色（封面 + 卡片 + blowfish utility）都通过 `:root` / `html.dark` 两个变量块驱动**，改一处即可全局生效。

1. 亮色：改 [`assets/css/_01_tokens.css`](file:///F:/Notes/assets/css/_01_tokens.css) 顶部 `:root` 的 7 个核心变量：
   - `--bg-base`（页面背景）/ `--bg-deep`（更深容器）/ `--line`（边框）
   - `--fg-base`（正文文字）/ `--fg-mute`（次要文字）/ `--fg-soft`（弱文字）
   - `--accent`（强调色 / 链接 / 按钮）
2. 暗色：改同一文件 `html.dark` 块的同名变量（暗色值）
3. ~~封面调色~~：**不需要单独改**，`data/cover.yaml` 的 `palette` 字段保留作占位，实际渲染以 `var()` 派生为准

**派生链路**（自动生效，不用动）：

```
:root { --bg-base: #FAF9F5 }  ──→  封面背景 --pal-bg-from: var(--bg-base)
html.dark { --bg-base: #141413 }  ──→  卡片边框 border: 1px solid var(--line)
                                       blowfish bg-neutral-800 → rgb(20,20,19)
                                       全部一起变
```

**例外**（如果想完全脱离 princess）：
- `hugo.toml` 里 `colorScheme = 'blowfish'`（中性灰）→ 但亮主题所有 `text-primary-500` 等 utility 会变蓝
- `hugo.toml` 里 `colorScheme = 'congo'` / `'slate'` 等其他方案 → 各自风格不同，自行尝试

**调按钮颜色避坑指南**（projects 卡上的 `.project-card-btn` 是反面教材）：

| 陷阱 | 原因 | 修复 |
|---|---|---|
| 米白 `#FAF9F5` 在纯 accent `#D97757` 上看不清 | 对比度仅 3.08:1（差 AA 4.5:1）| background 用 `color-mix(accent 70%, fg-base 30%)` → 对比度 4.64:1 |
| hover 用 `color-mix(accent 80%, fg-base 20%)` | 对比度 4.06:1 仍差一点 AA | hover 用 `color-mix(accent 60%, fg-base 40%)` → 对比度 5.36:1 |
| 想"按钮变亮"让 hover 更显眼 | **方向反了**——亮化让对比度更低，文字更看不清 | 让 background **更深**而非更亮 |
| 浏览器默认 `<a>` 蓝色文字盖掉设的 color | `<a>` 特异性 (0,1,0)，默认浏览器样式 specificity 同级但位置优先 | 加 `:link/:visited` 状态选择器提高到 (0,2,0) |
| 浏览器默认 `<a>` 下划线 | user-agent stylesheet 默认 | 加 `text-decoration: none`（覆盖 hover/focus/active） |
| 重构把外层 `<a>` 移除后 z-index 保护丢了 | `.project-card-link` 旧版有 `z-index: 2`，外层移除后反光层蒙住按钮 | 按钮加 `position: relative; z-index: 2;` + 反光层加 `mix-blend-mode: multiply;`（双保险）|

### 加 Lucide icon

在 [`layouts/partials/cover/icon.html`](file:///f:/Notes/layouts/partials/cover/icon.html) 加一个分支：

```html
{{ else if eq $name "github" }}
<svg><!-- 这里的 Lucide SVG path --></svg>
```

然后在 yaml 的 `icon` 字段写 `github` 即可。

### 改页面的 section layout

所有 section 主页（/notes/ /works/ /life/ /about/）都走 [`layouts/_default/list.html`](file:///f:/Notes/layouts/_default/list.html)。每个页面的 `_index.md` 可以设自己的 `kicker` / `subtitle`。

**frontmatter 开关**（list.html 支持）：

| 参数 | 作用 | 默认 |
|---|---|---|
| `cardColumns` | 子页面卡片列数（1 = 单列 / 2 / 3） | 3 |
| `showChildList` | 是否显示子页面卡片网格 | true |
| `cardView` | 卡片视图 vs 简单列表 | true |
| `groupByYear` | 按年份分组 | false |
| `orderByWeight` | 按 weight 排序（false 则按日期） | true |

### 加 /notes/ 的文章

```bash
# 推荐：直接用 notes archetype 起稿
hugo new content/notes/<slug>/index.md
# 然后编辑生成的 index.md
# hugo server 验证，/notes/ 入口自动渲染（受 cardColumns 控制）
```

- 当前已提供 [`archetypes/notes.md`](file:///f:/Notes/archetypes/notes.md)
- 若该文章的图片/附件只服务它自己，后续可优先和 `index.md` 放在同目录，而不是继续堆进 `static/`

### 加 life 子模块（如「图片」）

1. 在 [`data/life.yaml`](file:///f:/Notes/data/life.yaml) 复制 music 条目往下加一段，改 `id / name / cover / href` 等
2. 新建 `content/life/<id>/_index.md`，正文按需写（套 page-hero / section-rule 即可）
3. 若新子页要自己的"列表 + 播放器"风格，按 `life/music/` 模式再写一个 shortcode + yaml 即可

### 加一首音乐

1. mp3 放进 `static/life/music/<slug>.mp3`（**注意：用英文 / 数字命名，不要有空格和中文**）
2. 封面放进 `static/image/life/music/<slug>.jpg`
3. 在 [`data/music.yaml`](file:///f:/Notes/data/music.yaml) 加一段：
   ```yaml
   - title: "歌名"
     artist: "歌手"
     album: "专辑"
     cover: "/image/life/music/<slug>.jpg"
     src:   "/life/music/<slug>.mp3"
     duration: "4:12"
     mood: "lofi"
     note: "一句话小记"
   ```
4. `hugo server` 刷新就能看到

---

## 7. “相关”模块添加内容操作指南

> 本节是「加新内容」的完整 SOP。日常参考够用；更长的示例 / 排错细节看上面的 §2 §4 §8。

### 添加新项目（/works/projects/）

1. **准备封面图**：放图到 `static/image/works/projects/<slug>.png`（推荐 16:9 比例）
2. **编辑 yaml**：在 [data/projects.yaml](file:///f:/Notes/data/projects.yaml) 加一条：

   ```yaml
   - name: "项目名"
     title: "English Subtitle"
     desc: "衬线斜体描述，1-2 行"
     cover: "/image/works/projects/<slug>.png"
     href: "https://demo.example.com"   # 可空（在线 demo）
     repo: "https://github.com/..."     # 可空（源码）
     tags: [tag1, tag2]                  # 技术栈标签
     date: "2025-11"                     # YYYY-MM
     featured: true                      # 加 FEATURED 角标（可选）
   ```

3. **保存后** `hugo server` 刷新即可

### 添加新资源（/works/resources/）

1. **准备资源文件**：放到 `static/works-resources/<file>.zip`（mp3 / PDF / 字体包…任意格式）
2. **准备封面图**：放到 `static/image/works/resources/<slug>.png`（推荐 16:10）
3. **编辑 yaml**：在 [data/resources.yaml](file:///f:/Notes/data/resources.yaml) 加一条：

   ```yaml
   - name: "资源名"
     title: "English Subtitle"
     desc: "衬线斜体描述"
     cover: "/image/works/resources/<slug>.png"
     file: "/works-resources/<file>.zip"   # 也可以是外链 https://...
     format: "ZIP"                          # 右上角徽章文本
     size: "12 MB"                          # 文件大小（手动写）
     tags: [fonts, typography]
     date: "2025-11"
     source: "https://original.com"         # 可选，原始来源/致谢
   ```

4. **保存后** `hugo server` 刷新即可

### 添加新子模块（如 /works/designs/）

1. 在 [data/works.yaml](file:///f:/Notes/data/works.yaml) 加一条：

   ```yaml
   - id: designs
     name: "设计"
     title: "Designs · Posters & UI"
     icon: "palette"                        # Lucide icon 名
     desc: "偶尔做的小海报和 UI mockup。"
     href: "/works/designs/"
     tags: [design]
   ```

2. 新建 `content/works/designs/_index.md`（参考 [content/works/projects/_index.md](file:///f:/Notes/content/works/projects/_index.md) 或 [content/works/resources/_index.md](file:///f:/Notes/content/works/resources/_index.md)）
3. 如果新子页有特定列表（如 designs 的画廊），参考 `music-list` / `projects-list` / `resources-list` 的模式写 shortcode + 数据文件
4. **不需要改菜单**：`hugo.toml` 的 `[[menu.main]]` 已经包含 `/works/`，新子页通过 `/works/` 入口可达

### 微调视觉

| 想调什么 | 改哪里 |
|---|---|
| 3D 倾斜角度 / 反光 / 缩放 | [layouts/shortcodes/projects-list.html](file:///f:/Notes/layouts/shortcodes/projects-list.html) 里的 `data-tilt-*` 属性 |
| AOS 入场动画时长 / 触发距离 | [layouts/partials/extend-head.html](file:///f:/Notes/layouts/partials/extend-head.html) 的 `AOS.init({...})` |
| 卡片整体间距 / 圆角 / 边框 | [assets/css/_06_works-cards.css](file:///F:/Notes/assets/css/_06_works-cards.css) (projects / resources 共用) |
| 瀑布流列数 | [`_06_works-cards.css`](file:///F:/Notes/assets/css/_06_works-cards.css) 的 `.resources-masonry { column-count: ... }` |
| 加新 Lucide icon | [layouts/partials/cover/icon.html](file:///f:/Notes/layouts/partials/cover/icon.html) 加 `else if` 分支 |

### 通用注意事项

- **资源命名**：用英文 / 数字（不要空格、中文、特殊字符）—— 避免 URL 编码问题
- **文件大小**：手动写明，不会自动算
- **date 格式**：`YYYY-MM`（如 `2026-05`）
- **空数据**：`resources` / `projects` 为空时短代码会显示空态文案（"还没有项目" / "资源还在路上"），不会报错
- **图片加载失败**：shortcode 用 `onerror` 兜底（封面图变淡显示），但建议还是补上正确路径
- **a11y**：用户开启 `prefers-reduced-motion` 时 AOS 自动禁用，但 3D 倾斜仍是 hover 触发（用户主动操作，合理）

---

## 8. CSS 模块化踩坑提醒 + 加新文件 SOP

### ⚠️ 踩坑提醒：CSS `@import` 在本项目不工作（最重要！）

**不要在 `custom.css` 里写 `@import url("_*.css")`** —— 这是新接手的人最容易踩的坑。

**原因**：Blowfish 主题的 [themes/blowfish/layouts/partials/head.html](file:///f:/Notes/themes/blowfish/layouts/partials/head.html) 用的是 `resources.Get "css/custom.css"` → 直接 append 到 cssResources，下游 `resources.Concat` 拼接原始字节流，**不会展开 CSS `@import`**。

**结果**：编译通过、bundle 正常生成，但浏览器收到 bundle 后去请求 `/_tokens.css` 等 → 全 404 → 自定义样式全没（封面 `is-cover-page` 失效、princess 紫调出现、卡片布局错乱）。

**当前方案**：项目级 [layouts/partials/head.html](file:///f:/Notes/layouts/partials/head.html) 用 `resources.Match "css/_*.css" + Concat`，**Hugo 编译期合并**，浏览器只请求一次 `main.bundle.css`。

**不要去掉 head.html 的 [lyrumu 改造] 段**——升级 Blowfish 主题时优先 diff `themes/blowfish/layouts/partials/head.html`，把项目级这段保留下来。

### 加新 CSS 文件的 SOP

```bash
# 例：加一个 /about/ 的 timeline 组件
1. 创建 assets/css/_10_timeline.css      # 下一个序号（_01~_09 已用完）
2. 顶部加 header 注释（职责 + 来源 + 加载顺序）
3. 保存即可 —— 不需要改 head.html、不需要改 custom.css
4. hugo server 验证
```

**序号规则**：
- `_01_` ~ `_09_` 已分配给现有模块（详见 §3）
- 新文件用下一个两位数 `_10_xxx.css` / `_11_xxx.css`
- **序号大的在后面加载**（能覆盖前面的）
- 如果新文件依赖前面文件的变量（如 `--accent`），序号必须比被依赖的文件大
- 不要跳号（`_10_` 用完才能用 `_11_`，不能直接跳到 `_20_`）

**是否要拆 `_05_cards.css`**：
当前 1041 行包含 6 类卡片（module / vault / article-link / life / music-list / works-sub / file-tree / section-rule），review 价值仍可接受。**只在行数超过 1500 或某个子模块独立维护时才拆**，届时建议按"使用场景"再拆：`cards-list.css`（列表型） + `cards-grid.css`（瀑布流） + `shortcodes.css`（file-tree / section-rule 这种工具型）。

### 加新 CSS 模块的反模式（不要这样做）

❌ 在 `custom.css` 里加 `@import url("_10_xxx.css")` → 触发上面的踩坑  
❌ 直接编辑 `themes/blowfish/.../*.css` → 升级主题被覆盖  
❌ 把新样式塞进 `custom.css.bak.v2` → 备份文件不参与构建  
❌ 不加 `_NN_` 前缀（如 `_timeline.css`）→ `resources.Match "css/_*.css"` 匹配不上，文件不会被加载

### 紧急回滚 CSS 拆分

如果新拆的文件出问题想回滚：

```bash
cd f:\Notes
cp assets/css/custom.css.bak.v2 assets/css/_99_all.css   # 复制原文件作为最后加载的"全量兜底"
# head.html 不动（resources.Match 自动按字典序加载 _99 在最末）
# hugo server 验证 → 自定义样式按原版生效
```

回滚后即可定位是新文件的问题还是拆分本身的问题。
