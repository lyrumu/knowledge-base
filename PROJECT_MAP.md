# 项目地图 — 个人网站 `f:\Notes\`

> 最后更新：2026-06-24 · /about/ 加站点统计模块（零后端 + GitHub Actions 自动更新；新增 layouts/partials/about-stats.html、layouts/shortcodes/about-stats.html、scripts/refresh_stats.py、.github/workflows/refresh-stats.yml、data/site-stats.yaml） · Hugo v0.163.2 · Blowfish v2

---

## 1. 这是什么

一个基于 **本地 Obsidian Vault** 驱动的 **Hugo 静态站点**，部署在 **Cloudflare Pages**。
所有文章用 Obsidian 写 → 跑同步脚本 → `git push` → 自动部署上线。

---

## 2. 快速查阅：我想改什么 → 改哪个文件

| 我想…… | 改这个文件 |
|---------|-----------|
| 改封面的标题 / subtitle / 按钮文案 | [`data/cover.yaml`](file:///f:/Notes/data/cover.yaml) |
| 改封面的颜色 | [`assets/css/_01_tokens.css`](file:///F:/Notes/assets/css/_01_tokens.css) 顶部 `:root` / `html.dark` 的 `--bg-base / --line / --accent`（v3：封面 `--pal-*` 已派生自全局变量，统一改一处即可） |
| 改封面的字距 / 大小 / 花边位置 | [`assets/css/_08_cover.css`](file:///F:/Notes/assets/css/_08_cover.css) |
| 改内页"小封面"的文案 | 对应 `content/xxx/_index.md` 的 frontmatter `kicker / subtitle` |
| 换 /notes/ 的分类卡 | [`data/vault.yaml`](file:///f:/Notes/data/vault.yaml) |
| 换 /life/ 的子模块卡 | [`data/life.yaml`](file:///f:/Notes/data/life.yaml)（加图片 / 读书 / 旅行…都改这里） |
| 换 /life/music/ 的歌单 | [`data/music.yaml`](file:///f:/Notes/data/music.yaml)（加一首填一个 `- title/artist/cover/src/...` 条目） |
| 换 /life/music/ 的封面/SVG 动画 | [`assets/css/_05_cards.css`](file:///F:/Notes/assets/css/_05_cards.css) 的 `.life-sub-cover-*` 规则 |
| 换 /works/ 的子模块卡 | [`data/works.yaml`](file:///f:/Notes/data/works.yaml)（projects / resources / tools…） |
| 换 /works/projects/ 的项目卡 | [`data/projects.yaml`](file:///f:/Notes/data/projects.yaml)（加一条填 `- name/title/desc/cover/href/repo/tags/date/featured`） |
| 换 /works/resources/ 的资源卡 | [`data/resources.yaml`](file:///f:/Notes/data/resources.yaml)（加一条填 `- name/title/desc/cover/file/format/size/tags/date/source`） |
| 改 /works/projects/ 的 3D 倾斜角度 | [`assets/css/_06_works-cards.css`](file:///F:/Notes/assets/css/_06_works-cards.css) 的 `.project-card` 或 shortcode 里的 `data-tilt-*` |
| 加一个 Lucide icon | [`layouts/partials/cover/icon.html`](file:///f:/Notes/layouts/partials/cover/icon.html) 加 `else if` 分支 |
| 改 /about/ 联系方式图标 / 邮箱 | [`content/about/_index.md`](file:///f:/Notes/content/about/_index.md) + [`layouts/partials/about-contact.html`](file:///f:/Notes/layouts/partials/about-contact.html)（base64 邮箱解码 + Toast） |
| 改 /about/ 图标玻璃效果 | [`assets/css/_09_about.css`](file:///F:/Notes/assets/css/_09_about.css)（`.about-contact-glass` / `.about-contact-btn` / `.copy-toast`） |
| 改顶栏的菜单项 | [`hugo.toml`](file:///f:/Notes/hugo.toml) 的 `[[menu.main]]` 段 |
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
│   │   ├── _08_cover.css           # ★ 封面页（全屏 + 花边 + 字符入场）
│   │   └── _09_about.css           # ★ About 页（profile + 标签 + 液态玻璃联系方式）
│   └── icons/                      # Simple Icons 品牌色 SVG（github/gmail/qq 等联系方式图标）
│
├── archetypes/
│   └── default.md                  # `hugo new` 模板
│
├── content/                        # ★ 所有页面内容
│   ├── _index.md                   # 封面（极简，只放 layout: page）
│   ├── notes/                      # /notes/ 学习笔记
│   │   ├── _index.md
│   │   ├── docs/                   # Docs 分类（含 vscode, wsl2, docker 等嵌套）
│   │   ├── language/               # Language 分类（含 cpp, python）
│   │   ├── demo/                   # Demo 分类（含 minecraft, aipython）
│   │   └── tools/                  # 工具脚本页面
│   ├── works/                      # /works/ 相关（作品 / 资源 / 工具）
│   │   ├── _index.md               # 入口（works-grid 短代码）
│   │   ├── projects/_index.md      # 项目子页（projects-list 短代码 + 3D 倾斜）
│   │   ├── resources/_index.md     # 资源子页（resources-list 短代码 + 瀑布流）
│   │   └── tools/_index.md         # 工具子页（占位 + 计划收录）
│   ├── life/                       # /life/ 生活（可扩展子模块网格）
│   │   ├── _index.md               # 子模块入口（life-grid 短代码）
│   │   └── music/_index.md         # /life/music/ 子页
│   └── about/_index.md             # /about/ 关于（avatar + 液态玻璃联系方式 + 技术栈 + GitHub 热力图）
│
├── data/                           # ★ 数据驱动（改这里就能改 UI）
│   ├── cover.yaml                  # 封面所有内容 + 调色
│   ├── vault.yaml                  # /notes/ 的 vault 分类卡
│   ├── life.yaml                   # /life/ 子模块清单（music / 图片 / 读书…）
│   ├── music.yaml                  # /life/music/ 歌单
│   ├── works.yaml                  # /works/ 子模块清单（projects / resources / tools…）
│   ├── projects.yaml               # /works/projects/ 项目清单
│   └── resources.yaml              # /works/resources/ 资源清单
│
├── layouts/                        # ★ 自定义模板（覆写主题）
│   ├── _default/list.html          # section 主页 → page-hero 模式
│   ├── home.json                   # home kind 的 JSON 输出（消 build WARN；内容同主题 _default/index.json）
│   ├── page.html                   # 任何 layout: "page" 的页面（消 build WARN；复用主题 single.html 的 main 块）
│   ├── partials/
│   │   ├── head.html               # ⚠️ [lyrumu 改造] 覆盖 Blowfish 主题版本
│   │   │                           #  原因：CSS `@import` 在 Hugo Pipes 不展开（详见 §8 踩坑提醒）
│   │   │                           #  改为：resources.Match "css/_*.css" + Concat
│   │   ├── cover/icon.html         # Lucide SVG icon 字典
│   │   ├── cover/page-hero.html    # 内页"小封面" partial
│   │   ├── home/custom.html        # 封面 partial
│   │   ├── about-stats.html        # /about/ "Site & Activity" 统计模块（11 张卡片）
│   │   ├── header/components/
│   │   │   ├── desktop-menu.html   # 加 GitHub 按钮
│   │   │   └── mobile-menu.html    # 加 GitHub 按钮
│   │   ├── extend-head.html        # 第三方库（Splitting.js + AOS.js + VanillaTilt.js）
│   │   ├── music-player.html       # 粘性音乐播放器（被 music-list 自动注入）
│   │   └── about-contact.html      # /about/ 联系方式图标卡 partial（被 about-contact shortcode 调）
│   └── shortcodes/
│       ├── page-hero.html          # {{< page-hero >}} 短代码
│       ├── vault-sections.html     # /notes/ 分类网格
│       ├── life-grid.html          # /life/ 子模块网格
│       ├── music-list.html         # /life/music/ 歌曲列表
│       ├── works-grid.html         # /works/ 子模块网格
│       ├── projects-list.html      # /works/projects/ 项目列表（3D 倾斜）
│       ├── resources-list.html     # /works/resources/ 资源列表（瀑布流）
│       ├── file-tree.html          # 可折叠文件树
│       ├── about-contact.html      # /about/ 联系方式图标卡（壳）
│       ├── about-stats.html        # {{< about-stats >}} 短代码（包装 about-stats.html partial）
│       └── section-rule.html       # ✦ 分隔符
├── scripts/                        # ★ 运维脚本
│   ├── vault-to-hugo.ps1           # Vault → Hugo 同步（日常使用）
│   └── refresh_stats.py            # 拉 CF Analytics GraphQL API 写 yaml（被 workflow 调）
├── .github/
│   └── workflows/
│       └── refresh-stats.yml       # 每天 03:00 UTC 跑 refresh_stats.py，commit data/site-stats.yaml
├── data/
│   ├── cover.yaml                  # 封面所有内容（标题/介绍/按钮等）
│   ├── modules.yaml                # [废弃] 原 /start/ 大厅用，已注释说明
│   ├── site-stats.yaml             # /about/ 统计模块数据源（被 GitHub Actions 自动更新）
│   ├── vault.yaml                  # 顶栏 + 封面 Vault 卡的数据
│   └── works.yaml                  # /works/ 卡片的展示数据
├── .vscode/                        # 编辑器配置（用户设的，非自动生成）
│
├── static/                         # 静态资源
│   ├── fonts/                      # 字体文件（本地化）
│   ├── image/                      # 装饰 PNG（花边 / 花朵 / musicheart）
│   │   ├── life/music/             # /life/music/ 封面（用户自行放入）
│   │   └── works/                  # /works/ 子模块封面
│   │       ├── projects/           # /works/projects/ 项目封面（用户自行放入）
│   │       └── resources/          # /works/resources/ 资源封面（用户自行放入）
│   ├── life/music/                 # /life/music/ 音频文件（用户自行放入）
│   ├── works-resources/            # /works/resources/ 下载文件（用户自行放入）
│   ├── js/music-player.js          # 音乐播放器逻辑
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
├── DONE.md                         # 开发日志（本地保留）
└── .trae/rules/个人网站开发规则.md   # 项目宪法
```

---

## 4. 部件对应速查

### 封面（`/_index.md`）

| 元素 | 数据源 | 模板 |
|------|--------|------|
| 封面排版 / 社交链接 / 花边 | [`data/cover.yaml`](file:///f:/Notes/data/cover.yaml) | [`layouts/partials/home/custom.html`](file:///f:/Notes/layouts/partials/home/custom.html) |
| 封面 CSS（字体 / 调色 / 布局） | — | [`assets/css/_08_cover.css`](file:///F:/Notes/assets/css/_08_cover.css) |
| 封面主题切换按钮 | — | 内嵌在 `custom.html` 的 JS |
| 封面装饰元素（四角花朵） | — | 直接用 `static/image/` 下的 png |
| 封面调色（明 / 暗） | `cover.yaml` → `palette` | `custom.html` 的 `<style>` 块 |

### 内页"小封面"（section 主页顶部）

| 元素 | 数据源 | 模板 |
|------|--------|------|
| kicker / subtitle / eyebrow | 各 `_index.md` frontmatter | [`layouts/partials/cover/page-hero.html`](file:///f:/Notes/layouts/partials/cover/page-hero.html) |
| 短代码调用 | — | [`layouts/shortcodes/page-hero.html`](file:///f:/Notes/layouts/shortcodes/page-hero.html) |
| CSS | — | [`assets/css/_04_hero.css`](file:///F:/Notes/assets/css/_04_hero.css) |

### /notes/ 分类页

| 元素 | 数据源 | 模板 |
|------|--------|------|
| 分类卡列表 | [`data/vault.yaml`](file:///f:/Notes/data/vault.yaml) | [`layouts/shortcodes/vault-sections.html`](file:///f:/Notes/layouts/shortcodes/vault-sections.html) |

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
| 粘性播放器 HTML | — | [`layouts/partials/music-player.html`](file:///f:/Notes/layouts/partials/music-player.html) |
| 播放器逻辑（点击切歌 / 进度跳转 / 记忆位置 / 键盘） | — | [`static/js/music-player.js`](file:///f:/Notes/static/js/music-player.js) |
| 列表样式 + 播放器样式 | — | [`assets/css/_05_cards.css`](file:///F:/Notes/assets/css/_05_cards.css) 的 `.music-item` + [`_07_music-player.css`](file:///F:/Notes/assets/css/_07_music-player.css) 的 `.music-player` |
| 资源存放约定 | `static/life/music/<slug>.mp3` + `static/image/life/music/<slug>.jpg` | — |

### /about/ 联系方式图标卡（iOS 液态玻璃）

| 元素 | 数据源 | 模板 |
|------|--------|------|
| 头像 + 个人信息 + 联系方式的整体排版 | [`content/about/_index.md`](file:///f:/Notes/content/about/_index.md) | markdown（`.about-profile` 容器 + `{{< about-contact >}}` 短代码） |
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

所有 section 主页（/notes/ /works/ /life/ /about/）都走 [`layouts/_default/list.html`](file:///f:/Notes/layouts/_default/list.md)。每个页面的 `_index.md` 可以设自己的 `kicker` / `subtitle`。

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