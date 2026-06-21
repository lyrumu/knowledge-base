# 已完成清单 — 个人网站(基于本地 Obsidian Vault)

> 维护方式：每完成一大阶段，在下方加一段记录。

---

## 2026-06-21 · projects 卡片链接重构 + 按钮对比度修复

### 问题 1：在线/源码按钮都跳到同一个 URL

用户反馈：`projects.yaml` 里 `href` 和 `repo` 填了不同地址，但页面里点两个按钮都跳到 `href`。

#### 根因

[`layouts/shortcodes/projects-list.html`](file:///f:/Notes/layouts/shortcodes/projects-list.html) 旧版把整张卡片包在一个 `<a href="$p.href">` 里，"在线""源码"两个按钮是 `<span>` 装饰（没 `href`），点击被外层 `<a>` 吞掉 → 全跳 `href`。`data-repo` 属性根本没人读。

HTML 不允许 `<a>` 嵌套 `<a>`，所以必须重构。

#### 修复

- 移除外层 `<a class="project-card-link">`，两个按钮改成独立 `<a>` 各自跳对应地址
- 整张卡不可点（只有底部按钮可点）
- 顺带改善 a11y：CSS 早就有 `.project-card:focus-within .project-card-actions`，按钮变 `<a>` 后键盘 Tab 也能聚焦展开 actions

### 问题 2：重构后 `<a>` 默认样式破坏按钮

#### 现象

- 按钮变成 `<a>` 后浏览器默认**蓝色文字**盖掉 `color: var(--bg-base)`
- 浏览器默认**下划线**出现

#### 修复

[`.project-card-btn`](file:///f:/Notes/assets/css/custom.css) 覆盖全状态：

```css
.project-card-btn,
.project-card-btn:link,
.project-card-btn:visited {
  color: var(--bg-base);
  text-decoration: none;
  /* ... */
}
.project-card-btn:hover,
.project-card-btn:focus,
.project-card-btn:active {
  color: var(--bg-base);
  text-decoration: none;
  /* ... */
}
```

`:link`/`:visited` 提高 specificity 到 `(0,2,0) > 默认 (0,1,0)`，确保胜出。

### 问题 3：hover 反光层洗白按钮文字

#### 现象

重构前因为外层 `<a class="project-card-link">` 自带 `z-index: 2`（在第 2773 行），挡住了 `.project-card::after` 反光层（z-index 1）。重构后外层 `<a>` 被移除，z-index 保护丢了，hover 时反光层蒙住整个卡片表面，米白文字被冲淡。

#### 修复（双保险）

1. **按钮端**：`.project-card-btn` 加 `position: relative; z-index: 2;`，让按钮始终在反光层之上
2. **反光层端**：`.project-card::after` 加 `mix-blend-mode: multiply;`，让反光只和下层（封面/背景）按 multiply 混合，不影响上层（按钮文字），即使 z-index 没赢透也能保证文字清晰

#### 关键工程教训

**重构组件时小心"叠层保护"的传递**——旧版 `.project-card-link` 的 `z-index: 2` 是隐式依赖，重构移除外层 `<a>` 后没人接力，z-index 保护就丢了。

### 问题 4：米白文字在橘色按钮上对比度不够

#### 现象

- 默认 background `var(--accent)` = `#D97757`（鲜橙），color `var(--bg-base)` = `#FAF9F5`（米白）
- **对比度只有 3.08:1**，勉强够 AA Large（3:1）但小字（0.68rem ≈ 11px）看不清
- 反光层 + `color-mix(accent 80%, fg-base 20%)` 让 hover 背景变成 `#B46B45`，对比度 4.06:1（接近 AA 但不够）

#### 修复（关键思路：让 background 更深，不是更亮）

```css
.project-card-btn {
  /* v3 关键修复：米白在纯 accent 上只有 3.08:1
     改成 color-mix(accent 70%, fg-base 30%) = #A15C46，对比度 4.64:1 ✓ AA */
  background: color-mix(in srgb, var(--accent) 70%, var(--fg-base));
}

.project-card-btn:hover {
  /* hover 时进一步加深 = #8E5340，对比度 5.36:1 ✓ AA */
  background: color-mix(in srgb, var(--accent) 60%, var(--fg-base));
}
```

#### 试错记录（避免后人重蹈覆辙）

| 试错方向 | 结果 | 教训 |
|---|---|---|
| `color-mix(accent 80%, fg-base 20%)` | 4.06:1 差一点 AA | 暗 20% 不够 |
| `color-mix(accent 88%, bg-base 12%)` 亮化 | 2.6:1 完全看不清 | **方向反了**，对比度更低 |
| 加 mix-blend-mode multiply | 修了反光层，但解决不了对比度问题 | mix-blend-mode 只解决"叠加"问题 |

**关键**：用户最初反馈"按钮变暗"以为是设计偏好问题，走了"变亮"方向，结果更糟。后来才意识到"按钮变暗"是真实问题——background 变深后视觉变暗。**修复方向是让 background 更深以增强对比度**，而不是更亮。

### 关键文件清单（本次）

| 类型 | 路径 |
|---|---|
| 改动 | [`layouts/shortcodes/projects-list.html`](file:///f:/Notes/layouts/shortcodes/projects-list.html) — 移除外层 `<a>`，两个按钮独立 |
| 改动 | [`assets/css/custom.css`](file:///f:/Notes/assets/css/custom.css) — `.project-card-btn` 加 z-index / 颜色对比度修复，`.project-card::after` 加 mix-blend-mode |
| 数据 | [`data/projects.yaml`](file:///f:/Notes/data/projects.yaml) — 不变 |

### 验证

| 场景 | 旧 | 新 |
|---|---|---|
| 在线按钮点击 | 跳 href（和源码按钮一样） | 跳 href ✓ |
| 源码按钮点击 | 跳 href（被外层 a 吞） | 跳 repo ✓ |
| 默认文字色 | 浏览器默认蓝 | `#FAF9F5` 米白 ✓ |
| 默认对比度 | 3.08:1 ❌ | 4.64:1 ✓ AA |
| hover 对比度 | 4.06:1 ❌ | 5.36:1 ✓ AA |
| hover 反光层 | 覆盖按钮，文字被冲淡 | 不影响文字（mix-blend-mode + z-index 双保险）|

---

## 2026-06-21 · 暗主题调色板统一 + Claude 暖深重构

### 问题

用户反馈：暗主题下**后续页面**卡片和背景几乎融为一体，且**封面**与后续页面颜色脱节（封面紫、卡片看不清）。切换主题时各页面行为不一致，改色需要分别改多处。

### 根因（三套独立色板互相不通气）

| 色板 | 控制范围 | 来源 |
|---|---|---|
| princess RGB 三元组 | 所有 blowfish `bg-neutral-*` utility（body / header / scroll-to-top / hero 遮罩） | `hugo.toml` 的 `colorScheme = 'princess'` |
| `--pal-*` 调色板 | **封面**的背景 / 线条 / 文字 / 按钮 | `layouts/partials/home/custom.html` 的 `<style>` 块 |
| `--bg-base / --line / --accent` | 我自己定义的卡片（`.module-card` 等） | `assets/css/custom.css` |

三套各管各的 → 改一处不能带另一处 → 封面与后续页面脱节。

### 修复（v3 统一架构）

```
┌─────────────────── 唯一数据源 ───────────────────┐
│  :root { --bg-base / --line / --accent ... }      │  ← 改这里就完事
│  html.dark { --bg-base: #141413 ... }             │  ← 暗主题覆写
└───────────────────────────────────────────────────┘
           ↓              ↓              ↓
    ┌──────────┐    ┌──────────┐   ┌─────────────┐
    │ 封面      │    │ 卡片      │   │ blowfish    │
    │ --pal-*   │    │ .module- │   │ utility     │
    │ (var派生) │    │ card 等  │   │ bg-neutral  │
    └──────────┘    └──────────┘   └─────────────┘
```

#### 改动 1：封面 `--pal-*` 改为派生

[`layouts/partials/home/custom.html`](file:///f:/Notes/layouts/partials/home/custom.html#L53-L66) 把写死的颜色值改成 `var(--bg-base / --line / --accent)` 派生：

```css
.cover-page {
  --pal-bg-from: var(--bg-base);    /* 而不是 {{ $pal.background_from }} */
  --pal-bg-to:   var(--bg-deep);
  --pal-title:   var(--fg-base);
  --pal-line:    var(--line);
  --pal-accent:  var(--accent);
  /* ... 共 14 个全部派生 */
}
```

`data/cover.yaml` 里的 `palette` 字段保留（兼容旧配置），但实际渲染以 `var()` 为准。

#### 改动 2：删掉 custom.css 里的封面暗色覆写块

[`assets/css/custom.css §28`](file:///f:/Notes/assets/css/custom.css#L1571-L1582) 删掉整个 `html.dark .cover-page { --pal-*: ... }` 覆写块（15 行），由 v3 派生自动接管。

#### 改动 3：覆写 princess 的暗主题 RGB（驱动 blowfish utility）

[`assets/css/custom.css §0`](file:///f:/Notes/assets/css/custom.css#L89-L100) 的 `html.dark` 块里追加：

```css
--color-neutral-800: 20, 20, 19;   /* = #141413 Claude 暖深（替换 princess 紫 #2D212D）*/
--color-neutral-900: 15, 14, 13;   /* = #0F0E0D Claude bg-deep */
```

这样所有 `dark:bg-neutral-800/25|50|60` 工具类在暗主题下自动变 `rgba(20,20,19, .25|50|60)` 透明黑，header 的 `backdrop-filter` 模糊效果完全保留。

#### 改动 4：调亮暗主题卡片底色（提高对比度）

[`assets/css/custom.css`](file:///f:/Notes/assets/css/custom.css) 把 18 处暗主题卡片底色统一：

- 默认：`rgba(255,255,255, 0.015/0.018/0.02)` → **`0.03`**
- hover：`rgba(255,255,255, 0.035/0.04)` → **`0.06`**
- 边框 `--line`：`#2A2926` → **`#30302E`**（Claude 官方 surface，contrast ratio 1.4:1）

### 关键工程教训

**不要用 `!important` 强改 blowfish utility class**：
- 第一次尝试 `html.dark body { background-color: #141413 !important }` + `.bg-neutral-800/50 { ... !important }`
- 结果破坏了顶部 header 的 `backdrop-blur` 模糊遮罩 + projects 页面渲染
- 正确做法：覆写 princess 的底层 RGB 三元组 `--color-neutral-800/900`，让 blowfish utility 自动跟着变（不动 specificity、不动 class 树）

**调色板架构原则**：
- 调色板要**单一数据源**（`:root` + `html.dark` 两个变量块）
- 子模块用 `var()` 派生，不要写死颜色值
- 改一处变量 → 全部跟着变

### 关键文件清单（本次）

| 类型 | 路径 |
|---|---|
| 改动 | [`layouts/partials/home/custom.html`](file:///f:/Notes/layouts/partials/home/custom.html) — `--pal-*` 改 `var()` 派生 |
| 改动 | [`assets/css/custom.css`](file:///f:/Notes/assets/css/custom.css) — §0 加 princess RGB 覆写、§28 删掉旧覆写块、§0.5 删掉 body 强改（试错）、18 处卡片底色统一 |
| 文档 | `DONE.md` / `PROJECT_MAP.md` |

### 验证链路（暗主题）

改 `--bg-base: #141413` 一个值，自动触发：

| 渲染位置 | 走的变量 | 结果 |
|---|---|---|
| 封面背景渐变 | `--pal-bg-from: var(--bg-base)` | `#141413` |
| 封面底部渐变 | `--pal-bg-to: var(--bg-deep)` | `#0F0E0D` |
| 封面标题文字 | `--pal-title: var(--fg-base)` | `#FAF9F5` |
| 封面分隔线 | `--pal-line: var(--line)` | `#30302E` |
| 卡片边框 | `border: 1px solid var(--line)` | `#30302E` |
| body / header / scroll-to-top | `bg-neutral-800 → rgb(20,20,19)` | `#141413` |
| 正文文字色 | `var(--fg-base)` | `#FAF9F5` |

### 后续

- 亮主题也保持公主紫调（用户觉得 OK），不动 princess
- 调色板统一后，未来想换主题（如想完全脱离 princess）只需改 `:root` / `html.dark` 两个变量块

---

## 2026-06-21 · works 模块搭建 — 入口 + Projects(3D 倾斜) + Resources(瀑布流)

### 决策（与用户确认）

| 项 | 决定 |
|---|---|
| 页面结构 | 子模块网格（与 /life/ 同模式）：/works/ 入口 → /works/projects/ + /works/resources/ + /works/tools/(占位) |
| 内容分类 | 3 个：项目 Projects / 资源 Resources / 工具 Tools（draft） |
| Projects 视觉 | 双列 grid 卡片 + 3D 鼠标倾斜（VanillaTilt.js）+ 鼠标反光（CSS radial-gradient + --glare-x/y）+ hover 揭示 tags/actions |
| Resources 视觉 | CSS columns 瀑布流 + 格式徽章 + 元信息（size/date）+ 下载按钮 |
| 入场动画 | AOS.js（fade-up），但应用到卡片**内部子元素**避开 VanillaTilt 的 transform 冲突 |
| 工具 | 全部用第三方库：AOS.js（jsDelivr）+ VanillaTilt.js（jsDelivr），无新造轮子 |

### 数据驱动架构

- 新建 [data/works.yaml](file:///f:/Notes/data/works.yaml) — works 子模块清单（projects / resources / tools(draft)）
- 新建 [data/projects.yaml](file:///f:/Notes/data/projects.yaml) — 项目清单（name / title / desc / cover / href / repo / tags / date / featured）
- 新建 [data/resources.yaml](file:///f:/Notes/data/resources.yaml) — 资源清单（name / title / desc / cover / file / format / size / tags / date / source）
- 约定资源路径：项目封面 `/image/works/projects/<slug>.png`，资源封面 `/image/works/resources/<slug>.png`

### 短代码

- 新建 [layouts/shortcodes/works-grid.html](file:///f:/Notes/layouts/shortcodes/works-grid.html) — 渲染子模块网格（沿用 life-grid 风格）
- 新建 [layouts/shortcodes/projects-list.html](file:///f:/Notes/layouts/shortcodes/projects-list.html) — 渲染项目列表 + 3D 倾斜
- 新建 [layouts/shortcodes/resources-list.html](file:///f:/Notes/layouts/shortcodes/resources-list.html) — 渲染资源列表（瀑布流）

### 第三方库集成（无依赖，无造轮）

- AOS.js 2.3.4 + aos.css — jsDelivr CDN，prefers-reduced-motion 检测自动禁用
- VanillaTilt.js 1.8.1 — jsDelivr CDN，IntersectionObserver 延迟初始化（仅在卡片进视口时挂载）
- 全部通过 [layouts/partials/extend-head.html](file:///f:/Notes/layouts/partials/extend-head.html) 统一管理（之前 shortcode 各自挂 IIFE 有 CDN 时机 bug，已统一）

### 关键工程修复（2026-06-21 第二轮）

**AOS 缺失 CSS**：
- 之前只引 aos.js，没引 aos.css → AOS 完全没视觉效果
- 修：extend-head.html 加 `<link rel="stylesheet" href="...aos.css">`

**VanillaTilt init 时机 bug**：
- 之前 IIFE 在 shortcode 末尾同步执行，但 CDN defer 脚本可能还没加载完
- 修：移到 extend-head.html 的 `window.load` 回调里

**AOS 与 VanillaTilt transform 冲突**：
- AOS `fade-up` 动 `transform: translateY(...)`；VanillaTilt 动 `transform: rotate(...)` — 改同一属性会互相覆盖
- 修：把 AOS 从 `.project-card` 外层移到**内部子元素** `.project-card-cover` + `.project-card-body`，VanillaTilt 仍管外层

**AOS `transition` 接管 hover 动画**：
- AOS 给 `[data-aos]` 注入 inline `transition: ... 0.9s`；动画完成后 inline style 不清理
- `.resource-card` 自身有 `transition: ..., transform 0.5s`，hover 上浮被接管成 0.9s 显得迟钝
- 修：`aos:in` 事件触发 1s 后 `el.style.transition = ''`，让原本 CSS 的 transition 接管 hover 效果

**`.reveal` 类 scroll-driven animation 兼容性问题**：
- 之前用 `animation-timeline: view()`（scroll-driven animation API，Chrome 115+ 才支持）
- Firefox / 旧 Edge 不支持，入场效果看不到
- 修：移除 shortcode 里的 `.reveal` 类，统一改用 AOS

**3D perspective 位置**：
- 之前 `.project-card { transform: perspective(1000px) }` 会和 AOS 的 transform transition 冲突
- 修：移到 `.projects-grid` 父元素（perspective 是渲染容器属性，可放父级）

### 页面 & 样式

- 新建 [content/works/_index.md](file:///f:/Notes/content/works/_index.md) — works 入口（用 works-grid）
- 新建 [content/works/projects/_index.md](file:///f:/Notes/content/works/projects/_index.md) — 项目子页
- 新建 [content/works/resources/_index.md](file:///f:/Notes/content/works/resources/_index.md) — 资源子页
- 新建 [content/works/tools/_index.md](file:///f:/Notes/content/works/tools/_index.md) — 工具子页（占位 + 计划收录清单）
- [assets/css/custom.css §34](file:///f:/Notes/assets/css/custom.css#L2393-L2660) — works-grid（与 life-grid 共享视觉规范，独立 CSS）
- [assets/css/custom.css §35](file:///f:/Notes/assets/css/custom.css#L2662-L2990) — projects-list（3D 倾斜 + hover 揭示）
- [assets/css/custom.css §36](file:///f:/Notes/assets/css/custom.css#L2992-L3310) — resources-list（CSS columns 瀑布流）

### 图标扩充

- [layouts/partials/cover/icon.html](file:///f:/Notes/layouts/partials/cover/icon.html) 新增 icon：`code-2` / `package` / `download` / `external-link`

### 响应式

- 桌面端：projects 双列、resources 双列瀑布流、3D 倾斜 + 反光
- 移动端（max-width: 720px）：全部单列、3D 倾斜禁用、hover 揭示改为常显

### 关键文件清单（本次）

| 类型 | 路径 |
|---|---|
| 新增 | `data/works.yaml` / `data/projects.yaml` / `data/resources.yaml` |
| 新增 | `layouts/shortcodes/works-grid.html` / `projects-list.html` / `resources-list.html` |
| 新增 | `content/works/{_index,projects/_index,resources/_index,tools/_index}.md` |
| 大改 | `assets/css/custom.css`（追加 §34/§35/§36，约 920 行） |
| 大改 | `layouts/partials/extend-head.html`（AOS + VanillaTilt 统一初始化） |
| 大改 | `layouts/partials/cover/icon.html`（4 个新 icon） |
| 文档 | `DONE.md` / `PROJECT_MAP.md` |

### 用户下一步操作

1. 准备真实项目封面：放图到 `static/image/works/projects/<slug>.png`
2. 准备真实资源文件：放文件到 `static/works-resources/<file>`，封面到 `static/image/works/resources/<slug>.png`
3. 在 `data/projects.yaml` / `data/resources.yaml` 替换占位示例为真实条目

### 后续

- /works/tools/ 有内容时启用（现在 draft）
- 资源下载统计 / 链接二维码
- /works/ 顶部 banner / 项目筛选（按 tag 过滤）

---

## 2026-06-20 · life 模块扩展 — 音乐子页 + 可扩展子模块架构

### 决策（与用户确认）

| 项 | 决定 |
|---|---|
| 音乐资源形式 | 上传到 `static/life/music/`，用纯 HTML5 `<audio>` |
| life 是否可扩展 | 是，按子模块网格来做（图片 / 读书 / 旅行…） |
| music 页面结构 | 两层：`life/_index.md` 子模块入口 + `life/music/_index.md` 子页 |
| 封面类型 | 用户提供 `musicheart.png` / `.svg`（手绘耳机+心形+音符） |
| 歌曲列表交互 | 动态 lyric 风格：列表只点一次，底部粘性播放器统一控制 |

### 数据驱动架构

- 新建 [data/life.yaml](file:///f:/Notes/data/life.yaml) — life 子模块清单（music 已配好；加图片/读书只改这里）
- 新建 [data/music.yaml](file:///f:/Notes/data/music.yaml) — 歌单（title / artist / album / cover / src / duration / mood / note）
- 约定资源路径：封面 `/image/life/music/<slug>.jpg`、音频 `/life/music/<slug>.mp3`

### 短代码 & partial

- 新建 [layouts/shortcodes/life-grid.html](file:///f:/Notes/layouts/shortcodes/life-grid.html) — 渲染子模块网格（沿用 `modules-grid` 风格：左封面 / 中 body / 右 CTA）
- 新建 [layouts/shortcodes/music-list.html](file:///f:/Notes/layouts/shortcodes/music-list.html) — 渲染歌曲列表 + 自动注入播放器
- 新建 [layouts/partials/music-player.html](file:///f:/Notes/layouts/partials/music-player.html) — 底部粘性播放器 HTML
- 新建 [static/js/music-player.js](file:///f:/Notes/static/js/music-player.js) — 播放器逻辑

### 播放器功能（无第三方依赖）

- 点击 `.music-item` → 切换曲目并自动播放
- 上一首 / 下一首 / 播放-暂停 / 关闭
- 进度条拖动跳转；实时显示 current / duration
- 自动播放下一首（列表循环）；当前曲目高亮 + EQ 跳条动画
- 播放时封面慢转 14s/圈（CSS 动画）；暂停时停转
- localStorage 记忆播放位置（刷新后继续）
- 键盘快捷键：`Space` 播放/暂停、`Shift+←/→` 上下首
- `src` 为空的示例条目自动变灰不响应（`is-disabled` 状态）

### 页面 & 动画

- [content/life/_index.md](file:///f:/Notes/content/life/_index.md) — 改用 `{{< life-grid >}}`
- 新建 [content/life/music/_index.md](file:///f:/Notes/content/life/music/_index.md) — 音乐子页
- 卡片 hover 动画：图片旋转 -6° + 缩放 1.08 + 上浮 -2px（沿用 module-card 基础动效语言）
- SVG 类型默认带 6s 缓慢呼吸动画（不依赖 hover，永远在动）
- emoji 类型 hover 时旋转 -10° 缩放 1.12
- 播放器：玻璃质感（`backdrop-filter: blur`）、accent 色进度条渐变、hover 时进度 thumb 浮现

### 样式 & 图标

- [assets/css/custom.css §32](file:///f:/Notes/assets/css/custom.css#L1694-L1900) — life 子模块卡样式
- [assets/css/custom.css §33](file:///f:/Notes/assets/css/custom.css#L1900-L2360) — music 列表 + 粘性播放器
- [layouts/partials/cover/icon.html](file:///f:/Notes/layouts/partials/cover/icon.html) 新增 icon：`music`、`image`、`play`、`pause`、`skip-back`、`skip-forward`、`volume-2`、`volume-x`、`shuffle`、`repeat`、`x`

### 关键文件清单（本次）

| 类型 | 路径 |
|---|---|
| 新增 | `data/life.yaml`、`data/music.yaml` |
| 新增 | `layouts/shortcodes/life-grid.html`、`layouts/shortcodes/music-list.html` |
| 新增 | `layouts/partials/music-player.html`、`static/js/music-player.js` |
| 新增 | `content/life/music/_index.md` |
| 调整 | `content/life/_index.md`（改用 life-grid） |
| 大改 | `assets/css/custom.css`（§32 / §33 新增，约 690 行） |
| 大改 | `layouts/partials/cover/icon.html`（新增 11 个 icon 分支） |

### 用户下一步操作

1. 把 mp3 放进 `static/life/music/`，封面放进 `static/image/life/music/`
2. 在 `data/music.yaml` 把示例条目替换成真实歌曲（参考注释里的字段格式）
3. `hugo server` 本地预览

### 后续

- /life/ 第二个子模块（图片 / 读书 / 旅行…）
- /works/ 子模块网格化（套用 life-grid 模式）
- 全站深色封面标题里 musicheart 装饰

---

## 2026-06-19 · UI 整体同步 + 封面/顶栏修复

### 同步封面风格到后续页面

- 抽出可复用的"小封面"模式：`layouts/partials/cover/page-hero.html`（partial）+ `layouts/shortcodes/page-hero.html`（短代码）
- 加短代码 `{{< page-hero kicker="..." subtitle="..." eyebrow="..." title="..." >}}`，所有 section 主页（/start/, /notes/, /works/, /life/, /about/）统一调用
- 加短代码 `{{< section-rule >}}`（避免 goldmark 吞 HTML 的 ✦ 分隔符）
- 覆写 `layouts/_default/list.html`，section 主页全部走 page-hero 模式
- 5 个 `_index.md` 都加了 `kicker` / `subtitle` frontmatter
- 大幅扩充 `assets/css/custom.css`：新增 §21–§27 节，覆盖 prose / 面包屑 / article 列表卡 / TOC / footer / 单文章 hero / page-hero 等所有内页元素
- 打开 Goldmark `unsafe = true`，让 `<details>` 等不被吞

### Lucide icon 替换 emoji

- 扩充 `layouts/partials/cover/icon.html`：内联 Lucide SVG（手写，无 CDN 依赖）
- `data/modules.yaml` 和 `data/vault.yaml` 的 `icon` 字段从 emoji 改为 Lucide 名字
- 加新 icon：在 icon.html 加一个 `{{ else if eq $name "xxx" }}` 分支即可

### 代码块：单层框 + 行号与代码不分离

- `hugo.toml` 加 `lineNumbersInTable = false`，chroma 改用内联 `<span class="ln">` 输出行号
- `assets/css/custom.css §25` 把 `.highlight-wrapper / .highlight / .chroma` 全透明化，只在外层一个框；行号走 CSS counter 自增生成，紧贴代码左边一条 1px 浅线

### /start/ 模块卡：单列 + 居中 + 横向布局

- grid 改单列容器（max-width: 44rem, mx-auto）
- 模块卡用 grid 三列横向布局：左 icon（hover 旋转 -6° 变橙）/ 中 body / 右 CTA
- 移动端自动降级为 icon+body 一行、CTA 单独一行靠右

### 顶栏加 GitHub 项目按钮（明暗切换按钮右侧）

- 覆写 `layouts/partials/header/components/desktop-menu.html` 和 `mobile-menu.html`
- 链接 URL 来自 `data/cover.yaml` → `repo_url`（与封面 social 里的"个人 GitHub"区分开）
- 封面自动隐藏：因为 `body:has(.cover-page) .fixed.inset-x-0.z-100` 把整个顶栏藏掉了

### 封面主题切换按钮（封顶右上角，独立于顶栏）

- `layouts/partials/home/custom.html` 加 `<button id="appearance-switcher-cover">`
- 内联 JS：点击时转发到 `appearance-switcher` 按钮的 `.click()`，**100% 复用** appearance.js 的 localStorage / updateLogo / updateMermaidTheme
- 位置避开顶部 56px 黑色花边，`top: clamp(4.75rem, 7vh, 5.5rem)`

### 封面调色同步明暗主题

- `assets/css/custom.css §28` 加 `html.dark .cover-page { --pal-*: … }` 覆写
- 顶栏切了 dark → 封面也立刻变深；封面切 → 与全局保持一致
- 调色用 `E08769`（暗色版 accent）等 Claude 风暖白/暖黑对应色

### 项目地图文档

- 新建 `PROJECT_MAP.md` — 8 个章节 + 文件总览 + 最短修改路径速查表
- 想改任何东西，先查这份文档

### 关键文件清单（本次）

| 类型 | 路径 |
|---|---|
| 新增 | `layouts/shortcodes/page-hero.html`、`layouts/shortcodes/section-rule.html` |
| 新增 | `layouts/partials/cover/page-hero.html` |
| 覆写 | `layouts/_default/list.html` |
| 覆写 | `layouts/partials/home/custom.html` |
| 覆写 | `layouts/partials/header/components/desktop-menu.html` |
| 覆写 | `layouts/partials/header/components/mobile-menu.html` |
| 覆写 | `layouts/shortcodes/modules-grid.html`、`layouts/shortcodes/vault-sections.html` |
| 大改 | `layouts/partials/cover/icon.html`（Lucide SVG 字典） |
| 大改 | `assets/css/custom.css`（§21–§28 新增） |
| 大改 | `data/modules.yaml`、`data/vault.yaml`、`data/cover.yaml` |
| 调整 | `content/start/_index.md`、`content/notes/_index.md`、`content/works/_index.md`、`content/life/_index.md`、`content/about/_index.md` |
| 大改 | `content/notes/docs/example.md`（md 样式测试样章，14 大节） |
| 文档 | `PROJECT_MAP.md` |

### 后续待办

- 中英语言切换按钮
- /works/ /life/ 实际内容填充
- 进一步细化封面 hero
- 全站搜索框样式

---

## 2026-06-19 · 封面调色跟随暗色模式（CSS specificity 修复）

### 问题

- 封面页右上角主题切换按钮点击后，**底层**（其他页面的 `<html>.dark`）确实切换了，但**封面本身**没变化
- 原因：封面调色板走的是 inline `style="--pal-*: ..."`（specificity `1,0,0,0`），比 `html.dark .cover-page { ... }`（specificity `0,2,0`）高，inline 永远赢

### 修复

- [layouts/partials/home/custom.html](file:///f:/Notes/layouts/partials/home/custom.html)：把 inline `style="--pal-*: ..."` 换成 `<style>.cover-page { --pal-*: ... }</style>` 块
- `<style>` 块里 `.cover-page` 是 `0,1,0`，比 `html.dark .cover-page` `0,2,0` 低，暗色覆写稳定生效
- [assets/css/custom.css §28](file:///f:/Notes/assets/css/custom.css#L1543-L1567) 保留，覆写深色 `--pal-*`

### 验收

- 封面点切换 → 封面背景渐变 + 标题 + 副标题 + 按钮边框 + social 全部跟着切
- 顶栏点切换 → 同样，封面立刻变深
- 跳到任意内页 → 主题保持一致

---

## 2026-06-19 · Phase A 内容迁移 + 部署准备

### 决策（与用户确认）

| 项 | 决定 |
|---|---|
| Tools | 写一个汇总页（不写文档的话就只能下载；脚本本身即说明） |
| Demo/AIpython | 文件树形式（不展示全部内容），可折叠，点击下载 |
| Minecraft 资源 | 全部迁，下载链接可用 |
| URL 策略 | 中文 → 英文 slug |

### 一次性迁移脚本

- [scripts/migrate-vault.ps1](file:///f:/Notes/scripts/migrate-vault.ps1) — 幂等（已存在的 bundle 跳过），可重复运行
- 把 `/Vault/{Docs,Language,Demo&&Resources,Tools}` 同步到 `content/notes/<section>/<slug>/index.md` + `static/notes-assets/<section>/...`

### 产出统计

- **24 篇 leaf bundle**（15 Docs + 6 Language + 3 Demo）
- **~50+ .cpp 模板**随 Language 章节进入 `code/` 子目录
- **2 个 PDF** 资源拷入 Language cpp-data-structures
- **完整 Minecraft 资源**（datapacks / skins / music / src / resourcepacks 的 zip）→ `static/notes-assets/demo/minecraft/`
- **40+ 个 Python 学习脚本** → `static/notes-assets/demo/aipython/`
- **Tools 全部脚本** → `static/notes-assets/tools/`
- 排除：`.venv` / `__pycache__` / `.idea` / `.git`

### 新增短代码

- [layouts/shortcodes/file-tree.html](file:///f:/Notes/layouts/shortcodes/file-tree.html) — 把 `/static/<root>` 渲染为可折叠文件树（递归 `<details>` + 文件下载链接）
- [assets/css/custom.css §29](file:///f:/Notes/assets/css/custom.css#L1624-L1700) — file-tree 样式（衬线 summary、虚线缩进、accent 色 chevron 旋转）

### 合成页面（无 .md 时手写索引）

- [content/notes/demo/aipython/index.md](file:///f:/Notes/content/notes/demo/aipython/index.md) — Python 入门练习文件树
- [content/notes/tools/index.md](file:///f:/Notes/content/notes/tools/index.md) — 工具脚本文件树
- [content/notes/docs/_index.md](file:///f:/Notes/content/notes/docs/_index.md)、language/、demo/ — 各 section landing

### 文件夹 → Slug 映射（关键）

| 原 Vault 文件 | 站点 URL |
|---|---|
| `Docs/宿舍WLAN修复.md` | `/notes/docs/wifi-dorm-fix/` |
| `Docs/Docker/docker-Dify.md` | `/notes/docs/docker-dify/` |
| `Docs/WSL2/Hermes/hermes-agent.md` | `/notes/docs/wsl2-hermes-agent/` |
| `Language/C++Algorithm/basic C++/C++算法NOTE.md` | `/notes/language/cpp-algo-notes/` |
| `Demo&&Resources/Minecraft/datapacks/note/notes.md` | `/notes/demo/minecraft-datapacks-notes/` |
| `Demo&&Resources/AIpython/.../*.py` | `/notes-assets/demo/aipython/<chapter>/<file>.py` |

### 已知小坑（已修复）

- PowerShell 模板里 SearchReplace 会吞换行 → 整脚本改用一次 Write 写入
- Hugo `readDir` 走相对 Hugo 项目根，传绝对路径会读到根目录的 LICENSE / DONE.md → 改成 `static/<root>`
- Hugo `fileExists` 在 Windows 上对正斜杠不稳定 → 改用 `readDir | default slice` + `len > 0` 判断
- example.md 和新建的 docs/ 子目录冲突 → 移到 `content/start/style-test/index.md`

### 后续

- /works/ /life/ 页面实际内容（暂时占位）
- 中英切换（i18n）
- 高级感 UI（Phase B）

---

## 2026-06-19 · Vault 文件夹结构 1:1 还原到站点

### 用户反馈

> 网页上的各个文章的层级 能不能按照Vault来 不要全部把子笔记摊开一起展示可以吗？ 文件结构最好就都按照Vault中的来。

### 行动

- 上一版的扁平 leaf bundle（`docs/docker-dify/` 等）→ 嵌套结构（`docs/docker/docker-dify/` 等）
- 17 个 section landing 页（`docs/`、`docs/docker/`、`language/cpp-algorithm/` 等）—— 每个有 kicker / subtitle
- **结果**：URL 反映 Vault 层级结构，浏览时按 Vault 分类展开

### 新 URL 结构（部分）

```
/notes/docs/                               → Docs 入口
/notes/docs/wifi-dorm-fix/                 → 宿舍 WLAN 修复（根级）
/notes/docs/docker/                        → Docker 分类
/notes/docs/docker/docker-dify/            → docker-Dify
/notes/docs/wsl2/                          → WSL2 分类
/notes/docs/wsl2/fix/                      → WSL2 Fix 子分类
/notes/docs/wsl2/fix/wsl2-vmware-fix/      → VMware 关机修复
/notes/docs/wsl2/hermes/wsl2-hermes-agent/ → Hermes Agent
/notes/docs/wsl2/opencode/wsl2-opencode/   → Opencode Agent
/notes/language/cpp-algorithm/             → C++ Algorithm 入口
/notes/language/cpp-algorithm/basic-cpp/   → C++ 基础算法
/notes/language/cpp-algorithm/basic-cpp/algo-notes/  → C++ 算法 NOTE
/notes/language/python/python-note/pycharm/          → Pycharm 笔记
/notes/demo/minecraft/                     → Minecraft 入口
/notes/demo/minecraft/patpat-wiki/         → PatPat Wiki
/notes/demo/aipython/                      → AI Python 入门（file tree）
/notes/tools/                              → 工具脚本（file tree）
```

### 新增 / 修改文件

- [scripts/restructure-folders.ps1](file:///f:/Notes/scripts/restructure-folders.ps1) — 把扁平 bundle 移到嵌套位置 + 生成 _index.md
- [scripts/full-rebuild.ps1](file:///f:/Notes/scripts/full-rebuild.ps1) — 完整重建所有 leaf bundle + image/ + code/ + PDF + section landing
- [scripts/fix-images.ps1](file:///f:/Notes/scripts/fix-images.ps1) — 补回被误删的 image/ 目录
- [scripts/add-bom.ps1](file:///f:/Notes/scripts/add-bom.ps1) — 给 PowerShell 脚本加 UTF-8 BOM（**绕开中文解析问题**）
- 各 `content/notes/<section>/<subsection>/_index.md`（17 个 landing 页）

### 踩过的坑（教训）

| 坑 | 原因 | 修法 |
|---|---|---|
| PowerShell 中文解析失败 | Windows PowerShell 不带 BOM 的 UTF-8 会把中文 hash value 当多个表达式 | `.ps1` 文件全部加 UTF-8 BOM（用 `add-bom.ps1`） |
| `$Content` 被同名局部变量覆盖 | `New-SectionIndex` 里 `$content = $lines -join "`n"` 覆盖了全局 `$Content` | 改成 `$frontmatter = ...` 避免撞名 |
| cleanup 删了空 image/ → 进而删了整个 bundle | `Remove-EmptyDirs` 太激进，把没文件但子目录也被认作空 | 删除逻辑改成 `Get-ChildItem -Recurse -File | Where-Object` 全局判断 |

### 后续

- 中英切换（i18n）
- /works/ /life/ 页面实际内容（暂时占位）
- 高级感 UI（Phase B）

---

## 2026-06-19 · 首次部署上线 + 仓库清理

### 部署到 Cloudflare Pages

- 在 Cloudflare Pages 创建项目，连接 GitHub repo `lyrumu/knowledge-base`
- 构建配置：Framework preset **Hugo**，Build command `hugo --minify --themesDir themes --theme blowfish --config hugo.toml`，输出目录 `/public`
- 环境变量 `HUGO_VERSION = 0.163.2`（Cloudflare 默认 Hugo 0.147.7 不够，Blowfish 需要 0.163.2）
- tag `v1.0.0` 标记首次部署
- 网站地址：`https://knowledge-base-85b.pages.dev`

### 仓库清理

- `copilot/`、`Raw information/`、`DONE.md`、`PROJECT_MAP.md` → 从 git 移除跟踪（`git rm --cached`），加入 `.gitignore`，本地保留
- 旧 `cloudflare-pages.yml` workflow 已删除（改用 Cloudflare Pages Git 集成，不需要 GitHub Actions）
- `.gitignore` 增加 `Vault/`、`site/`、`copilot/`、`Raw information/`、`DONE.md`、`PROJECT_MAP.md` 等排除项

### 文档更新

- 新增 [DEPLOY.md](file:///f:/Notes/DEPLOY.md) — 部署与维护指南（日常更新流程、架构速查、故障排查）
- [README.md](file:///f:/Notes/README.md) — 追加 Website 章节，描述网站部署信息
- [PROJECT_MAP.md](file:///f:/Notes/PROJECT_MAP.md) — 更新部署方式和文件结构

### 后续

- 零配置 vault-to-hugo 脚本编写（自动发现 Vault 中所有 .md 文件）
- GitHub Actions 全自动化部署
- /works/ /life/ 内容填充
- 中英切换（i18n）
- 高级感 UI（Phase B）
