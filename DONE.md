# 已完成清单 — 个人网站(基于本地 Obsidian Vault)

> 维护方式：每完成一大阶段，在下方加一段记录。(最新记录写在最上方)

---
## 2026-06-30 · Music 播放器新增播放模式与音量控制

### 改动

| 文件 | 改动 |
|---|---|
| [layouts/shortcodes/music-list.html](file:///f:/Notes/layouts/shortcodes/music-list.html) | 新增播放模式/音量控制栏 HTML（位于歌曲列表上方） |
| [layouts/partials/music-player.html](file:///f:/Notes/layouts/partials/music-player.html) | 移除播放模式/音量控件，保持底部播放器简洁 |
| [static/js/music-player.js](file:///f:/Notes/static/js/music-player.js) | 支持三种播放模式（Loop All / Loop One / Shuffle）、音量控制、静音切换；localStorage 记忆音量与模式 |
| [assets/css/_05_cards.css](file:///F:/Notes/assets/css/_05_cards.css) | 新增 `.music-controls-bar` 页面控制栏样式（播放模式按钮 + 音量滑块） |
| [assets/css/_07_music-player.css](file:///F:/Notes/assets/css/_07_music-player.css) | 移除不再需要的音量控件样式 |

### 功能

- **播放模式**：列表循环 / 单曲循环 / 随机播放（点击切换，active 态高亮）
- **音量控制**：滑块调节 + 静音按钮 + 百分比显示
- **localStorage 记忆**：音量与模式设置持久保存
- **UI 位置**：控制栏位于 `/life/music/` 页面歌曲列表上方，不在底部弹出播放器里
- **界面语言**：全部英文（Mode / Vol / Loop All / Loop One / Shuffle）

### 设计决策

- 控制栏放在页面列表区而非底部播放器，保持播放器简洁易用
- 随机播放使用 Fisher-Yates 洗牌算法打乱顺序
- 音量滑块 hover 时显示手柄，图标随音量等级变化（高/低/静音）

---

## 2026-06-30 · 全站图片转 webp + 加载策略优化

### 改动

| 文件 / 目录 | 改动 |
|---|---|
| [scripts/convert-to-webp.ps1](file:///f:/Notes/scripts/convert-to-webp.ps1) | 新增一次性转换脚本：用 `cwebp` 把 `static/image/` 和 `content/notes/*/image/` 下所有 png/jpg 转 webp，质量 80，自动备份原图到 `._backup_originals/` |
| [scripts/replace-image-refs.ps1](file:///f:/Notes/scripts/replace-image-refs.ps1) | 新增引用替换脚本：扫描 `data/` `layouts/` `content/` `assets/css/` 内 `.png/.jpg` 引用并改成 `.webp` |
| `static/image/*.png/jpg` | 全部转 webp（原图保留在 `._backup_originals/static/image/`），共 12 张图，3.3MB → 0.7MB |
| `content/notes/*/image/*.png` | 全部转 webp（原图保留在 `._backup_originals/content/notes/*/image/`），共 7 张图 |
| [layouts/partials/head.html](file:///f:/Notes/layouts/partials/head.html) | preload 路径自动跟随改为 `.webp`；封面花朵的两条 preload 补上 `fetchpriority="high"` |
| [layouts/partials/home/custom.html](file:///f:/Notes/layouts/partials/home/custom.html) | `黑色花.png` 引用改 `黑色花.webp`（12 处，Hugo dict 形式） |
| [layouts/partials/header/basic.html](file:///f:/Notes/layouts/partials/header/basic.html) | logo `<img>` 加 `loading="eager" decoding="async" fetchpriority="high"`（首屏 logo 不应懒加载） |
| [layouts/shortcodes/about-timeline.html](file:///f:/Notes/layouts/shortcodes/about-timeline.html) | timeline 图补 `fetchpriority="low"` |
| `data/*.yaml`、`content/notes/*/index.md`、`content/about/_index.md`、`assets/css/_08_cover.css` | 引用路径已由脚本批量改 `.webp` |

### 结果

- **19 张图总计：3.84 MB → 1.07 MB，节省 72%**
- 转换前后单图对比示例：
  - `cover-README.png` 746 KB → 42 KB（-94%）
  - `cover-Blackhumor.png` 325 KB → 15 KB（-95%）
  - `melody.png` 564 KB → 46 KB（-92%）
  - `bedrock_MC.png` 287 KB → 119 KB（-59%）
  - `file-20260609163609280.png` 234 KB → 34 KB（-86%）
- 加载策略：封面/头像/logo `eager + high`，卡片封面/时间轴 `lazy + low`，全部 `async` 解码
- 备份目录：`f:\Notes\._backup_originals\`（如需回滚，把文件拷回原位即可）

### 注意事项

- 占位封面 `data/resources.yaml` 的 `minecraft.png` 文件本身不存在，保留原样未替换
- `data/*.yaml` 里的注释（`<slug>.png` 路径模板）未替换，仅替换实际可加载的引用
- 文档 `DONE.md` / `PROJECT_MAP.md` / `DEPLOY.md` 中说明性路径未替换
- `Vault/` 内容源保持只读，未触碰
- `public/` 是 Hugo 编译产物，下次 `hugo` 会自动重新生成

---
## 2026-06-28 · 站点统计改为显示项目数与音乐数

### 改动

| 文件 | 改动 |
|---|---|
| [layouts/partials/site-stats.html](file:///f:/Notes/layouts/partials/site-stats.html) | 将站点统计中的 `tags` 替换为 `projects` 与 `music`；项目数读取 `data/projects.yaml`，音乐数读取 `data/music.yaml`，继续保持构建时统计 |
| [PROJECT_MAP.md](file:///f:/Notes/PROJECT_MAP.md) | 补充“改站点统计显示项”的维护入口，并注明 `site-stats` 当前显示项 |
| [BLOWFISH_FEATURE_AUDIT.md](file:///f:/Notes/BLOWFISH_FEATURE_AUDIT.md) | 补充 `site-stats` 当前统计项的数据来源说明 |

### 结果

- 站点统计现在显示 `notes / projects / music / days online / last updated`
- `projects` 与 `music` 都只在构建发布时更新，符合当前站点的静态统计思路
- `days online` 仍然保留前端实时计算；其余项目继续由 Hugo 构建期生成

---
## 2026-06-28 · 新增 notes 专用 archetype

### 改动

| 文件 | 改动 |
|---|---|
| [archetypes/notes.md](file:///f:/Notes/archetypes/notes.md) | 新增 `notes` 专用 archetype，统一 `notes` 新文章的基础 front matter、标签字段、更新时间字段与页面级可选覆写注释 |
| [BLOWFISH_FEATURE_AUDIT.md](file:///f:/Notes/BLOWFISH_FEATURE_AUDIT.md) | 将 `archetypes` 条目标记为已实施，并补充该 archetype 的定位：只承载文章级字段，分区规则继续交给 `cascade` |
| [PROJECT_MAP.md](file:///f:/Notes/PROJECT_MAP.md) | 将 `/notes/` 新文章 SOP 改为优先使用 `hugo new content/notes/<slug>/index.md`，并记录 archetype 与后续 page resources 的配合方式 |

### 结果

- 以后新建 `notes` 时不需要再从旧文章复制 front matter
- `notes` 文章模板和现有 `cascade + site params` 的职责边界更清晰，不会重复堆一堆默认开关
- 后续若要继续升级 `page resources`，当前 archetype 已预留了说明，不会和未来内容结构冲突

---
## 2026-06-28 · 站点在线天数改为前端实时计算

### 改动

| 文件 | 改动 |
|---|---|
| [layouts/partials/site-stats.html](file:///f:/Notes/layouts/partials/site-stats.html) | `days online` 改为输出带 `data-launch-date` 的占位元素；首屏保留构建期兜底值，加载后交给前端脚本实时校正 |
| [static/js/site-stats-days.js](file:///f:/Notes/static/js/site-stats-days.js) | 新增轻量脚本，按 `data/site.yaml` 的 `launch_date` 在浏览器端实时计算站点在线天数 |
| [data/site.yaml](file:///f:/Notes/data/site.yaml) | 继续只维护固定起点 `launch_date`，不再需要为在线天数单独触发部署 |

### 结果

- 即使几天不重新部署，`days online` 也会在用户打开页面时自动更新
- `launch_date` 仍然是唯一手动维护项，只需在真实站点起始日期变更时改一次
- `notes / tags / last updated` 仍然保持 Hugo 构建期统计逻辑，不受这次改动影响
- 同步将 `site-stats` 中遗留的 `.Site.Data` 改为 `hugo.Data`，消除 Hugo v0.163 的 deprecation 警告

---
## 2026-06-27 · 首页封面收尾清理与信息对齐

### 改动

| 文件 | 改动 |
|---|---|
| [assets/css/_08_cover.css](file:///f:/Notes/assets/css/_08_cover.css) | 将首页副标题与站点统计改为居中；删除首页已不再使用的 `cover-footnote`、封面逐字入场残留选择器，并补充“封面略超出版心”的维护注释 |
| [assets/css/_04_hero.css](file:///f:/Notes/assets/css/_04_hero.css) | 修正 page hero 注释，明确 `Splitting` 的共享基础样式来自 `_08_cover.css` |
| [layouts/partials/home/custom.html](file:///f:/Notes/layouts/partials/home/custom.html) | 删除首页已无视觉作用的 `data-splitting`、`Splitting()` 初始化脚本和黑花 `animation-delay` 残留；收紧 `cover` / `home_highlights` 的 fallback 到当前真实在用字段 |
| [data/home_highlights.yaml](file:///f:/Notes/data/home_highlights.yaml) | 删除首页已不再读取的 `section_kicker / section_title / section_text` 字段，并补注释说明当前只维护 `sections` |
| [data/cover.yaml](file:///f:/Notes/data/cover.yaml) | 清理旧首页遗留的 `background / entrance / social / decorations / palette` 字段与过期注释，只保留当前首页 masthead 与顶栏 GitHub 按钮真实在用配置 |
| [PROJECT_MAP.md](file:///f:/Notes/PROJECT_MAP.md) | 同步首页数据结构与维护说明，去掉已经失效的首页字段说明 |

### 结果

- 首页 masthead 里的 `Welcome to...` 副标题与站点统计现在都居中，不再偏向头像这一侧
- 首页模板、数据文件和 CSS 里已经确定无效的残留逻辑又清掉一轮，后续维护时不会再被旧字段和旧脚本误导
- 首页配色和数据入口的注释更贴近当前真实结构，减少“文档还停留在前一版”的问题

### 验证

- `GetDiagnostics`：[`custom.html`](file:///f:/Notes/layouts/partials/home/custom.html)、[`_08_cover.css`](file:///f:/Notes/assets/css/_08_cover.css)、[`_04_hero.css`](file:///f:/Notes/assets/css/_04_hero.css)、[`cover.yaml`](file:///f:/Notes/data/cover.yaml)、[`home_highlights.yaml`](file:///f:/Notes/data/home_highlights.yaml) 当前无 diagnostics 报错
- `hugo --renderToMemory --themesDir themes --theme blowfish --config hugo.toml` 构建通过

---

## 2026-06-27 · 首页封面重构为“真首页式封面”

### 改动

| 文件 | 改动 |
|---|---|
| [layouts/partials/home/custom.html](file:///f:/Notes/layouts/partials/home/custom.html) | 首页主体从“居中 CTA + Start Here 展开区”改为“上方 masthead + 下方三组 highlights”；移除封面专用主题切换与首页专属假 header 逻辑，直接复用主题原生 header |
| [assets/css/_08_cover.css](file:///f:/Notes/assets/css/_08_cover.css) | 删除首页对主题 header 的隐藏规则，保留暖白、grain、上下花边、左右黑花与古典分隔符；重写首页 masthead 与三列 highlights 样式，并补移动端纵向堆叠 |
| [data/home_highlights.yaml](file:///f:/Notes/data/home_highlights.yaml) | 新增首页精选数据文件，独立维护 `Daily / Docs / Works Highlights` 的分组说明、组级入口与手动精选条目 |
| [content/_index.md](file:///f:/Notes/content/_index.md) | 同步首页注释说明，标明首页现在由 `cover.yaml` + `home_highlights.yaml` 驱动 |
| [PROJECT_MAP.md](file:///f:/Notes/PROJECT_MAP.md) | 同步首页维护入口、数据源和当前首页结构说明 |

### 结果

- 首页现在直接显示与内页一致的主题原生 header，不再靠 `_08_cover.css` 隐藏 header 再另做一套首页专用交互
- 首屏信息层级从“两个大按钮”切换成“轻量个人 intro + 精选导览”，头像、名字、副标题、统计仍保留，但不再压住整页重心
- 原有暖白衬线、grain、上下流动花边、左右黑花和古典分隔符都保留下来，没有被改成普通博客首页
- 首页精选改为完全数据驱动；以后换首页推荐内容，优先改 [`data/home_highlights.yaml`](file:///f:/Notes/data/home_highlights.yaml)，不用再动模板本体
- 旧的 [`data/start_here.yaml`](file:///f:/Notes/data/start_here.yaml) 目前不再参与首页渲染，但文件先保留作历史参考，避免贸然删除带来回溯困难

### 验证

- `GetDiagnostics`：[`custom.html`](file:///f:/Notes/layouts/partials/home/custom.html) 与 [`_08_cover.css`](file:///f:/Notes/assets/css/_08_cover.css) 当前无 diagnostics 报错

---

## 2026-06-27 · Notes 接入 Firebase 阅读数与点赞

### 改动

| 文件 | 改动 |
|---|---|
| [hugo.toml](file:///f:/Notes/hugo.toml) | 新增 `[params.firebase]` 配置，并明确 `article.showViews / article.showLikes` 的站点级默认值 |
| [content/notes/_index.md](file:///f:/Notes/content/notes/_index.md) | 在 `cascade` 中只给 `notes` 后代文章开启 `showViews / showLikes` |
| [FIREBASE_SECURITY.md](file:///f:/Notes/FIREBASE_SECURITY.md) | 新增根目录安全说明，记录 Firestore Rules、Anonymous Auth 与上线后检查步骤 |
| [BLOWFISH_FEATURE_AUDIT.md](file:///f:/Notes/BLOWFISH_FEATURE_AUDIT.md) | 将 `Views / Likes` 标记为已实施，并补充安全说明入口 |

### 结果

- `notes` 单篇文章现在可以使用 Blowfish 原生 `views / likes`
- `Like` 按钮会出现在文章头部 meta 区
- `apiKey` 等前端配置虽然会下发到浏览器，但安全边界已明确收口到 Firestore Rules 与 Anonymous Auth
- 后续若要调整 Firebase 安全策略，不必翻聊天记录，直接看根目录 `FIREBASE_SECURITY.md`

---

## 2026-06-27 · Notes 开启 Taxonomies / Edit Link / Pagination + 接入 Umami

### 改动

| 文件 | 改动 |
|---|---|
| [hugo.toml](file:///f:/Notes/hugo.toml) | 补 `article.editURL / editAppendPath`，并按 Blowfish 原生方式接入 `[params.umamiAnalytics]` |
| [content/notes/_index.md](file:///f:/Notes/content/notes/_index.md) | 新增 `cascade`，只给 `notes` 下文章开启 `showTaxonomies / showEdit / showPagination` |
| [content/notes/linux-getting-started/index.md](file:///f:/Notes/content/notes/linux-getting-started/index.md) + [content/notes/python-env-setup/index.md](file:///f:/Notes/content/notes/python-env-setup/index.md) | 删掉旧的 `showEdit: false`，避免覆盖 `notes` 分区级默认规则 |
| [BLOWFISH_FEATURE_AUDIT.md](file:///f:/Notes/BLOWFISH_FEATURE_AUDIT.md) | 补充本轮已确认实施方案，并新增 `Taxonomies 后续维护约定` |
| [PROJECT_MAP.md](file:///f:/Notes/PROJECT_MAP.md) | 同步 notes 分区 `cascade`、Umami 配置入口和 taxonomy 维护入口 |

### 结果

- `notes` 文章现在可以显示 taxonomy 信息，并继续沿用 Blowfish 原生渲染链路
- `Edit Link` 只在 `notes` 文章里开启，且只是跳转到 GitHub 编辑页，真正修改权限仍由仓库控制
- `notes` 文章的上一篇 / 下一篇由 [`layouts/page.html`](file:///f:/Notes/layouts/page.html) 补回主题原生 `article-pagination`
- Umami 已按 Blowfish 原生 analytics 配置接入，不需要手写 head 脚本
- 后续如何维护 `tags / categories / series` 已写入根目录文档，避免后面越写越乱

---

## 2026-06-27 · 微调上一篇/下一篇样式并确认阅读数数据源方向

### 改动

| 文件 | 改动 |
|---|---|
| [layouts/partials/article-pagination.html](file:///f:/Notes/layouts/partials/article-pagination.html) | 新增项目级 pagination partial 覆写，保留 Blowfish 原生前后文逻辑，只重做输出结构以便精确控样式 |
| [assets/css/_02_chrome.css](file:///f:/Notes/assets/css/_02_chrome.css) | 将上一篇/下一篇从“简单文字链接”微调为更贴近全站设计语言的轻卡片样式，补上 serif 标题、mono kicker/date、hover 态与移动端单列适配 |

### 结果

- `notes` 文章底部的上一篇/下一篇现在有更完整的视觉承载，不再只是简单一行链接
- 视觉语言与现有 module / article card 更接近，但没有引入重组件感
- 进一步确认：如果后面要启用 Blowfish 原生 `views / likes`，最省事、最原生的方案仍然是 `Firebase`
- `Umami` 继续适合作为后台分析，不适合作为主题现成的前台阅读数来源

---

## 2026-06-27 · 扩展站点静态统计摘要并记录站龄起点

### 改动

| 文件 | 改动 |
|---|---|
| [data/site.yaml](file:///f:/Notes/data/site.yaml) | 新增站点级数据文件，记录网站起始日期 `2026-06-19`，供后续静态统计复用 |
| [layouts/shortcodes/site-stats.html](file:///f:/Notes/layouts/shortcodes/site-stats.html) | `site-stats` 从 S1 升级到 S2：显示 `notes / tags / days online / last updated`，在线天数按 build 时动态计算 |

### 结果

- `/about/` 与 `/notes/` 中调用的 `site-stats` 现在会显示站龄相关摘要
- 这部分完全基于 Hugo 构建期计算，无需外部服务
- 站龄起点不再硬编码在模板里，后续只需改 `data/site.yaml`
- 动态阅读数仍建议后续走 Blowfish 原生 `Firebase views`

---

## 2026-06-27 · 封面接入可复用的站点统计摘要

### 改动

| 文件 | 改动 |
|---|---|
| [layouts/partials/site-stats.html](file:///f:/Notes/layouts/partials/site-stats.html) | 新增可复用 `partial`，承载 `notes / tags / days online / last updated` 的实际渲染逻辑 |
| [layouts/shortcodes/site-stats.html](file:///f:/Notes/layouts/shortcodes/site-stats.html) | 改成 shortcode 壳，仅转发到 `partial "site-stats.html"`，保持现有内容页调用方式不变 |
| [layouts/partials/home/custom.html](file:///f:/Notes/layouts/partials/home/custom.html) | 封面新增 `show_stats` 开关位，开启时直接复用站点统计 partial |
| [data/cover.yaml](file:///f:/Notes/data/cover.yaml) | 新增 `show_stats: true`，由数据层控制封面是否显示统计摘要 |
| [assets/css/_08_cover.css](file:///f:/Notes/assets/css/_08_cover.css) | 新增封面统计区样式，使 `site-stats` 在首页首屏中居中并沿用封面配色 |

### 结果

- 首页封面现在可以显示与 `/about/`、`/notes/` 同源的站点统计信息
- 后续若要调整统计文案或计算逻辑，只需要改 `layouts/partials/site-stats.html`
- 后续若只想隐藏封面统计，无需改模板，只需把 `data/cover.yaml` 的 `show_stats` 改为 `false`

---



## 2026-06-26 · About Timeline 改为数据驱动并支持多组

### 改动

| 文件 | 改动 |
|---|---|
| [data/about_timeline.yaml](file:///f:/Notes/data/about_timeline.yaml) | 用 `groups` 结构统一管理时间线分组、里程碑顺序、文案、折叠状态和可选图片字段，并新增一组 `Learning path` |
| [layouts/shortcodes/about-timeline.html](file:///f:/Notes/layouts/shortcodes/about-timeline.html) | 改为循环读取多组 `about_timeline.yaml`，保留整块折叠 + 单条折叠结构，并支持可选左图右文 |
| [assets/css/_09_about.css](file:///f:/Notes/assets/css/_09_about.css) | 补充时间线多组容器间距和里程碑图片样式；图片改为“原比例优先 + 统一最大尺寸范围” |
| [PROJECT_MAP.md](file:///f:/Notes/PROJECT_MAP.md) | 同步 about timeline 的新维护入口和加图方式 |

### 结果

- 以后加里程碑文字，不用再改 shortcode 结构
- 以后给某条里程碑加图片，只需在数据文件里补字段
- 现在同一个 about timeline 可以放多组内容，`Learning path` 已直接接入
- 里程碑图片不再强制裁成固定比例，而是按原图比例缩放到相近大小

---

## 2026-06-26 · Start Here 改为数据驱动

### 改动

| 文件 | 改动 |
|---|---|
| [data/start_here.yaml](file:///f:/Notes/data/start_here.yaml) | 新增首页 `Start Here` 数据文件，统一管理三张卡的文案、跳转和读取模式 |
| [layouts/partials/home/custom.html](file:///f:/Notes/layouts/partials/home/custom.html) | 改成循环读取 `start_here.yaml`；当前统一按固定 `page` 路径渲染三张卡 |
| [PROJECT_MAP.md](file:///f:/Notes/PROJECT_MAP.md) | 把 `Start Here` 的维护入口更新为数据文件，并同步新的更新规则 |

### 结果

- 后续改首页三张卡片的固定文字，不用再改模板
- `Latest Note` 现在固定跳到 `/notes/`，用户能直接看到最新文章并继续自由选择
- `Music` / `Projects` 的跳转和文案也集中到一个数据文件里维护

---

## 2026-06-26 · Inner Hero Spacing Tightened + Divider Contrast Raised

### 改动

| 文件 | 改动 |
|---|---|
| [assets/css/_04_hero.css](file:///f:/Notes/assets/css/_04_hero.css) | 再次上移共享 `page-hero`；继续减少非封面页 `article` 的顶部 padding |
| [layouts/page.html](file:///f:/Notes/layouts/page.html) | 将 `layout: "page"` 页面里的 `#single_header` 顶部间距进一步收紧到 `mt-0` |
| [assets/css/_05_cards.css](file:///f:/Notes/assets/css/_05_cards.css) + [assets/css/_03_prose.css](file:///f:/Notes/assets/css/_03_prose.css) | 提高 `section-rule` / `page-divider` / `cover-divider` 与正文 `hr` 两侧横线的对比度 |

### 结果

- 非封面页的 hero 区块整体更靠上
- 顶栏下方的空白更少，但仍保留安全呼吸感
- “横线 + ✦ + 横线” 里的横线不再过淡
- 封面页和 `ABOUT ME` 保持当前状态不变

---

## 2026-06-26 · 全站分隔符统一为“横线 + ✦ + 横线”

### 改动

| 文件 | 改动 |
|---|---|
| [assets/css/_03_prose.css](file:///f:/Notes/assets/css/_03_prose.css) | 统一正文 `hr` 样式；补分隔符相邻去重；分隔符后紧跟 `h2` 时自动去掉标题顶部细线 |
| [assets/css/_05_cards.css](file:///f:/Notes/assets/css/_05_cards.css) + [assets/css/_04_hero.css](file:///f:/Notes/assets/css/_04_hero.css) + [assets/css/_08_cover.css](file:///f:/Notes/assets/css/_08_cover.css) | 收口 `section-rule`、`page-divider`、`cover-divider` 的基础视觉语言 |
| [assets/css/_09_about.css](file:///f:/Notes/assets/css/_09_about.css) | 去掉 about 的特殊分隔符覆盖，让 about 回到全站统一规则 |
| [content/life/_index.md](file:///f:/Notes/content/life/_index.md) 等 6 个页面 | 删除 `section-rule` 后面紧跟的重复 `---` |
| [PROJECT_MAP.md](file:///f:/Notes/PROJECT_MAP.md) | 增加全站分隔符规则和写作约定 |

### 结果

- 全站块级分隔符统一成一种视觉语言
- about 和普通文章都回到同一套分隔规则
- 已有重复分隔源头被清掉，后续写作也有约定可循

---

## 2026-06-26 · ABOUT ME 结构收口为 Technical stack 下的 Focus + 可折叠 Path

### 背景

上一版 `ABOUT ME` 里新增了 `Now`、`Current focus`、`Path so far` 三块，但实际看下来有两个问题：

1. `Now` 和 `Current focus` 语义重叠，信息层级不够清楚
2. `Path so far` 如果后续继续加内容，会越来越长，页面不够轻，也不利于后面给里程碑扩展图片

这轮的目标就是把新增内容收口得更统一、更利于后续维护：

- 新增内容统一压到 `Technical stack` 下面
- `Now` 合并进 `Current focus`
- `Path so far` 改成可折叠的里程碑结构
- about 各板块之间统一补上星型分隔符

### 改动

| 文件 | 改动 |
|---|---|
| [content/about/_index.md](file:///f:/Notes/content/about/_index.md) | 删除单独的 `Now` 板块；把新增内容统一放到 `Technical stack` 下方；`Path so far` 改成“整块先折叠、里程碑再细折叠”的结构，并改为通过 shortcode 引入，避免原始 HTML 在 markdown 中被当文本显示 |
| [layouts/shortcodes/about-timeline.html](file:///f:/Notes/layouts/shortcodes/about-timeline.html) | 新增 about 专用 shortcode，承载 `Path so far` 的双层折叠里程碑结构，后续扩图也统一在这里维护 |
| [assets/css/_09_about.css](file:///f:/Notes/assets/css/_09_about.css) | 清理旧 `about-glance` 样式；补 `about-timeline-group-*` 和 `about-milestone-*` 样式；把原先较重的 `+ / -` 按钮改成更简约的 chevron；about 里只保留星型分隔符，不再叠加默认横线 |
| [layouts/_default/list.html](file:///f:/Notes/layouts/_default/list.html) | 给 about 的正文容器补 `about-page-content` 类，让分隔符去横线的覆盖只作用于 about，不影响其他 section |
| [PROJECT_MAP.md](file:///f:/Notes/PROJECT_MAP.md) | 同步记录：about 新增内容现在的实际顺序、`Path so far` 的 shortcode 入口、双层 `<details>` 结构、倒叙维护方式，以及未来给里程碑加左图的方式 |

### 结果

- `ABOUT ME` 的新增内容层级更明确，不再出现 `Now` / `Current focus` 重复
- `Path so far` 默认先收起整块内容，页面长度更可控，展开后再看细节
- 后续如果要给某个里程碑加图，已经有现成结构可接，不需要再推翻样式
- about 的板块分隔现在也走全站统一分隔规则

---

## 2026-06-26 · 首屏资源预加载 + ABOUT ME 内容扩充

### 背景

新一轮问题主要集中在 3 个点：

1. 首页和内页的一些图片资源希望更快、更稳，尽量减少刷新时的空白和失败概率
2. `ABOUT ME` 当前内容偏薄，除了头像、联系方式、技术栈和热力图外，缺少真正能说明“现在在做什么”的正文
3. 首页封面的 CTA 按钮刷新后会晚一拍才出现，影响首屏完成度

### 改动

| 文件 | 改动 |
|---|---|
| [layouts/partials/head.html](file:///f:/Notes/layouts/partials/head.html) | 按页面条件为首页和 `/about/` 首屏关键图片、字体加 `preload`，减少封面与头像的等待时间 |
| [layouts/partials/home/custom.html](file:///f:/Notes/layouts/partials/home/custom.html) | 首页头像和装饰花改为更积极的加载策略：`loading="eager"` / `decoding="async"` / `fetchpriority="high"` |
| [assets/css/_08_cover.css](file:///f:/Notes/assets/css/_08_cover.css) | 去掉首页 CTA 的延迟淡入，让按钮刷新后直接可见 |
| [layouts/partials/article-link/card.html](file:///f:/Notes/layouts/partials/article-link/card.html) | 文章卡封面图补 `fetchpriority="low"` 与可用时的 `width/height`，降低布局跳动 |
| [content/about/_index.md](file:///f:/Notes/content/about/_index.md) | 在原有头像 / 联系方式 / 技术栈之外，新增 `Now`、`Current focus`、`Path so far` 三块内容 |
| [assets/css/_09_about.css](file:///f:/Notes/assets/css/_09_about.css) | 新增 about 内容卡、焦点区和时间线路径样式，延续现有暖白衬线风格 |
| [PROJECT_MAP.md](file:///f:/Notes/PROJECT_MAP.md) | 补记录：`ABOUT ME` 新内容块维护入口、首页 / about 预加载链路位置 |

### 设计取舍

- **预加载只做关键资源**：只给首页和 `/about/` 的首屏图片与主要字体加 `preload`，避免全站无差别抢带宽
- **不动整体气质**：about 仍然保留头像、联系方式、技术栈、热力图这条主线，只是补齐“我现在在做什么”
- **按钮立即可见**：保留现有 hover 和交互语言，但去掉不必要的入场延迟

### 结果

- 首页 CTA 刷新后不再晚一拍出现
- 首页和 `/about/` 的关键图片有了更积极的加载优先级
- `ABOUT ME` 不再只是资料页，而是开始具备“当前方向 + 学习路径”的个人叙事

---

## 2026-06-25 · 首页收口为“封面式快速开始页” + Music 下载入口补齐

### 背景

原首页更像一张气质很强的封面图：有辨识度，但信息效率偏低。用户第一次进入站点后，需要先看封面，再通过入口按钮跳到 `/about/` 才能开始浏览。与此同时，`ABOUT ME` 被特殊渲染在顶栏左侧，已经不再适合新的首页定位。随后首页又经历了多轮收口：去重、按钮简化、`Start Here` 延迟展开、花朵重排、间距压缩。与此同时，`/life/music/` 也补上了下载入口与文件信息提示。

本轮调整的目标：

1. **保留首页封面的审美气质**
2. **让首页本身承担“快速开始页”的职责**
3. **让 `ABOUT ME` 回归与 `DOCS / WORKS / DAILY` 同级的普通菜单项**
4. **清掉首页重复入口，只保留真正有意义的首屏动作**
5. **让 `/life/music/` 的每首歌都能直接下载**

### 改动

| 文件 | 改动 |
|---|---|
| [layouts/partials/home/custom.html](file:///f:/Notes/layouts/partials/home/custom.html) | 首页封面改为最终版：首屏只保留 `Get To Know Me` / `Start Here` 两个 CTA；`Start Here` 默认隐藏，点击后展开；去掉重复导航卡和底部社交；黑花左右镜像、参数只维护一套 |
| [assets/css/_08_cover.css](file:///f:/Notes/assets/css/_08_cover.css) | 首页 CTA、`Start Here` 展开区、间距、标题大小、按钮纵排、花朵镜像与明亮主题黑花透明度都收口到当前版本 |
| [layouts/partials/header/basic.html](file:///f:/Notes/layouts/partials/header/basic.html) | 删除 `ABOUT ME` 的顶栏左侧特殊渲染，恢复为标准站点标题 + 右侧菜单结构 |
| [layouts/partials/header/components/desktop-menu.html](file:///f:/Notes/layouts/partials/header/components/desktop-menu.html) | 右侧桌面菜单恢复渲染全部 `menu.main` 项，不再跳过 `ABOUT ME` |
| [layouts/partials/header/components/mobile-menu.html](file:///f:/Notes/layouts/partials/header/components/mobile-menu.html) | 移动端菜单恢复渲染全部 `menu.main` 项 |
| [hugo.toml](file:///f:/Notes/hugo.toml) | `ABOUT ME` 去掉特殊 `identifier`，回归普通 Hugo 菜单配置 |
| [layouts/shortcodes/music-list.html](file:///f:/Notes/layouts/shortcodes/music-list.html) | 每首歌增加下载按钮，并显示文件格式 / 大小信息 |
| [assets/css/_05_cards.css](file:///f:/Notes/assets/css/_05_cards.css) | 下载按钮样式与歌曲文件信息样式；顺手把歌曲 note 的内联样式收成独立 class |
| [data/music.yaml](file:///f:/Notes/data/music.yaml) | 为现有歌曲补了 `size` 字段，给下载提示使用 |
| [static/js/music-player.js](file:///f:/Notes/static/js/music-player.js) | 点击下载按钮时不再误触发卡片播放；播放器状态恢复逻辑补齐 `playing` 和 `src` 匹配 |
| [PROJECT_MAP.md](file:///f:/Notes/PROJECT_MAP.md) | 补了首页 `Start Here` 的维护说明，并同步当前首页结构与 notes 实际渲染方式 |

### 首页结构变化

- **保留**：暖白衬线封面、头像、大标题、上下流动花边、左右黑花装饰、顶栏导航
- **首屏 CTA**：`Get To Know Me`、`Start Here`
- **展开区**：3 个“Start Here”精选起点（最新笔记 / Music / Projects）
- **删除**：重复的四张导航卡、底部 GitHub / Google Mail 社交按钮、黄色花素材

也就是说，首页不再只是“进入网站前的封面”，而是直接承担：

- 第一印象
- 导览
- 精选入口

### 设计取舍

- **没有推翻封面**：继续保留首页最有辨识度的视觉资产
- **没有把 `/about/` 强行改成首页替身**：`/about/` 回归“深入了解我”的页面职责
- **没有新加复杂模块或脚本**：只在现有 Hugo 模板和 CSS 结构内增强首页信息架构

### 验证

- `GetDiagnostics`：首页模板、封面 CSS、顶栏模板、`hugo.toml` 全部无报错
- `hugo --renderToMemory --themesDir themes --theme blowfish --config hugo.toml` 构建通过
- 构建结果：52 pages / 158 static files / 0 构建失败

### 结果

- 首页现在是“封面式快速开始页”
- 顶栏左侧只保留站点标题 `lyrumu's page`
- `ABOUT ME` 已回到顶栏右侧，与 `DOCS / WORKS / DAILY` 同级
- 首屏 CTA 精简为两个统一按钮：`Get To Know Me` 与 `Start Here`
- `Start Here` 现在默认隐藏，点击按钮后才会展开并平滑滚动到精选区
- 两个按钮改为竖排，展开区底部留白更安全，不会贴到下方流动花边
- 标题、头像区和整体上下留白都压紧了一轮，首屏更紧凑
- 封面只保留黑花，右侧花群通过镜像左侧参数保持对称
- `/life/music/` 现在每首歌都可直接下载，并显示格式与大小提示

---

## 2026-06-24 · /about/ 整个 page-hero 不显示（让头像顶上去）

### 背景

第一版只隐藏 page-hero 里的 eyebrow + divider 两条线，但 `page-hero` 容器本身有 `padding-top: clamp(2rem, 5vh, 4rem)` + `margin-bottom: 2-3.5rem`（[_04_hero.css](file:///f:/Notes/assets/css/_04_hero.css) L19-29）。所以头像上方还是有 2-4rem 空白。用户决定：**整个 page-hero 块在 about 里隐藏**，让头像直接顶上去。

### 改动

| 文件 | 改动 |
|---|---|
| [assets/css/_09_about.css](file:///f:/Notes/assets/css/_09_about.css) | `.page-hero--no-deco .page-eyebrow, .page-hero--no-deco .page-divider { display: none; }` → 改为 `.page-hero--no-deco { display: none; }` |
| [layouts/_default/list.html](file:///f:/Notes/layouts/_default/list.html) | about section 渲染时传 `extraClass="page-hero--no-deco"`（上轮已做） |
| [layouts/partials/cover/page-hero.html](file:///f:/Notes/layouts/partials/cover/page-hero.html) | 容器 div 加 `extraClass` 注入（上一轮已做） |

### 关键代码

```css
.page-hero--no-deco {
  display: none;
}
```

### 验证

- about 页 page-hero 整体隐藏（含 kicker / h1 "ABOUT ME" / subtitle / eyebrow / divider）
- notes / works / life 不传 page-hero--no-deco，page-hero 正常显示
- hugo build 0 warnings

---

## 2026-06-24 · /about/ 紧凑化（5 处 margin 调整）

### 背景

`/about/` 页头部空白过多、section 之间距离过宽。改 5 处 CSS margin 让头像更接近顶部、各 section 更紧凑。

### 改动清单

| 位置 | 改前 | 改后 |
|---|---|---|
| `.about-profile` margin | `2rem 0` | `0.5rem 0 1rem` |
| `.about-profile-row` margin-bottom | `1.5rem` | `0.85rem` |
| `.about-tags` margin | `1rem 0` | `0.6rem 0` |
| `.about-stats` margin | `2.5rem 0 1rem` | `1.25rem 0 0.4rem` |
| `.article-content hr, .about hr` margin（覆盖主题 3em） | `3em` | `1.2em` |
| `.about h2` margin（覆盖主题 1.5em/0.5em） | `1.5em 0 0.5em` | `0.7em 0 0.4em` |
| `.about-stats` group 之间 gap | `1.5rem` | `0.75rem` |
| `.about-stats-group` 内部 gap | `0.75rem` | `0.4rem` |

### 文件

- [assets/css/_09_about.css](file:///f:/Notes/assets/css/_09_about.css) — §37-39 全部加 `/* 2026-06-24 紧凑化：xxx */` 注释
- 新增小规则块：`.article-content hr, .about hr { margin: 1.2em 0 }` + `.article-content h2, .about h2 { margin: 0.7em 0 0.4em }` 覆盖主题 prose

### 验证

8 处全部生效，hugo build 0 warnings

---


## 2026-06-24 · 站点重构（语言切换 + 删除 /start/ + 顶栏主入口化）

### 背景

三件事一次性做完：
1. **默认语言 zh-cn → en**（hugo.toml），文章正文以中文居多故 `hasCJKLanguage` 保持 true
2. **删除 /start/ 大厅页**，合并到 /about/（"个人展示站"主入口）
3. **顶栏左侧"Catalogue"硬编码 → 改读 hugo.toml**（避免 HTML 硬编码 vs hugo.toml 数据源不一致）

### 改动清单

| 类型 | 文件 | 关键变更 |
|---|---|---|
| 配置 | [hugo.toml](file:///f:/Notes/hugo.toml) | `[languages.zh-cn]` → `[languages.en]`；`[[menu.main]] ABOUT ME` 加 `identifier = 'home'` |
| 模板 | [layouts/partials/header/basic.html](file:///f:/Notes/layouts/partials/header/basic.html) | 删 Catalogue 硬编码 → `range .Site.Menus.main` 找 `Identifier="home"` 项 |
| 模板 | [layouts/partials/header/components/desktop-menu.html](file:///f:/Notes/layouts/partials/header/components/desktop-menu.html) / [mobile-menu.html](file:///f:/Notes/layouts/partials/header/components/mobile-menu.html) | `range` 内加 `if ne .Identifier "home"` 跳过 |
| 模板 | [layouts/partials/home/custom.html](file:///f:/Notes/layouts/partials/home/custom.html) | L16 fallback `href` `/start/` → `/about/` |
| 内容 | 删除 [content/start/_index.md](file:///f:/Notes/content/start/_index.md) + 整个 [content/start/](file:///f:/Notes/content/start/) 目录 |
| 内容 | 迁移 [content/start/style-test/index.md](file:///f:/Notes/content/start/style-test/index.md) → [content/notes/style-test/index.md](file:///f:/Notes/content/notes/style-test/index.md) |
| 数据 | [data/cover.yaml](file:///f:/Notes/data/cover.yaml) | `entrance.href` `/start/` → `/about/` |
| 数据 | [data/modules.yaml](file:///f:/Notes/data/modules.yaml) + [layouts/shortcodes/modules-grid.html](file:///f:/Notes/layouts/shortcodes/modules-grid.html) | dead code，加废弃说明注释（保留不删） |
| 文档 | [PROJECT_MAP.md](file:///f:/Notes/PROJECT_MAP.md) | 删 5 处 `/start/` 引用 + dead code 文件清单 2 行 |

### 关键工程坑

1. **基本架构错误（被用户当场纠正）**：第一版把 `basic.html` 的 Catalogue **硬编码改成 "ABOUT ME"**——正确做法是删除 Catalogue + 用 `range .Site.Menus.main` 从 hugo.toml 读 `Identifier="home"` 项渲染。模板只决定位置，hugo.toml 才是真理源
2. **Hugo Menu API 误用**：写 `.Site.Menus.main.GetByIdentifier "home"` → build 报错 `can't evaluate field GetByIdentifier in type navigation.Menu`。Hugo v0.163.2 的 `navigation.Menu` 类型只有 `ByName / ByWeight / Limit / Reverse`，**没有 `Get*` 方法**。改用 `range` 遍历查找
3. **并发 edit 失效**：同时对同一文件做多个 `SearchReplace` 时，偶尔显示 success 但实际未写入。修复：每次单独 edit + 立即 Read 验证

### 教训

- **模板硬编码 = 技术债**：菜单项等内容必须从 hugo.toml 等配置驱动，模板只决定渲染位置。否则维护时要在多处同步改
- **改 API 前先查文档**：Hugo Menu API 不像直觉那样有 `GetByName` / `GetByIdentifier`，务必 `WebFetch` / `query-docs` 确认
- **并发 edit 后必须 Read 验证**：编辑工具的 success 不等于磁盘已写入，重要改动后用 Read 工具确认

---

## 2026-06-23 · Linux 入门文章整合（WSL2 / OpenCode / Hermes Agent）

### 背景

[`Vault/Docs/WSL2/`](file:///f:/Notes/Vault/Docs/WSL2/) 目录下散落着 8 篇 Linux 主题笔记（Opencode ×2 / Hermes ×3 / Fix ×3），没有入口页，Vault 内的阅读路径是"目录式"逐个点开。响应用户需求"在 docs 里上传一篇新文章，整理所有 Linux 相关内容"——合成一篇综合性入门文章，把这些碎片串成可线性阅读的教程。

### 文章结构

11 个主章节，**严格按用户给定的内容顺序**：

1. 为什么选择 WSL2（vs 原生 / VM / Mac 对比表）
2. 安装 WSL2 Ubuntu（一键安装 / 验证 / 重装）
3. 基础配置（更新 / 换源清华 / 关闭 PATH 继承 / 备份 Ubuntu）
4. **基础 Linux 命令入门**（10 个分类速查表，覆盖文件 / 文本 / 进程 / 权限 / 网络 / apt / 压缩 / 服务）
5. 安装 Node.js（nvm 多版本管理，OpenCode / Hermes 共用前置）
6. OpenCode Agent（安装 / 代理 / WSL 内项目 / AGENTS.md / Skills / MCP / Oh My OpenCode / Session 习惯）
7. Hermes Agent（前置 / 一键安装 / 目录结构 / LLM Provider / TUI / 基础命令 / 安全加固 / 进阶 / 更新）
8. **优势组合**（WSL2 vs Windows / Mac / VM 三方对比 + OpenCode vs Hermes 选型建议）
9. 常见问题修复（VMware 关机 / WinNAT 端口 / Dashboard / API 网络）
10. 速查命令汇总
11. 参考资料（Vault 原文索引 + 官方文档链接）

### 内容来源

- **完全来自 Vault**：安装步骤、换源、PATH 优化、备份、OpenCode / Hermes 的命令、Fix 章节
- **补充**：第 4 章基础 Linux 命令（Vault 没有专门的入门命令文档，按 Linux 常用清单补充）
- **原创**：第 8 章优势组合对比（基于 Vault 内容做横向分析）

### 文件清单

| 类型 | 路径 |
|---|---|
| 新增 | [content/notes/docs/wsl2/linux-getting-started/index.md](file:///f:/Notes/content/notes/docs/wsl2/linux-getting-started/index.md) — 11 章节 ~580 行 |
| 新增（图片） | [content/notes/docs/wsl2/linux-getting-started/image/](file:///f:/Notes/content/notes/docs/wsl2/linux-getting-started/image/) — 5 张 PNG（opencode ×3 + hermes ×2） |

### 图片处理

5 张图片从 `Vault/Docs/WSL2/` 复制到 `content/notes/docs/wsl2/linux-getting-started/image/`，并按内容语义重命名（便于 markdown 引用和未来维护）：

| 原文件名 | 新文件名 | 用在哪 |
|---|---|---|
| `WSL内安装opencode.png` | 不改 | §6.1 OpenCode 一键安装 |
| `opencode-AGENTSmd.png` | 不改 | §6.5 AGENTS.md |
| `优化环境变量.png` | 不改 | §3.3 优化环境变量 |
| `file-20260606222237624.png` | `hermes-tui-config.png` | §7.4 TUI 配置 |
| `file-20260606221444684.png` | `hermes-tui-sessions.png` | §7.6 TUI 历史会话浏览 |

Obsidian 自动生成的 `file-2026xxxxxxxxx.png` 命名无意义，重命名后 markdown 引用更可读。

### 验证

- `hugo --renderToMemory`：**56 页通过**（之前 47 → 56，新增 9 个页面 = 新文章 + 各种 alias/list 衍生）
- 页面 URL：`/notes/docs/wsl2/linux-getting-started/` ✓
- 渲染 HTML 大小：164KB（含 5 张图 + 完整 prose 样式）✓
- 内部链接验证：所有 `file:///f:/Notes/Vault/...` 引用都基于 Obsidian Vault 路径，点击可在本地跳转

### 设计决策

- **不创建父级 _index.md**：用户明确表示"需求就是直接在 doc 里创建一篇文章"，不擅自新增 docs/ 和 wsl2/ 的入口页（避免范围蔓延）
- **图片放本地**：`/image/...` 走 Hugo 静态资源，与项目其他文章风格一致（参考 python-env-setup）
- **大量表格 + 代码块**：技术教程 + 命令速查的形式比纯散文更适合 Linux 入门
- **章节顺序按用户指定**：安装 → 命令 → OpenCode → Hermes → 优势 → Fix，逻辑上由浅入深

### 后续

- 用户启动 hugo server 后可手动预览 `/notes/docs/wsl2/linux-getting-started/`
- 父级 docs/ 和 wsl2/ 入口页留待后续需要时再补

---


## 2026-06-23 · PC 端卡片相对 hero 偏左 · 真凶是 `.prose` 的 max-width: 65ch

### 根因

[`layouts/_default/list.html`](file:///F:/Notes/layouts/_default/list.html) line 32 用 `class="prose ... max-w-none"`，但本项目 Tailwind **没有纯 `.max-w-none`**（只有 `.lg\:max-w-none`，仅 lg 断点）→ `max-width: none` 不生效 → `.prose` 自带的 `max-width: 65ch` (576px) 把下面的 `.modules-grid` 压成 576px 宽 → `.modules-grid-stack` 在 576px 内居中（center ≈ 688px），而 `.page-hero` 在 main 中心（center = 960px），差 272px → "明显偏左"。

### 修复

| 文件 | 改动 |
|---|---|
| [_05_cards.css](file:///F:/Notes/assets/css/_05_cards.css) 顶部 | 加 `main > section.prose { max-width: none }`（specificity 0,1,2 压过 `.prose` 0,1,0）|
| [_05_cards.css](file:///F:/Notes/assets/css/_05_cards.css) §15/16/32/34 | 4 个 `*-stack` 的 `max-width: 44rem` → `56rem`（与 `.page-hero` 同宽）|
| [themes/blowfish/.../baseof.html](file:///F:/Notes/themes/blowfish/layouts/_default/baseof.html) line 11 | body padding `md:px-24 lg:px-32` → `md:px-16 lg:px-20`（内容区 1024px → 1120px）|

修复后 hero 中心 = cards 中心 = 960px（viewport 中心），左右边缘完美对齐。

---

## 2026-06-23 · custom.css 拆分重构（3514 行单文件 → 9 个模块 + 主入口）

### 背景

[assets/css/custom.css](file:///F:/Notes/assets/css/custom.css.bak.v2) 累积到 **3514 行 / ~100KB**，单文件维护成本高：

- 改一处要在 3500 行里 Ctrl+F 定位
- 模块边界模糊（封面 / 卡片 / prose / About 全部揉在一起）
- git diff 一片红，无 review 价值
- 多人协作容易冲突

### 1. 拆分方案：9 个 `_*.css` + `custom.css` 索引

按"基础 → 组件 → 页面"分层，前缀数字保证加载顺序：

| 文件 | 行数 | 职责 |
|---|---|---|
| [custom.css](file:///F:/Notes/assets/css/custom.css) | 44 | **文档索引**（不再被加载）|
| [_01_tokens.css](file:///F:/Notes/assets/css/_01_tokens.css) | 160 | `@font-face` + CSS 变量 (light/dark) + `html/body` 基线 |
| [_02_chrome.css](file:///F:/Notes/assets/css/_02_chrome.css) | 102 | footer / 主菜单 / scroll-to-top / 分页 / TOC |
| [_03_prose.css](file:///F:/Notes/assets/css/_03_prose.css) | 250 | 长文章 `.prose` + `.reveal` 滚动入场 |
| [_04_hero.css](file:///F:/Notes/assets/css/_04_hero.css) | 210 | `.page-hero` + 面包屑 + single 页头 |
| [_05_cards.css](file:///F:/Notes/assets/css/_05_cards.css) | 1041 | module / vault / article-link / life / music-list / works-sub / file-tree / section-rule |
| [_06_works-cards.css](file:///F:/Notes/assets/css/_06_works-cards.css) | 553 | projects (3D 倾斜) + resources (瀑布流) |
| [_07_music-player.css](file:///F:/Notes/assets/css/_07_music-player.css) | 323 | 全局音乐播放器 + `.copy-toast` |
| [_08_cover.css](file:///F:/Notes/assets/css/_08_cover.css) | 503 | 封面页（全屏 + 花边 + 字符入场）|
| [_09_about.css](file:///F:/Notes/assets/css/_09_about.css) | 356 | About 页（profile + 标签 + 液态玻璃）|

数字前缀 `_01_` → `_09_` 保证 `resources.Match` 按字典序加载时就是正确顺序（tokens 必须最先、覆盖样式最后）。Hugo Pipes `resources.Match "css/_*.css"` 自动发现，新加 `_NN_xxx.css` 不用改 head.html。

### 2. 关键工程坑：CSS `@import` 在本项目不工作（必看！）

**踩坑记录**（如果别人接手项目，第一眼看 custom.css 看到 `@import url("_*.css")` 会以为能用 → **大坑**）：

#### 现象
最初按"标准 CSS 写法"在 `custom.css` 里写 `@import url("_tokens.css")`，以为 Hugo Pipes 会展开。结果：

- ✅ 编译通过，CSS bundle 正确生成
- ❌ 浏览器收到 bundle 后，看到 `@import url("_tokens.css")` → 发起 HTTP 请求 `/_tokens.css`
- ❌ `/_tokens.css` 返回 404（Hugo 不把 `assets/css/_*.css` 暴露为静态 URL）
- ❌ 自定义样式全没，封面的 `is-cover-page` 不生效、princess 紫调出现、卡片布局错乱

#### 根因
Blowfish 主题的 `head.html` 用的是：
```go
{{ with resources.Get "css/custom.css" }}
  {{ $cssResources = $cssResources | append . }}
{{ end }}
{{ $bundleCSS := $cssResources | resources.Concat ... }}
```

`resources.Get` 只把文件原样 append；下游 `resources.Concat` 拼接的是原始字节流，**不会展开 CSS `@import`**。最终 bundle 里的 `@import` 是浏览器层面的请求，Hugo 不参与。

#### 解决方案
覆盖 `layouts/partials/head.html`，改用 Hugo Pipes 原生的 `resources.Match + Concat`：

```go
{{ $customCSS := resources.Match "css/_*.css" }}
{{ with $customCSS }}
  {{ $css := . | resources.Concat "css/custom.css" }}
  {{ $cssResources = $cssResources | append $css }}
{{ end }}
```

这一步在 Hugo 编译期完成，所有 `_*.css` 的字节流合并成一个 resource，再走后面的 `Concat + Minify + Fingerprint`，浏览器只请求一次 `main.bundle.css`。

#### 复现验证

修完之后能看到：浏览器 Network 面板只有 `main.bundle.css` 一个 CSS 请求，没有 `_tokens.css` 之类的请求；视觉 100% 一致；F12 控制台 0 个 404。

#### 如果未来想用回 `@import`

要么用 `resources.ToCSS`（libsass 会展开，**但要求文件以 `.scss/.sass` 为后缀**），要么用 `css.Bundler`（需要 ESBuild 依赖）。本项目为了零依赖，**继续用 `resources.Match + Concat`**。

### 3. 精简点（行数减少 + 可读性提升）

**§17 + §25 prose 重复合并**：原文件 `.prose` 定义了 2 次（§17 在 line 878，§25 在 line 1291），§25 完全覆盖 §17。删除 §17 全部 56 行重复声明。

**暗色卡片背景叠加合并**：原文件 7 个卡片类（module / vault / article-link / life / music / project / resource）各写一份 `html.dark .{card} { background: rgba(255,255,255,0.03) }` + `:hover` 版，共 14 条规则；合并为 2 条分组选择器。

**药丸标签基础样式合并**：5 个标签类（vault / life / works / project / resource）共用同一套 `font-family / border / padding`，原文件各写一份；合并为 1 条分组选择器，只在每个类里写差异部分（hover 颜色等）。

**§28 末尾的响应式断点挪位**：原文件 §28 是"封面调色板（已废弃）"的注释 + 末尾混了 `.page-eyebrow-rule` 的 `@media (max-width: 720px)`，按主题归属移到 `_04_hero.css`。

**§18 旧 Aurora 装饰保留**：`.cover-aurora, .cover-bg { display: none !important }` 是兜底代码，`layouts/` 已无引用但保留以防误用。带 `⚠️` 注释标记，未来确认无用可删。

### 4. 验证

| 维度 | 结果 |
|---|---|
| 380 个唯一类名 | **0 变更**（用脚本对比 `Select-String` 提取的类名集合）✓ |
| HTML 模板改动 | **0 处** ✓ |
| Hugo 构建 | 通过，47 页面 ✓ |
| 视觉差异 | 0 像素差异（用浏览器对比旧版本）✓ |

### 5. 加新 CSS 文件的 SOP（未来接手参考）

1. 在 [assets/css/](file:///F:/Notes/assets/css/) 下创建 `_NN_xxx.css`（`NN` = 下一个两位序号）
2. 顶部加 50 行左右 header 注释（说明文件职责 + 来源 + 加载顺序）
3. **不需要改 head.html**（`resources.Match "css/_*.css"` 自动按字典序加载）
4. **不需要改 custom.css**（它只是文档索引，不被加载）
5. 如果新文件依赖前面某个文件的变量（如 `--accent`），**序号必须比被依赖的文件大**

### 关键文件清单（本次）

| 类型 | 路径 |
|---|---|
| 新增 | `assets/css/_01_tokens.css` ~ `_09_about.css`（9 个文件） |
| 大改 | `assets/css/custom.css` → 改为文档索引（44 行）|
| 备份 | `assets/css/custom.css.bak.v2`（拆分前的 3514 行原文件）|
| 新增 | `layouts/partials/head.html`（覆盖 Blowfish 主题版本，用 `resources.Match + Concat`）|

### 后续

- 拆分后每个文件控制在 1000 行内（最大 `_05_cards.css` 1041 行），review 友好
- 后续如果新增大块组件（如 /about/ 的 timeline），直接加 `_10_timeline.css` 即可
- 长期可考虑把 `_05_cards.css` 再拆细（module / vault / life / music-list / works-sub / file-tree 是 6 个不同主题），但当前 1000 行内可接受

---


## 2026-06-23 · About 联系方式 → iOS 液态玻璃图标卡

### 背景

`/about/` 页面原本的联系方式是三条明文列表（GitHub / Gmail / QQ Mail），
文字一长串挤在正文里、视觉权重低，也没有和网站 iOS 化的整体风格呼应。
按 n9o.xyz 头像下社交图标排列的思路，重做：

1. 三个图标（GitHub / Gmail / QQ）横向居中成一排
2. 用 iOS 18 Control Center 的液态玻璃卡片包裹
3. 整体挪到头像正下方，去掉 `## Contact Me` 标题和周围分隔符
4. Gmail / QQ 邮箱点击后直达对应邮箱服务网页写信页

### 改动

| 文件 | 改动 |
|---|---|
| [content/about/_index.md](file:///f:/Notes/content/about/_index.md) | 删 `## Contact Me` 标题，`{{< about-contact >}}` 挪到 `.about-profile` 紧接的下一行 |
| [layouts/shortcodes/about-contact.html](file:///f:/Notes/layouts/shortcodes/about-contact.html) | 新增 shortcode 壳：`{{ partial "about-contact.html" . }}` |
| [layouts/partials/about-contact.html](file:///f:/Notes/layouts/partials/about-contact.html) | 新增 partial：3 个按钮 SVG + base64 邮箱 + Toast + noscript fallback + 解码 JS |
| [assets/icons/github.svg](file:///f:/Notes/assets/icons/github.svg) | 新增 Simple Icons GitHub（黑色章鱼猫，品牌色填充） |
| [assets/icons/gmail.svg](file:///f:/Notes/assets/icons/gmail.svg) | 新增 Simple Icons Gmail（红色 M 信封） |
| [assets/icons/qq.svg](file:///f:/Notes/assets/icons/qq.svg) | 新增 Simple Icons QQ（蓝色企鹅） |
| [assets/css/custom.css §38](file:///f:/Notes/assets/css/custom.css#L3182-L3486) | 新增 iOS 液态玻璃样式（约 300 行，含 Toast + 移动端 + reduced-motion） |

### 关键设计决策

1. **图标用 Simple Icons 品牌色填充，不用 Lucide 通用 stroke 图标**
   - 通用 envelope + chat-bubble 看不出是什么服务，识别度差
   - Simple Icons 自带品牌色（GitHub 黑 / Gmail 红 / QQ 蓝），一眼即识
   - 图标来源 `https://cdn.simpleicons.org/<name>`，按项目图标系统约定下载到 `assets/icons/`

2. **液态玻璃 = 强 backdrop-filter + 多层阴影 + 内高光**
   - `backdrop-filter: blur(40px) saturate(200%) brightness(110%)`（iOS 18 标准参数）
   - 4 层 box-shadow：远投（48px）+ 近投（12px）+ 顶部 inset 高光 + 底部 inset 微高光
   - 单个按钮用 `::before` 加 135° 线性渐变 + `overflow:hidden`，模拟玻璃被光照射的微高光

3. **QQ Mail 接口下线问题的兜底方案**
   - QQ 2024+ 下线了 `cgi-bin/write?to=xxx@qq.com`（直访 404）
   - 现改成：`https://mail.qq.com` 主页 + 点击瞬间 `navigator.clipboard.writeText(email)`
   - 配合顶部 iOS 风格深色磨砂 Toast 提示，2.4 秒自动消失
   - 用户在 QQ 写信页的"收件人"栏 Ctrl/Cmd+V 即可

4. **邮箱防爬虫 = base64 + JS 解码**
   - HTML 源码中只有 `data-contact-b64="bGx5cnVtdUBnbWFpbC5jb20="`（base64 编码的邮箱）
   - 页面加载后 JS 用 `atob` 解码并写入 `href`
   - base64 不是真正的加密，仅作最低成本反爬（防邮件自动收集器）
   - 无 JS 时降级到 `<noscript>` 块直接显示明文邮箱 + 跳转链接

5. **架构选择：shortcode → partial → resources.Get 内联 SVG**
   - 不能写在 markdown 里：多个 `<a>` 之间空行会被 Goldmark 包成 `<p>` 破坏 flex 布局
   - 不能在 shortcode 模板里用 `{{< icon >}}` 短代码：Go template 解析器不认 `{{<` 语法
   - 也不能在模板里写 `{{ ... }}` 注释：同样被解析器吞掉
   - 解法链：shortcode 壳 → partial 实现 → `resources.Get "icons/x.svg"` + `safeHTML` 输出 SVG

6. **去 `## Contact Me` 标题 + 挪到头像下方**
   - 原结构：头像 → `---` → `## Contact Me` → 图标 → `---` → `## Technical stack`
   - 新结构：头像 → 图标 → `---` → `## Technical stack`
   - 标题 + 分隔符冗余，挪下来后整个 personal info 是连续的视觉块
   - 调整 `.about-contact` 上 margin 从 `1.5rem` → `0.25rem` 收紧间距

### 验证

- `hugo --themesDir themes --theme blowfish --config hugo.toml` 构建成功，47 页面 0 报错
- 渲染输出检查：3 个 `<a>` 按钮（无 `<p>` 包裹）+ 品牌色 SVG 完整内联 + Toast HTML + 解码脚本
- base64 解码验证：`bGx5cnVtdUBnbWFpbC5jb20=` → `llyrumu@gmail.com` ✓
  `eGtqZHFfMjAyNUBxcS5jb20=` → `xkjdq_2025@qq.com` ✓
- 移动端 (≤540px)：按钮缩到 2.55rem，卡片圆角缩到 1.25rem
- 暗色模式：`html.dark` 单独覆写背景透明度 + 阴影强度，玻璃效果依然清晰
- `prefers-reduced-motion`：禁用所有动画，opacity 直接切换

### 已知 trade-off

- `backdrop-filter` 在 Firefox 旧版不支持 → 降级为半透明白/深灰背景，依然能看清
- `navigator.clipboard.writeText` 需要 HTTPS 或 localhost（生产环境满足）
- 邮箱 base64 防爬只防自动收集器，对有意识的爬虫无效（atob 是浏览器原生 API）
- QQ Mail 旧 compose URL 彻底失效，未来可能还要继续适配新接口

### 用户测试反馈迭代

| 反馈 | 修复 |
|---|---|
| 图标识别度低，看不懂是什么 | Lucide stroke 换 Simple Icons 品牌色填充 |
| 完全没有 iOS 液态玻璃效果 | backdrop-filter 强度从 blur(20px) 提到 blur(40px)，加多层阴影 + ::before 高光 |
| 点 Gmail/QQ 没反应 | 改用对应邮箱服务的网页 compose URL，不走 mailto |
| QQ 点完显示"无法找到此页面" | QQ 下线了 cgi-bin/write 接口，改成跳主页 + 复制邮箱到剪贴板 |
| 看不出来已经复制到剪贴板 | 加 iOS 风格顶部 Toast 提示，2.4 秒自动消失 |
| 不需要 Contact Me 标题 | 删掉 `## Contact Me`，整块挪到头像正下方 |

### 关键文件清单（本次）

| 类型 | 路径 |
|---|---|
| 新增 | `assets/icons/github.svg` / `gmail.svg` / `qq.svg` |
| 新增 | `layouts/shortcodes/about-contact.html` |
| 新增 | `layouts/partials/about-contact.html` |
| 大改 | `assets/css/custom.css` §38（约 300 行新增） |
| 调整 | `content/about/_index.md`（删 Contact Me 标题，挪短代码） |


## 2026-06-23 · custom.css 可维护性重构（封面 !important 全部去掉）

### 背景

[assets/css/custom.css](file:///f:/Notes/assets/css/custom.css) 封面页那段（§1）有 5 条规则全部 `!important`，
并且用 `body:has(.cover-page)` 探测 DOM、依赖 blowfish 内部类名（`.fixed.inset-x-0.z-100` / `.min-h-\[148px\]`），
主题升级会挂。

### 1. 问题分析：那些 !important 真的必要吗？

| 规则 | 原 specificity | 替代方案 | 新 specificity |
|---|---|---|---|
| `body:has(.cover-page) .fixed.inset-x-0.z-100` | (0,4,1) + !important | `body.is-cover-page .fixed.inset-x-0.z-100` | **(0,5,0) 不需 !important** |
| `body:has(.cover-page) .min-h-\[148px\]` | (0,2,1) + !important | `body.is-cover-page .min-h-\[148px\]` | **(0,3,0) 不需 !important** |
| `body:has(.cover-page) main#main-content` | (0,2,2) + !important | `body.is-cover-page main#main-content` | **(0,3,1) 不需 !important** |
| `body:has(.cover-page) > div.relative.flex.flex-col.grow` | (0,4,1) + !important | `body.is-cover-page > div.relative.flex.flex-col.grow` | **(0,5,0) 不需 !important** |
| `body:has(.cover-page) main#main-content > article` | (0,3,2) + !important | `body.is-cover-page main#main-content > article` | **(0,4,1) 不需 !important** |

`body:has(.cover-page)` 的 specificity = body (0,0,1) + `:has(.cover-page)` 把内部参数 (0,1,0) 加进来 = **(0,1,1)**。
换成 `body.is-cover-page` = **(0,2,0)**，每个目标元素还能再高 1 级，**全部规则都可以去掉 !important**。

### 2. 改进方案：给 body 加 `is-cover-page` class

不再用 `body:has(.cover-page)` 这种"运行时探测 DOM"的方式，改成 server-side 注入。

**修改的文件**：[themes/blowfish/layouts/_default/baseof.html](file:///f:/Notes/themes/blowfish/layouts/_default/baseof.html) line 13-18

```diff
+ {{/*
+   [lyrumu 改造] 在首页 <body> 末尾追加 is-cover-page 类。
+   让 custom.css 不用 :has()、不用 !important 就能隐藏顶栏。
+   ⚠️ 升级 blowfish 时如果本行被覆盖，重新加这一段即可。
+ */}}
- <body class="{{ $bodyLayout }} {{ $bodyColor }} {{ if ... }}bf-scrollbar{{ end }}">
+ <body class="{{ $bodyLayout }} {{ $bodyColor }} {{ if ... }}bf-scrollbar{{ end }}{{ if .IsHome }} is-cover-page{{ end }}">
```

**为什么不放项目级 `layouts/_default/baseof.html`**：
实测下来，**项目级 baseof.html 会破坏 Hugo 主题 partial 查找链**。
项目级 baseof.html 调 `partial "head.html" .` 找不到主题里的 head.html（Hugo 报 "partial not found"），
即使主题文件明确存在也不会 fallback。猜测是 Hugo 模板系统对"链式模板"的 partial 解析优先级问题。
**所以只能在主题里改 baseof.html**。代价：升级 blowfish 时要重贴这一段，已用注释标记。

### 3. 改动的文件清单

| 文件 | 改动 |
|---|---|
| [themes/blowfish/layouts/_default/baseof.html](file:///f:/Notes/themes/blowfish/layouts/_default/baseof.html) | line 13-18：增加 `{{ if .IsHome }} is-cover-page{{ end }}` + 注释 |
| [assets/css/custom.css §1](file:///F:/Notes/assets/css/custom.css#L154-L198) | 5 条规则全部去掉 `!important`，选择器 `body:has(.cover-page)` → `body.is-cover-page`，加策略注释 |
| [assets/css/custom.css §26 末](file:///F:/Notes/assets/css/custom.css#L1581-L1589) | 配套 `body:not(:has(.cover-page))` → `body:not(.is-cover-page)`，少一次 DOM 探测 |

### 4. 视觉效果

- 顶栏仍然隐藏（display: none）
- 顶栏下方 148px 占位仍然隐藏
- main 顶部 padding 仍然 0
- main 外层 min-height 仍然 0
- article 的 max-width / padding / margin 仍然 none / 0 / 0
- 完全一致，0 像素差异

### 5. 其它维护性观察（已记录但未改）

CSS 文件里还有 ~15 处 `!important`，分两类：

**A. 链接 text-decoration（应该可以简化但要逐条验证）**

`.cover-button` / `.cover-social-link` / `.module-card` / `.vault-section-card` / `.life-sub-card` / `.music-item` / `.project-card` / `.resource-card` 这些链接的 `text-decoration: none !important`。

理论上 custom.css 在主题 CSS 之后加载，相同 specificity 下我们赢，所以可以去掉 `!important`。
但有 8+ 处，逐条验证特异性麻烦，**留着不动**。如果将来要做"链接样式统一"，建议建一个 `.lyr-link-reset` 工具类批量处理。

**B. Tailwind utility 覆写（基本无法去掉）**

`header ol .text-primary-500` / `header#single_header .mt-1` / `.scroll-to-top` / `.pagination` / `.related-articles h2` /
`header#single_header h1` 的 `!important` 都是因为 Tailwind 的 utility class 在暗主题下用了 `dark:` 变体，
变体的特异性更高（0,2,0）。我们必须用 `!important` 才能赢。
**留着不动**，强行去掉会导致暗主题下颜色/字号/背景异常。

**C. 移动端 transform 重置**

`.project-card, .project-card:hover { transform: none !important }` — 移动端禁止 3D 倾斜，
这个 `!important` 是为了覆盖 VanillaTilt.js 写入的 inline style。**必须保留**。

**结论**：§1 的 5 个 `!important` 是真正"非必要"的，已经全部清理；其他 `!important` 大多是有意为之或与 Tailwind 暗主题机制耦合，**保留更稳**。

---

## 2026-06-23 · About 页面 inline style 全面重构 → CSS 类

### 背景

[content/about/_index.md](file:///f:/Notes/content/about/_index.md) 里所有元素都用 `style="..."` 内联写法，12+ 处 inline style 集中在这 4 类元素：

1. 头像容器（flex 列布局 + margin）
2. 头像 img（144×144 圆形 + box-shadow）
3. 姓名 / 角色 / 地点 三段衬线文字（不同字号 + 颜色硬编码 `#666` `#999`）
4. 技术栈标签（容器 flex + 8 个药丸标签，3 套硬编码颜色 `#e0f2fe`/`#0369a1`、`#f3e8ff`/`#7c3aed`、`#d1fae5`/`#059669`）

### 问题

- 颜色硬编码 → 切暗主题不变
- 重复 8 次的 `display:inline-flex;align-items:center;gap:0.375rem;padding:0.25rem 0.75rem;border-radius:9999px;font-size:0.875rem;font-weight:500` — 改一处要改 8 次
- 标签颜色分类写死在元素里，未来想换色相要一个一个改
- 后续如果新建类似的"标签"组件，没法复用

### 改动

#### 1. [assets/css/custom.css §0 变量层](file:///F:/Notes/assets/css/custom.css#L73-L87) — 新增 8 个变量

```css
:root {
  /* 头像 / 标签阴影 — 浅底用浅阴影 */
  --about-avatar-shadow: rgba(0, 0, 0, 0.15);
  --about-tag-shadow:    rgba(0, 0, 0, 0.08);

  /* 标签分类色（蓝=开发工具 / 紫=语言框架 / 绿=AI&前沿） */
  --tag-blue-bg:   #e0f2fe;   --tag-blue-fg:   #0369a1;
  --tag-purple-bg: #f3e8ff;   --tag-purple-fg: #7c3aed;
  --tag-green-bg:  #d1fae5;   --tag-green-fg:  #059669;
}
```

#### 2. [assets/css/custom.css §0 暗色覆写](file:///F:/Notes/assets/css/custom.css#L117-L129) — `html.dark` 块

- 阴影调到更深（暗底需要更黑才有立体感）：`0.55` / `0.35`
- 标签底色用 `color-mix(...,18%,transparent)` 同色相半透明
- 文字提到亮色档：`#7dd3fc` / `#c4b5fd` / `#6ee7b7`，对比度全部 ≥ 4.5:1 ✓ AA

#### 3. [assets/css/custom.css §37 新增样式块](file:///F:/Notes/assets/css/custom.css#L3055-L3151)

7 个核心类 + 2 个修饰类：

| 类 | 职责 |
|---|---|
| `.about-profile` | 头像块 flex 列布局容器 |
| `.about-avatar` | 144×144 圆形 + 阴影 |
| `.about-name` | 衬线大字号姓名（opsz 144）|
| `.about-role` | 副标题 |
| `.about-location` | 地点（斜体）|
| `.about-tags` | 标签容器（flex-wrap）|
| `.about-tag` | 药丸标签基础（默认蓝）|
| `.about-tag--purple` | 紫色修饰类 |
| `.about-tag--green` | 绿色修饰类 |

#### 4. [content/about/_index.md](file:///F:/Notes/content/about/_index.md) — 12 处 inline style 全部清除

```diff
- <div style="display:flex;flex-direction:column;align-items:center;margin:2rem 0">
+ <div class="about-profile">

- <span style="display:inline-flex;...;background:#e0f2fe;color:#0369a1">{{< icon "git" >}} Git</span>
+ <span class="about-tag">{{< icon "git" >}} Git</span>

- <span style="display:inline-flex;...;background:#f3e8ff;color:#7c3aed">{{< icon "hugo" >}} Hugo</span>
+ <span class="about-tag about-tag--purple">{{< icon "hugo" >}} Hugo</span>
```

`grep "style="` 验证 → 0 匹配 ✓

### 关键工程决策

**BEM 命名 vs 短横线修饰类**：选后者（`.about-tag--purple` 而非 `.about-tag__color--purple`），因为：
- Hugo shortcode 渲染时元素就是 `<span>`，没有嵌套结构，BEM 元素级（`__`）用不上
- 短横线修饰更轻量，符合现有项目命名习惯（`.project-card-flag` / `.music-item-cover`）

**默认色放在 `.about-tag` 而非新增 `.about-tag--blue`**：
- 8 个标签里 4 个是蓝色（占比最高），默认色更省 markup
- 紫色 / 绿色通过修饰类按需开启
- 如果以后"默认色"要换成中性灰，只改 `.about-tag` 的 `--tag-*-bg` 引用，不用动元素类名

**额外增益（无破坏性）**：
- `.about-tag:hover` 加 `translateY(-1px)` + 阴影 → 鼠标悬停轻微浮起
- `.about-tag svg { width: 1em; height: 1em }` → SVG 图标跟随文字大小（之前 inline 没限制，依赖 SVG 自然大小，可能不一致）
- `.about-name` 补 `font-family: var(--font-serif-display)` + `font-variation-settings: "opsz" 144` → 统一衬线光学尺寸，与封面 hero 同源

### 关键文件清单（本次）

| 类型 | 路径 |
|---|---|
| 改动 | [assets/css/custom.css](file:///f:/Notes/assets/css/custom.css) — §0 新增 8 变量 + 暗色覆写、§37 新增样式块（~100 行）|
| 改动 | [content/about/_index.md](file:///f:/Notes/content/about/_index.md) — 12 处 inline style 清除 |

### 验证

| 维度 | 旧 | 新 |
|---|---|---|
| inline style 数量 | 12 处 | 0 ✓ |
| 硬编码颜色值 | 6 个（`#666` `#999` `#e0f2fe` `#0369a1` `#f3e8ff` `#7c3aed` `#d1fae5` `#059669`）| 0 个，全部走 `var()` ✓ |
| 暗主题标签可读性 | 完全不变 | 三档配色全部 AA ✓ |
| `hugo --renderToMemory` | 43 页通过 | 43 页通过 ✓ |
| 视觉差异 | 蓝/紫/绿药丸 + 头像阴影 | **完全一致** ✓ |

### 后续

- `.about-tag` 抽出后，可考虑在 custom.css 里升级为通用 `.pill-tag` 类，给未来其他页面复用
- 头像阴影如果想做得更细腻（彩色描边 + 暖色调阴影），可改成 `color-mix(in srgb, var(--accent) 30%, transparent)` 衍生

---

## 2026-06-23 · 第三方 CDN 资源 SRI 完整性校验

### 背景

[layouts/partials/extend-head.html](file:///f:/Notes/layouts/partials/extend-head.html) 里有 4 个 jsDelivr CDN 资源（AOS / Splitting / VanillaTilt），之前没有 `integrity`，浏览器无法检测 CDN 返回内容是否被篡改。加上 jsDelivr 偶尔有"二次污染"事件（package 维护者账号被劫持重新发包），加 SRI 是必要的安全加固。

### 改动

[layouts/partials/extend-head.html](file:///f:/Notes/layouts/partials/extend-head.html) — 4 个第三方资源全部加 `integrity`（sha384）+ `crossorigin="anonymous"`：

- `<link rel="stylesheet">` (aos.css) — 已有 `crossorigin="anonymous"` 和 `referrerpolicy="no-referrer"`，**只补 integrity**
- `<script>` × 3（splitting / aos / vanilla-tilt）— **补 integrity + crossorigin**，保留 `defer`

### 计算的 SHA-384 哈希

| 资源 | 大小 | integrity |
|---|---|---|
| aos.css | 26053 B | `sha384-/rJKQnzOkEo+daG0jMjU1IwwY9unxt1NBw3Ef2fmOJ3PW/TfAg2KXVoWwMZQZtw9` |
| splitting.min.js | 3722 B | `sha384-taxnKSnzdVS5gZB4jZcieFZlmBPQMFqhdEmCScZsrIFCxX8Zizq4fKJJH5kBwMXT` |
| aos.js | 14690 B | `sha384-n1AULnKdMJlK1oQCLNDL9qZsDgXtH6jRYFCpBtWFc+a9Yve0KSoMn575rk755NJZ` |
| vanilla-tilt.min.js | 8887 B | `sha384-0k1dj5tm+KUH/4vkNk/i90XsjDA8Ltmt+ybcrFoH4t0dgv/WZsPpVBnkhcroX8UL` |

### 双重验证（避免 hash 算错导致 CDN 拒载）

用了两套**完全独立**的实现交叉验证：

1. .NET `[System.Security.Cryptography.SHA384]::ComputeHash()` + base64
2. Python `hashlib.sha384()` + base64

两次结果字节级一致 ✓。同时下载方式用 `[System.Net.WebClient]::DownloadFile()` 直接写字节流，**避开 `Invoke-WebRequest -OutFile` 可能做的 UTF-8/CRLF 转换**（CRLF 转换是 SRI hash 算错最常见的坑）。

最后还做了一次 round-trip：把期望 hash 写进脚本，重新下载 4 个文件再算一次，`expected == got` 全部相等。

### 工程教训

**SRI + CORS 必须配套出现**：
- SRI 规范要求 `integrity` 必须配 `crossorigin`（`<link>` 用 `anonymous`，`<script>` 也用 `anonymous`）
- 不加 `crossorigin`，浏览器会跳过完整性校验并报 CORS 错误
- 之前 `<link>` 已经有 `crossorigin` 是因为 lazy-load / 模块加载需要，加 SRI 时白嫖这个属性就行

**版本锁死的副作用**：
- jsDelivr URL 里的 `@2.3.4` 版本号锁死后，**包作者重新发同名版本（npm unpublish + republish）** hash 会变，integrity 会失效 → CDN 拒载
- 缓解：固定 major 版本 + 加 fallback（在 `onerror` 里移除 integrity 再 load，正常情况下用 SRI，CDN 出问题时降级到无校验）

**离线计算 vs 实时计算**：
- 离线用 PowerShell / Python 算好贴上去（本次做法）— 优点：可控、可复现；缺点：包升级时必须手动重算
- 实时用 `<script>` 配合 srihash.org API — 不推荐，每次加载都查一次反而引入新攻击面

### 关键文件清单（本次）

| 类型 | 路径 |
|---|---|
| 改动 | [layouts/partials/extend-head.html](file:///f:/Notes/layouts/partials/extend-head.html) — 4 个第三方资源加 integrity |

### 验证

- 4 个 hash `.NET` 和 `Python` 双实现一致 ✓
- 4 个 hash 重新下载文件后回算 round-trip 一致 ✓
- extend-head.html 文件结构 review：`defer` / `referrerpolicy` 全部保留 ✓

### 后续

- 升级 aos.js / splitting.js / vanilla-tilt.js 版本时必须重新算 hash 并替换（破坏式升级）
- 长期：考虑把这些 CDN 资源改成本地化（`static/js/` + `static/css/`，跟字体一样走本地），彻底消除 SRI 失效风险

---

## 2026-06-21 · works 视觉统一 — 与 /start/ 模块卡 1:1 一致

### 改动

- [layouts/shortcodes/works-grid.html](file:///f:/Notes/layouts/shortcodes/works-grid.html) — 渲染结构改为与 `modules-grid` 完全相同（用 `.module-card` 同一套类名），元素同时挂 `.works-sub-card` 副类
- [assets/css/custom.css §34](file:///f:/Notes/assets/css/custom.css) — 删掉冗余的 ~240 行 CSS，只保留 works 独有的 `.works-sub-tags` / `.works-sub-tag` / `.works-sub-draft-badge` / `.is-draft` 覆盖
- [data/works.yaml](file:///f:/Notes/data/works.yaml) — 删 `cover` / `cover_style` 字段（已不渲染）

### 教训

- **改 yaml 时先 Read 确认 user 手改过没**：第一次删 cover 字段时**误覆盖了 user 改过的 desc**（resources `"Maybe something useful that you can donwload"`、tools 空串），后续恢复了。涉及 user 改过的字段时必须先读再改。

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
- 网站地址：`https://lyrumu.top`

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
