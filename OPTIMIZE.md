# OPTIMIZE.md — f:\Notes 项目优化方案

> **维护规则**：每次完成一大阶段开发后更新；新需求先查本文件再动手。
> **边界**：本文件与 `DONE.md`（已完成清单）、`PROJECT_MAP.md`（项目地图）互补，不重复记录历史。
> **原则**：以代码为准 — 文档与代码不一致时改文档；DONE.md 历史记录不改。
>
> ！！！工作流程：从文档挑目前最适合开始的一个工作 ->和我讨论详细方案 优化后的效果->你动手 我验收->更新优化文档->下一个任务(循环)

***

## 0. 文档元信息

| 项       | 值                                                 |
| ------- | ------------------------------------------------- |
| 创建时间    | 2026-06-25                                        |
| Hugo 版本 | v0.163.2                                          |
| 主题      | Blowfish v2                                       |
| 部署      | Cloudflare Pages                                  |
| 域名      | lyrumu.top                                        |
| baseURL | `https://lyrumu.top/`                             |
| 内容源     | Obsidian Vault（手动上架，不自动同步）                        |
| 字体本地化   | ✓ 已完成                                             |
| 动画库 CDN | AOS / Splitting / VanillaTilt + aos.css（**待本地化**） |

***

## 1. 现状摘要

| 维度         | 现状                                                                                   |
| ---------- | ------------------------------------------------------------------------------------ |
| 顶栏导航       | 4 项 `[[menu.main]]`：ABOUT ME / DOCS / WORKS / DAILY                                  |
| Section 主页 | 5 个 `_index.md`：cover / about / notes / works / life                                 |
| 子页         | 4 个 `_index.md`：works/{projects,resources,tools} + life/music                        |
| 文章         | 17 篇 vault 笔记（含 linux-getting-started / python-env-setup 等）                          |
| 数据驱动       | 7 个 yaml（cover / vault / life / music / works / projects / resources）+ 1 个废（modules） |
| Shortcode  | 9 个在用 + 1 个 dead（vault-sections）+ 1 个废（modules-grid）                                 |
| Layout 模板  | page.html 在用 + list.html 备用 + home.html 走 custom.html partial                        |
| CSS        | 9 个 `_*.css` + custom.css 索引；`_05_cards.css` 已 1041 行（临界）                            |

***

## 2. 已验证事实（写文档时的探测结果）

### 2.1 canonical / sitemap 验证

通过读 `public/`（最近一次 `hugo server --port 8080` 产物）：

| 验证项                           | 结果                                       |
| ----------------------------- | ---------------------------------------- |
| `hugo.toml` baseURL           | `https://lyrumu.top/` ✓                  |
| `hugo server` 产物的 canonical   | `http://localhost:8080/...`（server 强制覆盖） |
| `hugo --minify` 产物的 canonical | **未本地生成，需部署后验证**                         |
| sitemap.xml 来源                | Hugo 自动从 baseURL 生成                      |

**结论**：baseURL 配置正确；`public/` 里的 localhost URL 是 `hugo server` 副作用，不影响线上。

**部署后验证命令**：

```bash
curl -s https://lyrumu.top/ | grep -i canonical
# 期望：<link rel="canonical" href="https://lyrumu.top/">

curl -s https://lyrumu.top/sitemap.xml | head -10
# 期望：<loc>https://lyrumu.top/...</loc>

curl -s https://lyrumu.top/about/ | grep -i 'og:url'
# 期望：<meta property="og:url" content="https://lyrumu.top/about/">
```

### 2.2 dead code 完全确认

| 文件                                       | 引用方                                                            | 完全无用？                    |
| ---------------------------------------- | -------------------------------------------------------------- | ------------------------ |
| `data/modules.yaml`                      | 仅 `data/vault.yaml` / `modules-grid.html` / 文档互相引用；layouts/ 不读 | ✓ 删                      |
| `layouts/shortcodes/modules-grid.html`   | content/ **0 调用**；layouts/ 只在自己内部                              | ✓ 删                      |
| `layouts/shortcodes/vault-sections.html` | content/ **0 调用**                                              | ✓ 删                      |
| `data/vault.yaml`                        | 仅 `vault-sections.html` + 文档引用                                 | ✓ 删（与 vault-sections 联动） |
| `.vault-section-*` CSS 规则                | 仅 `vault-sections.html` 用                                      | ✓ 删（与 vault-sections 联动） |
| `layouts/_default/list.html`             | **0 个 .md 显式调用**                                               | ✗ 保留备用（顶部加注释）            |

**确认命令**（写文档时跑过，未来想再验证可重跑）：

```bash
# vault-sections 完全无 .md 调用
grep -rn "vault-sections" content/   # → 0 matches

# data/vault.yaml 完全无 layouts 读取
grep -rn "hugo.Data.vault\|data/vault" layouts/  # → 0 matches (除 shortcode 自己)

# modules-grid 同理
grep -rn "modules-grid" content/     # → 0 matches
grep -rn "hugo.Data.modules\|data/modules" layouts/  # → 0 matches
```

### 2.3 SEO description 机制（重要事实）

- Hugo frontmatter `description:` 字段 → **只渲染到** **`<meta>`** **标签**
- **不会渲染到 HTML body**（不在网页正文里显示）
- 这是 Hugo 默认行为，无需额外代码
- 如果 `description:` 为空，Hugo 自动从正文首段提取（用 summary 机制）
- `og:description` 和 `twitter:description` 也自动从 `description:` / `summary` 取

**所以 description 只让浏览器/爬虫可见、网页上不可见是默认行为** — 只需补 `description:` 字段。

### 2.4 CDN 资源清单

[layouts/partials/extend-head.html](file:///f:/Notes/layouts/partials/extend-head.html) 引入：

| 资源                  | URL                                                                | 用途     | 大小          |
| ------------------- | ------------------------------------------------------------------ | ------ | ----------- |
| aos.css             | `cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.css`                      | 滚动入场淡入 | \~26 KB     |
| splitting.min.js    | `cdn.jsdelivr.net/npm/splitting@1.0.6/dist/splitting.min.js`       | 字符级分割  | \~4 KB      |
| aos.js              | `cdn.jsdelivr.net/npm/aos@2.3.4/dist/aos.js`                       | 滚动入场淡入 | \~15 KB     |
| vanilla-tilt.min.js | `cdn.jsdelivr.net/npm/vanilla-tilt@1.8.1/dist/vanilla-tilt.min.js` | 3D 倾斜  | \~9 KB      |
| **总计**              | —                                                                  | —      | **\~54 KB** |

**风险**：SRI 锁版本 → npm republish 时 hash 变 → CDN 拒载；国内访问速度不稳。

***

## 3. 关键概念展开

### 3.1 三种 layout 的实际分工

| layout       | 用在                               | Hugo 找的模板                        | 实际渲染                                |
| ------------ | -------------------------------- | -------------------------------- | ----------------------------------- |
| `background` | 仅 `content/_index.md`（封面）        | home.html → fallback baseof.html | `layouts/partials/home/custom.html` |
| `page`       | 9 个 `_index.md`（section 主页 + 子页） | `layouts/page.html`（项目级）         | ✓                                   |
| 隐式（不写）       | 17 篇笔记（single page）              | 主题的 `_default/single.html`       | ✓                                   |

[layouts/\_default/list.html](file:///f:/Notes/layouts/_default/list.html) 写了 100+ 行但 0 个 .md 显式调用 → 保留备用。

### 3.2 当前架构优劣（page + 短代码）

| 优势                                      | 劣势                                   |
| --------------------------------------- | ------------------------------------ |
| 灵活——每个 section 用不同 shortcode            | 重复——5 个 `_index.md` 都写相同 frontmatter |
| page.html 简洁                            | list.html 写了 100+ 行但完全没人用            |
| 子页面有自定义 frontmatter 时不需要 list.html 自动列表 | 新人不知道 list.html 的存在                  |
| 短代码可复用、可重排                              | 5 个页面都要写 `{{< xxx-grid >}}`          |

**当前架构保留**——它能工作、灵活。

### 3.3 shortcode 一览表

| shortcode        | 文件                               | 数据源                   | 调用方                                 | 状态    |
| ---------------- | -------------------------------- | --------------------- | ----------------------------------- | ----- |
| `section-rule`   | `shortcodes/section-rule.html`   | 无                     | 各 `_index.md`                       | ✓     |
| `page-hero`      | `shortcodes/page-hero.html`      | frontmatter           | list.html / page.html 通过 partial    | ✓     |
| `about-contact`  | `shortcodes/about-contact.html`  | partial 内部            | `content/about/_index.md`           | ✓     |
| `life-grid`      | `shortcodes/life-grid.html`      | `data/life.yaml`      | `content/life/_index.md`            | ✓     |
| `works-grid`     | `shortcodes/works-grid.html`     | `data/works.yaml`     | `content/works/_index.md`           | ✓     |
| `projects-list`  | `shortcodes/projects-list.html`  | `data/projects.yaml`  | `content/works/projects/_index.md`  | ✓     |
| `resources-list` | `shortcodes/resources-list.html` | `data/resources.yaml` | `content/works/resources/_index.md` | ✓     |
| `music-list`     | `shortcodes/music-list.html`     | `data/music.yaml`     | `content/life/music/_index.md`      | ✓     |
| `file-tree`      | `shortcodes/file-tree.html`      | 文件系统                  | markdown 手写                         | ✓     |
| `vault-sections` | `shortcodes/vault-sections.html` | `data/vault.yaml`     | **无人调用**                            | ⚠️ 待删 |
| `modules-grid`   | `shortcodes/modules-grid.html`   | `data/modules.yaml`   | **无人调用**                            | ☠️ 待删 |

> 注：用户配置里的 `{{< icon >}}` 实际是 `partial "cover/icon.html"`，不是 shortcode。

### 3.4 partial 一览表

| partial                               | 文件                                                     | 用途                                                   |
| ------------------------------------- | ------------------------------------------------------ | ---------------------------------------------------- |
| `head.html`                           | `layouts/partials/head.html`                           | 覆写主题版本；CSS 用 `resources.Match + Concat` 不用 `@import` |
| `cover/icon.html`                     | `layouts/partials/cover/icon.html`                     | Lucide SVG 字典                                        |
| `cover/page-hero.html`                | `layouts/partials/cover/page-hero.html`                | 内页"小封面"                                              |
| `home/custom.html`                    | `layouts/partials/home/custom.html`                    | 封面 partial                                           |
| `header/basic.html`                   | `layouts/partials/header/basic.html`                   | 覆写主题版本（主入口渲染）                                        |
| `header/components/desktop-menu.html` | `layouts/partials/header/components/desktop-menu.html` | 覆写 + GitHub 按钮                                       |
| `header/components/mobile-menu.html`  | `layouts/partials/header/components/mobile-menu.html`  | 覆写 + GitHub 按钮                                       |
| `extend-head.html`                    | `layouts/partials/extend-head.html`                    | 第三方 CDN 资源 + 动画库初始化                                  |
| `music-player.html`                   | `layouts/partials/music-player.html`                   | 粘性音乐播放器 HTML                                         |
| `about-contact.html`                  | `layouts/partials/about-contact.html`                  | iOS 液态玻璃联系方式图标卡                                      |

**主题已覆写但需关注升级的文件**：

- `themes/blowfish/layouts/_default/baseof.html`（\[lyrumu 改造] 段）— 升级时重贴
- `themes/blowfish/layouts/partials/head.html`（被项目级覆盖）— 升级时优先看 \[lyrumu 改造]

***

## 4. 用户决策记录

| #   | 决策                                                         | 时间         | 状态    |
| --- | ---------------------------------------------------------- | ---------- | ----- |
| D1  | /notes/ 入口：直接显示文章列表，不用 vault 分类                            | 2026-06-25 | ✅ 已决策 |
| D2  | canonical / sitemap：部署后手动验证一次                              | 2026-06-25 | ✅ 已决策 |
| D3  | CDN 资源：全部本地化                                               | 2026-06-25 | ✅ 已决策 |
| D4  | SEO description：只让浏览器/爬虫可见，网页上不可见（**默认行为，无需 hack**）        | 2026-06-25 | ✅ 已决策 |
| D5  | 死代码：完全确认无用才删                                               | 2026-06-25 | ✅ 已决策 |
| D6  | 站点统计：S1 极简 Hugo 内置                                         | 2026-06-25 | ✅ 已决策 |
| D7  | vault 同步脚本：手动上架，不需要自动同步                                    | 2026-06-25 | ✅ 已决策 |
| D8  | 文档与代码不一致：以代码为准                                             | 2026-06-25 | ✅ 已决策 |
| D9  | list.html：保留 + 顶部加「备用」注释                                   | 2026-06-25 | ✅ 已决策 |
| D10 | modules.yaml + modules-grid.html：完全确认无用，可删                 | 2026-06-25 | ✅ 已决策 |
| D11 | vault-sections.html + data/vault.yaml：完全确认无用（grep 0 调用），可删 | 2026-06-25 | ✅ 已决策 |
| D12 | vault.yaml 删 → DEPLOY.md / PROJECT\_MAP.md 同步改             | 2026-06-25 | ✅ 已决策 |
| D13 | /notes/ 入口：list.html 默认行为 + cardColumns frontmatter（修正方案）| 2026-06-25 | ✅ 已决策 |
| D14 | dead code 清理：4 文件删除 + 共享 CSS 标签块 bug fix             | 2026-06-25 | ✅ 已决策 |
| D15 | CDN 本地化：4 个资源下载到 static/ + extend-head.html 改本地    | 2026-06-25 | ✅ 已决策 |
| D16 | 文档对齐 + scripts/ 冻结：PROJECT_MAP / DEPLOY / scripts/README | 2026-06-25 | ✅ 已决策 |
| D17 | 站点统计 S1：新建 site-stats shortcode + about 末尾调用 + CSS | 2026-06-25 | ✅ 已决策 |
| D18 | description 补全：8 个 _index.md 加英文 SEO description     | 2026-06-25 | ✅ 已决策 |
| D19 | 自定义 404 页：layouts/404.html + baseof.html / 404.html 2 个 bug fix | 2026-06-25 | ✅ 已决策 |
| D20 | llms.txt 启用：static/llms.txt（AI 爬虫友好）             | 2026-06-25 | ✅ 已决策 |

***

## 5. 优化方案（详细）

### 5.1 /notes/ 入口页改造（D1）

**当前**：[content/notes/\_index.md](file:///f:/Notes/content/notes/_index.md) 只写 `> ⏳ Under construction...`，17 篇笔记无可见入口。

**方案 A（推荐）**：新增 `notes-list` shortcode

1. 新建 [layouts/shortcodes/notes-list.html](file:///f:/Notes/layouts/shortcodes/notes-list.html)：
   ```go
   {{/*
     Shortcode: notes-list
     ----------------------------------------------------------------
     渲染 content/notes/ 下所有 leaf bundle 为卡片网格
     按日期倒序；样式复用主题 article-link/card.html
   */}}
   <div class="notes-list-grid not-prose my-10">
     {{ range (where .Site.RegularPages "Section" "notes").ByDate.Reverse }}
       {{ partial "article-link/card.html" . }}
     {{ end }}
   </div>
   ```
2. 改 [content/notes/\_index.md](file:///f:/Notes/content/notes/_index.md)：
   ```yaml
   ---
   title: "DOCS"
   kicker: "NOTES · MODULE 01"
   subtitle: "Vault 驱动的学习笔记合集"
   description: "环境配置、算法、Demo 资源、工具脚本 — 全部基于 Obsidian Vault"
   layout: "page"
   showHero: true
   showBreadcrumbs: true
   showTableOfContents: true
   ---

   {{< section-rule >}}

   {{< notes-list >}}
   ```
3. CSS：复用主题的 `article-link/card.html` 样式；如需微调，在 `_05_cards.css` 加 `.notes-list-grid` 调整间距。

**方案 B**：改用 `layout: "list"` 调 list.html — 风险：要改 list.html 处理空子页面场景；会牵动其他页面。

**推荐 A** — 不破坏现有架构。

### 5.2 canonical / sitemap 部署后验证（D2）

无需代码改动。部署到 Cloudflare Pages 后跑 §2.1 的 3 条 curl 命令。

### 5.3 CDN 本地化（D3）

| 步骤 | 动作                                                                                                             |
| -- | -------------------------------------------------------------------------------------------------------------- |
| 1  | 下载 4 个文件到 `static/css/aos.css`、`static/js/{aos,splitting,vanilla-tilt}.js`                                     |
| 2  | 改 [extend-head.html](file:///f:/Notes/layouts/partials/extend-head.html)：CDN URL → 本地 `/css/aos.css` `/js/...` |
| 3  | 删除 SRI integrity + crossorigin（本地资源不需要）                                                                        |
| 4  | 验证：F12 → Network 面板，4 个资源都从同源加载                                                                                |

**对比**：

| 维度   | CDN                        | 本地化          |
| ---- | -------------------------- | ------------ |
| 外部依赖 | jsDelivr                   | 0            |
| 失效风险 | SRI 锁版本 → npm republish 时挂 | 无            |
| 国内访问 | 不稳                         | 极快           |
| 升级库  | 重新算 hash + 改 4 处           | 替换文件 + 改 1 处 |

### 5.4 SEO description 补全（D4）

机制：frontmatter `description:` → 只渲染到 `<meta>` 标签（默认行为，无需 hack）。

**9 个** **`_index.md`** **待补**：

```yaml
# content/_index.md（封面）
description: "lyrumu's personal page — Student · Developer · Hangzhou"

# content/about/_index.md
description: "About lyrumu — Student · Developer in Hangzhou, China"

# content/notes/_index.md
description: "Vault 驱动的学习笔记：环境配置、算法、Demo 资源、工具脚本"

# content/works/_index.md
description: "我的作品：项目（vibe coding、demo）、可下载资源、工具脚本"

# content/life/_index.md
description: "生活记录：音乐歌单、图片、思想"

# content/works/projects/_index.md
description: "个人项目：vibe coding、demo、实验作品"

# content/works/resources/_index.md
description: "可下载资源：Minecraft 资源包、字体、脚本"

# content/works/tools/_index.md
description: "工具与脚本合集"

# content/life/music/_index.md
description: "我的歌单：Departures、Unravel、黑色幽默...(不定期更新)"
```

**撰写原则**：60-160 字符，包含核心关键词，不堆砌不重复 title。

### 5.5 dead code 删除（D5/D10/D11）

**确认已 100% 无用**（grep 0 调用）：

```bash
# 写文档时的验证结果
grep -rn "vault-sections" content/   # → 0 matches
grep -rn "hugo.Data.vault" layouts/  # → 0 matches (除 shortcode 自己)
grep -rn "modules-grid" content/     # → 0 matches
grep -rn "hugo.Data.modules" layouts/# → 0 matches (除 shortcode 自己)
```

**删除清单**：

| # | 文件                                                   | 删除原因                |
| - | ---------------------------------------------------- | ------------------- |
| 1 | `data/modules.yaml`                                  | 完全无用                |
| 2 | `layouts/shortcodes/modules-grid.html`               | 完全无用                |
| 3 | `layouts/shortcodes/vault-sections.html`             | 完全无用                |
| 4 | `data/vault.yaml`                                    | 与 vault-sections 联动 |
| 5 | `_05_cards.css` 中 `.vault-section-*` 规则（约 L240-L310） | 与 vault-sections 联动 |

**同步更新文档**：

- `PROJECT_MAP.md §3`：删除 5 行
- `PROJECT_MAP.md §2`：删除"换 /notes/ 分类卡 → data/vault.yaml"行
- `PROJECT_MAP.md §4`：删除 vault-section-card 描述行
- `DEPLOY.md L109`：修正"在 data/vault.yaml 中添加 section 定义"为"在 content/notes/\_index.md 中加 shortcode"

### 5.6 list.html 处置（D9）✅ 已修正（2026-06-25）

**之前判断**：list.html "0 调用"，保留备用 → **错了**。

**实际情况**：list.html 是 section 主页的核心模板，所有 8 个 section `_index.md` 都走它（默认 list kind）。

**当前状态**：
- 顶部已有注释（标记为"核心"，不是"备用"）
- 2026-06-25 加 `cardColumns` frontmatter 开关
- 2026-06-25 加 `showChildList` 开关（如未来需要关闭自动子页面渲染）

**不再做**：
- ~~加"备用"注释~~
- ~~删除 list.html~~

```go
{{/*
  _default/list.html — Claude 风覆写版（备用，2026-06-25 起主流程不再使用）
  ----------------------------------------------------------------
  当前所有 section _index.md 都用 layout: "page" + 手动 shortcode 驱动
  本文件保留以备未来场景（如 /archive/ 时间倒序全部文章 / 按 tag 聚合列表）
  渲染逻辑保留：page-hero + 面包屑 + 子页面卡片网格

  ⚠️ 不要删除本文件 — 升级 Blowfish 时不要被主题版本覆盖
  ⚠️ 启用前确认没有与 page.html 冲突的 frontmatter 处理
*/}}
```

### 5.7 站点统计 S1 极简（D6）

**位置**：`/about/` 末尾

**实现**：在 `content/about/_index.md` 末尾（GitHub 热力图下方）加：

```html
{{< section-rule >}}

<section class="site-stats">
  <span class="site-stats-item">
    <span class="site-stats-num">{{ len (where .Site.RegularPages "Section" "notes") }}</span>
    <span class="site-stats-label">篇笔记</span>
  </span>
  <span class="site-stats-sep">·</span>
  <span class="site-stats-item">
    <span class="site-stats-num">{{ len .Site.Taxonomies.tags }}</span>
    <span class="site-stats-label">个标签</span>
  </span>
  <span class="site-stats-sep">·</span>
  <span class="site-stats-item">
    <span class="site-stats-label">最近更新</span>
    <span class="site-stats-num">
      {{- with (where .Site.RegularPages "Section" "notes").ByDate.Reverse | first 1 -}}
        {{- .Format "2006-01-02" -}}
      {{- end -}}
    </span>
  </span>
</section>
```

**CSS**：在 `_09_about.css` 加 `.site-stats` 样式（衬线斜体小字，与 about 风格一致）。

**优点**：零依赖、零隐私问题、build 时计算。

### 5.8 scripts/ 目录冻结标记（D7）

在 `scripts/` 目录新建 `README.md`：

```markdown
# scripts/ — 历史遗留脚本（已冻结）

⚠️ 本目录所有脚本已于 2026-06-25 起标记为"冻结不维护"。

## 原因
未来新增内容改为手动上架（直接编辑 content/ 和 data/），不再自动同步。

## 脚本清单
| 脚本 | 最后用途 | 状态 |
|---|---|---|
| vault-to-hugo.ps1 | Vault → Hugo 同步 | 冻结 |
| migrate-vault.ps1 | 一次性内容迁移 | 历史完成 |
| restructure-folders.ps1 | 目录重构 | 历史完成 |
| full-rebuild.ps1 | 完整重建 | 历史完成 |
| fix-images.ps1 | 修复 image 目录 | 历史完成 |
| add-bom.ps1 | UTF-8 BOM 处理 | 历史完成 |
| test-*.ps1 | 测试脚本 | 历史完成 |
| fix-lines.ps1 | 行修复 | 历史完成 |

## 保留原因
- 可能需要回退参考
- vault 目录仍然在本地，仅不再自动同步

## 删除时机
确认不再需要回退时，可整体删除 scripts/ 目录。
```

同时给 `vault-to-hugo.ps1` 顶部加显眼注释：`⚠️ 已冻结 — 2026-06-25`。

### 5.9 文档对齐（D8/D12）

| 文档位置                                                 | 现状                      | 修正                                          |
| ---------------------------------------------------- | ----------------------- | ------------------------------------------- |
| PROJECT\_MAP.md §2 "换 /notes/ 分类卡 → data/vault.yaml" | 错误（vault.yaml 没人调）      | 改为"改 /notes/ 入口 → content/notes/\_index.md" |
| PROJECT\_MAP.md §3 文件结构                              | 含 `vault-sections.html` | 删除                                          |
| PROJECT\_MAP.md §4 "vault-section-card"              | 含死 shortcode 描述         | 删除或重写为"已删除"                                 |
| PROJECT\_MAP.md §3 "modules.yaml"                    | 已标记 dead code 但仍在目录树    | 整段删除                                        |
| DEPLOY.md L109 "在 data/vault.yaml 中添加 section"       | 错误                      | 改为"在 content/notes/\_index.md 中加 shortcode" |
| DEPLOY.md 顶部"添加 vault 分类"章节                          | 已过时                     | 删除或重写                                       |

DONE.md **不修改**——历史就是历史。

### 5.10 顺手可做（其他修复）

| # | 事项                                   | 工作量   | 备注                                        |
| - | ------------------------------------ | ----- | ----------------------------------------- |
| 1 | 修 "REOURCES" 拼写                      | 1 分钟  | `content/works/resources/_index.md` 第 2 行 |
| 2 | 封面 social 加 Twitter / Bilibili / RSS | 5 分钟  | 待用户提供链接                                   |
| 3 | 自定义 404 页                            | 30 分钟 | 含搜索框 + 推荐                                 |
| 4 | 自定义 favicon（明暗双套）                    | 15 分钟 | 视觉品牌                                      |
| 5 | DEPLOY.md 整体更新（清理历史 TODO）            | 30 分钟 | 与本文件交叉引用                                  |

***

## 6. 实施优先级（已完成决策）

### 🔴 立即可做（按依赖排序）

| 序号 | 事项 | 工作量 | 阻塞 | 状态 |
|---|---|---|---|---|
| 1 | /notes/ 入口改造（list.html cardColumns + card.html 覆写） | ~20 分钟 | 无 | ✅ 2026-06-25 完成 |
| 2 | 删 dead code（5 个文件：modules.yaml / modules-grid.html / vault.yaml / vault-sections.html / .vault-section-* CSS） | 5 分钟 | 无 | ✅ 2026-06-25 完成 |
| 3 | 修 REOURCES 拼写 | 1 分钟 | 无 | ✅ 已由用户修复（content/works/resources/_index.md 标题为 RESOURCES）|
| 4 | 9 个 `_index.md` 补 description | 15 分钟 | 用户提供文案 | ✅ 2026-06-25 完成（英文文案） |
| 5 | CDN 本地化（4 个资源到 static/） | 20 分钟 | 无 | ✅ 2026-06-25 完成 |
| 6 | PROJECT_MAP.md / DEPLOY.md 同步修正 | 15 分钟 | 2 | ✅ 2026-06-25 完成 |
| 7 | `scripts/` 加 README + 冻结标记 | 10 分钟 | 无 | ✅ 2026-06-25 完成 |
| 8 | 站点统计 S1（about 末尾 + CSS） | 20 分钟 | 无 | ✅ 2026-06-25 完成（修复 range bug） |
| **合计** | — | **~1.5 小时** | — | — |

**删除的方案**（之前误判，已撤掉）：
- ~~新增 `notes-list` shortcode~~ — 改用 list.html 默认行为
- ~~list.html 加"备用"注释~~ — list.html 是核心模板

***

## 7. 待讨论 / 待用户决策的方向

> 本节列出"用户没明确表态"的项目问题和优化方向。每项都是潜在改进，**留待用户主动提出需求后再展开具体方案**。

### 7.1 内容扩充

| 方向                | 现状                      | 决策点                                     |
| ----------------- | ----------------------- | --------------------------------------- |
| /life/ 增加第二个子模块   | 只有 music                | 加哪个？图片 / 读书 / 旅行 / 游戏                   |
| /works/tools/ 真内容 | "Under construction" 占位 | 走 file-tree（与 /notes/tools/ 重复）/ 重新做作品级 |
| 关于页 timeline      | 无                       | 学习里程碑 / 项目里程碑 / 兴趣发展                    |
| 关于页 读书清单          | 无                       | 站内展示还是外链（如 Goodreads）                   |
| 关于页 兴趣标签          | 有 but 简单                | 加更多维度（游戏 / 音乐类型 / 运动）                   |

### 7.2 功能扩展

| 方向               | 现状           | 决策点                      |
| ---------------- | ------------ | ------------------------ |
| 自定义 404 页        | 用主题默认        | 搜索框 / 推荐内容 / 引导回首页       |
| 自定义 favicon      | 用主题默认        | 明暗双套 / 单套 / 字符 logo      |
| PWA / manifest   | 无            | 是否做"添加到主屏幕"支持            |
| 标签 / 分类 / 主题索引页  | hugo 自动生成    | 是否覆写 term.html 套 site 风格 |
| /archive/ 全部文章列表 | 无            | 按时间倒序 / 按分类 / 按标签        |
| llms.txt         | 无            | 启用给 AI 爬虫用（Blowfish 已支持） |
| RSS reader 引导    | RSS 已配置但无 UI | 封面加 RSS 链接 / about 加订阅引导 |
| 全文搜索高亮           | 无            | 关键词高亮 / 搜索建议             |
| 图片优化             | lazy-load 启用 | webp / srcset / LQIP 预览  |
| 评论系统             | 无            | Giscus / Artalk / 不加     |

### 7.3 工程改进

| 方向                 | 现状           | 决策点                       |
| ------------------ | ------------ | ------------------------- |
| `_05_cards.css` 拆分 | 1041 行 6 类卡片 | 按用途拆 3-4 文件               |
| 自定义字体管理            | 已本地化         | unicode-range 优化（中文用衬线字体） |
| 备份策略               | 靠 git        | Vault 单独备份 / 增量备份         |
| GitHub Actions     | 无            | 构建测试 / 链接检查 / 死链扫描        |
| Hugo 版本管理          | 固定 0.163.2   | 是否锁定到具体 commit / 自动更新通知   |
| 依赖审计               | 无            | SRI 失效检测 / 第三方库版本监控       |

### 7.4 SEO / 性能 / 安全

| 方向         | 现状                  | 决策点                                                   |
| ---------- | ------------------- | ----------------------------------------------------- |
| 完整 SEO 方案  | 仅 OG / Twitter Card | JSON-LD 结构化数据（Article / BreadcrumbList / Person）      |
| 图片懒加载优化    | 默认开启                | LQIP 模糊预览 / IntersectionObserver 自定义                  |
| CSP 内容安全策略 | 无                   | 严格 CSP / report-only                                  |
| 域名 www 重定向 | 未知                  | lyrumu.top vs [www.lyrumu.top](http://www.lyrumu.top) |
| 性能预算       | 无                   | LCP < 2s / FID < 100ms / CLS < 0.1                    |
| 安全头        | Cloudflare 默认       | HSTS / X-Frame-Options / Referrer-Policy              |
| Sitemap 增强 | 自动生成                | 拆分子 sitemap / sitemap index                           |

### 7.5 UX 改进

| 方向       | 现状                        | 决策点                           |
| -------- | ------------------------- | ----------------------------- |
| 移动端体验    | 基础响应式                     | 触摸优化 / 抽屉菜单 / 滑动返回            |
| 暗色模式细节   | v3 统一调色板                  | 封面独立色板 / 主题色微调                |
| 键盘导航     | 默认                        | 快捷键 / 焦点环美化 / Skip to content |
| 无障碍 a11y | 部分                        | 完整 ARIA / 屏幕阅读器测试             |
| 错误处理     | 主题默认                      | 图片加载失败 / 404 推荐 / 离线页         |
| 阅读体验     | 衬线 + 滚动入场                 | 阅读进度条 / 字号调节 / 行距调节           |
| 暗模式手动覆盖  | autoSwitchAppearance=true | 提供"跟随系统 / 浅 / 深"三选一           |

### 7.6 内容工作流

| 方向              | 现状     | 决策点                         |
| --------------- | ------ | --------------------------- |
| 写作模板（archetype） | 默认     | 自定义 frontmatter 模板          |
| 图片管理            | 手动     | 命名规范 / 处理流程 / 压缩            |
| frontmatter 规范  | 各文件略不同 | 统一字段顺序 / 必填项                |
| 链接规范            | 混合     | 站内用相对路径 / 站外 target=\_blank |
| 标签 / 分类管理       | 自动     | 标签去重 / 分类层级                 |
| 内容审查            | 无      | 拼写检查 / 链接检查 / 风格统一          |

### 7.7 部署 / 运维

| 方向            | 现状    | 决策点                                           |
| ------------- | ----- | --------------------------------------------- |
| Cloudflare 配置 | 默认    | 缓存规则 / Rocket Loader / Polish 图片优化            |
| 域名邮箱          | 无     | Cloudflare Email Routing（<lyrumu@lyrumu.top>） |
| 监控            | 无     | UptimeRobot / Better Stack                    |
| 分析            | 无     | Umami / Plausible / Google Analytics          |
| 备份            | 靠 git | Vault / content / data 定期打包                   |
| 多环境           | 无     | preview 分支 / staging 环境                       |

### 7.8 内容策略

| 方向     | 现状                | 决策点                            |
| ------ | ----------------- | ------------------------------ |
| 写作频率   | 不定期               | 每周一篇 / 每月一篇 / 随缘               |
| 内容深度   | 教程 + 速查           | 增加观点文 / 教程重写                   |
| 国际化    | 仅中文（HTML lang=en） | 中英双语 / 仅中文改 lang               |
| 内容归档   | 无                 | 老文章标记 archived / 隐藏            |
| 内容交叉引用 | 手动                | 自动 related posts（Blowfish 已支持） |

***

## 8. 决策日志（每次决策追加一行）

```
2026-06-25  D1-D12  初版优化文档创建
             - /notes/ 入口改造方案 A（notes-list shortcode）
             - 死代码删除：modules.yaml / modules-grid.html / vault-sections.html / data/vault.yaml
             - list.html 保留备用
             - 站点统计 S1 极简
             - CDN 全部本地化
             - SEO description 补全
             - scripts/ 冻结标记
             - 文档以代码为准

2026-06-25  D13  /notes/ 入口改造完成（修正版）
             - 撤销方案 A（notes-list shortcode）
             - 实际方案：list.html 默认行为 + cardColumns frontmatter 控制
             - 同步覆写 article-link/card.html（全局关摘要）
             - 修正 OPTIMIZE.md 错误判断：list.html 不是 dead code（核心模板）
             - 修正 OPTIMIZE.md 错误判断：section _index.md 默认走 list.html
             - 修正 OPTIMIZE.md 错误数字：实际 3 篇笔记，非 17 篇

2026-06-25  D14  dead code 清理完成
             - 删除 4 个文件：data/modules.yaml, data/vault.yaml,
               layouts/shortcodes/modules-grid.html, layouts/shortcodes/vault-sections.html
             - _05_cards.css：删除 vault-section 整块（150 行）+ modules-grid-stack 容器（7 行）
             - _05_cards.css：更新顶部 + §15 块头注释（移除 dead 引用）
             - Bug fix：恢复 4 个共享标签样式块（life-sub-tag / works-sub-tag /
               project-card-tag / resource-card-tag），删除时连带删了导致 #demo 等
               标签失去药丸样式
             - 用户已修过 REOURCES 拼写（resources/_index.md 第 2 行是 RESOURCES）

2026-06-25  D15  CDN 本地化完成
             - 下载 4 个文件到 static/：css/aos.css (26KB), js/aos.js (14.7KB),
               js/splitting.min.js (3.7KB), js/vanilla-tilt.min.js (8.9KB)
             - extend-head.html：4 处 CDN URL → 本地路径，删除 SRI integrity +
               crossorigin + referrerpolicy
             - 注释更新：顶部说明 + L20 "defer CDN" → "defer"
             - 效果：零外部依赖；npm republish 时 hash 失效风险消失

2026-06-25  D16  文档对齐 + scripts/ 冻结
             - scripts/README.md 新建：冻结标记 + 11 个脚本清单 + 替代流程
             - scripts/vault-to-hugo.ps1 顶部加冻结警告
             - PROJECT_MAP.md：9 处更新（删 dead code 引用 / 修正 list.md 拼写错误 /
               加 frontmatter 开关表 / 加 /notes/ 手写 SOP / 更新目录结构）
             - DEPLOY.md 重写：v1.0.0 → v1.0.1（手写流程 + 删 vault.yaml 引用 +
               删 -Watch 命令 + 加新章节标记）

2026-06-25  D17  description 补全（SEO）
             - 8 个 _index.md 加 description 字段（英文文案）
             - cover / works / life / projects / resources / tools / music 子页
             - notes/_index.md 之前已加（保留）
             - about/_index.md 跳过（frontmatter 是 HTML 注释，hugo 自动用 summary 兜底）

2026-06-25  D19  自定义 404 页
             - 新建 layouts/404.html（衬线 + 罗马数字 DCCCIV + 5 个返回按钮）
             - _02_chrome.css 加 .not-found 样式（80 行）
             - Bug fix 1：baseof.html L14 注释 `<body>` → `body`（Hugo 解析器在 404
               路径下严格处理注释里的 `<`）
             - Bug fix 2：404.html `{{< section-rule >}}` 是 markdown 语法，不能在
               template 文件里用；改为内联 div
             - 文案全部英文（按规则"界面尽量保持英文"）

2026-06-25  D20  llms.txt 启用
             - 新建 static/llms.txt（hugo 直接复制到 public/，无需模板）
             - 内容：站点说明 + 4 大类（Docs / Works / Daily / About）链接
             - 维护规则：手动（加新文章时顺便更新）
             - 受益：AI 爬虫（Claude / GPT）友好，AI 引用站点内容时更准
```

***

## 9. 文档维护规则

| 规则   | 说明                                                |
| ---- | ------------------------------------------------- |
| 更新时机 | 完成一大阶段开发后；用户决策后                                   |
| 边界   | 本文件 = 待办 + 决策；DONE.md = 历史；PROJECT\_MAP.md = 项目地图 |
| 冲突时  | 文档改文档；DONE.md 历史不改；代码优先                           |
| 待讨论项 | 全部列在 §7，等用户主动提出再展开                                |
| 引用格式 | 文档内用 `[filename](file:///f:/Notes/...)` 链接        |
| 撤销决策 | 在决策日志写撤销行，不删除原行                                   |

