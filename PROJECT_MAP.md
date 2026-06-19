# 项目地图 — 个人网站（lyrumu's site）

> **目的**：让你（或下一次接手的人）一站式知道"想改 X，应该改 Y"。
> **风格**：Claude-inspired 衬线 · 暖白/暗色双主题 · Hugo + Blowfish · 本地化资源 · jsDelivr 第三方库。

---

## 1. 想改内容 → 改哪里

### 1.1 封面（首页 `/`）

| 想改 | 文件 | 关键位置 |
|---|---|---|
| 标题 / kicker / 副标题 / 题词 | [data/cover.yaml](file:///f:/Notes/data/cover.yaml) | `title` / `kicker` / `subtitle` / `epigraph` |
| 入口按钮文字 / 跳转 | [data/cover.yaml](file:///f:/Notes/data/cover.yaml) | `entrance.label` / `entrance.href` |
| 封面社交链接（GitHub/邮箱/…） | [data/cover.yaml](file:///f:/Notes/data/cover.yaml) | `social` 列表 |
| 项目仓库链接（顶栏 GitHub 按钮） | [data/cover.yaml](file:///f:/Notes/data/cover.yaml) | `repo_url` |
| 封面调色（背景渐变 / 各文字色 / 按钮色） | [data/cover.yaml](file:///f:/Notes/data/cover.yaml) | `palette.*` |
| 封面装饰图（四角花朵） | [layouts/partials/home/custom.html](file:///f:/Notes/layouts/partials/home/custom.html) | `cover-flowers` div |
| 顶部 / 底部花边 | [static/image/](file:///f:/Notes/static/image/) | 改 PNG；CSS 同步调整 [custom.css §19](file:///f:/Notes/assets/css/custom.css#L654-L711) |

### 1.2 顶部分类导航

| 想改 | 文件 |
|---|---|
| 顶部分类条目（学习笔记 / 作品 / …） | [hugo.toml](file:///f:/Notes/hugo.toml) → `[[menu.main]]` |
| 分类对应的页面 | `content/<slug>/_index.md` |

### 1.3 大厅页（`/start/`）

| 想改 | 文件 |
|---|---|
| 大厅文字（标题、说明段落） | [content/start/_index.md](file:///f:/Notes/content/start/_index.md) |
| 模块卡（4 个） | [data/modules.yaml](file:///f:/Notes/data/modules.yaml) |
| 模块卡的视觉样式 | [assets/css/custom.css §15](file:///f:/Notes/assets/css/custom.css#L475-L644) |
| 模块卡的 HTML 结构 | [layouts/shortcodes/modules-grid.html](file:///f:/Notes/layouts/shortcodes/modules-grid.html) |

### 1.4 各模块入口页（`/notes/` · `/works/` · `/life/` · `/about/`）

| 想改 | 文件 |
|---|---|
| 页面顶部"小封面"（kicker / 标题 / 副标题） | `content/<slug>/_index.md` 的 frontmatter `kicker` / `subtitle` |
| 页面正文 markdown | `content/<slug>/_index.md` |
| notes 页的 vault 分类卡 | [data/vault.yaml](file:///f:/Notes/data/vault.yaml) |
| vault 卡的视觉样式 | [assets/css/custom.css §16](file:///f:/Notes/assets/css/custom.css#L647-L794) |

### 1.5 整篇文章 / 长文（如 `/notes/docs/example/`）

| 想改 | 文件 |
|---|---|
| 文章正文 | `content/notes/.../<slug>.md` |
| 文章 frontmatter（标题/日期/标签/hero 样式） | 同上，最上面 `---` 块 |
| 文章列表卡样式 | [assets/css/custom.css §23](file:///f:/Notes/assets/css/custom.css#L1075-L1156) |
| 长文 prose（h1-h5 / blockquote / table / code …） | [assets/css/custom.css §25](file:///f:/Notes/assets/css/custom.css#L1244-L1370) |
| TOC 侧栏样式 | [assets/css/custom.css §26](file:///f:/Notes/assets/css/custom.css#L1500-L1512) |

### 1.6 页脚 / 面包屑 / 顶栏

| 想改 | 文件 |
|---|---|
| 页脚 | [assets/css/custom.css §26 #site-footer](file:///f:/Notes/assets/css/custom.css#L1410-L1428) |
| 面包屑 | [assets/css/custom.css §22](file:///f:/Notes/assets/css/custom.css#L1060-L1080) |
| 顶栏主菜单链接 | [hugo.toml](file:///f:/Notes/hugo.toml) → `[[menu.main]]` |
| 顶栏 GitHub 按钮 | [layouts/partials/header/components/desktop-menu.html](file:///f:/Notes/layouts/partials/header/components/desktop-menu.html) |
| 顶栏 GitHub URL | [data/cover.yaml](file:///f:/Notes/data/cover.yaml) → `repo_url` |

---

## 2. 想改样式（颜色 / 字体 / 间距） → 改哪里

### 2.1 颜色 / 主题色

| 想改 | 文件 | 关键变量 |
|---|---|---|
| 整体配色（亮色） | [assets/css/custom.css](file:///f:/Notes/assets/css/custom.css) | `:root` 里的 `--bg-base` / `--fg-base` / `--accent` 等 |
| 整体配色（暗色） | [assets/css/custom.css](file:///f:/Notes/assets/css/custom.css) | `html.dark { … }` 里的同名变量 |
| 封面专属配色（覆盖全局） | [data/cover.yaml](file:///f:/Notes/data/cover.yaml) | `palette.*` |

可调变量列表（按命名约定）：
- `--bg-base` / `--bg-deep`：背景色
- `--fg-base` / `--fg-mute` / `--fg-soft`：前景文字色（由实到虚）
- `--line`：分隔线 / 边框色
- `--accent`：强调色（Claude 橙系）

### 2.2 字体

| 想改 | 文件 |
|---|---|
| 字体定义（@font-face + CSS 变量） | [assets/css/custom.css §0](file:///f:/Notes/assets/css/custom.css#L11-L98) |
| 字体文件本体 | [static/fonts/](file:///f:/Notes/static/fonts/) |
| 字体回退栈 | `--font-serif-display` / `--font-serif-body` / `--font-sans` / `--font-mono` |

> ⚠️ 不要换 CDN：项目规则禁止依赖 Google Fonts CDN。所有字体已经本地化。

### 2.3 整体排版 / 间距 / 字号

- 内页"小封面"：[assets/css/custom.css §21](file:///f:/Notes/assets/css/custom.css#L720-L846)
- 封面"大标题"：[assets/css/custom.css §7](file:///f:/Notes/assets/css/custom.css#L243-L286)
- 文章正文 prose：[assets/css/custom.css §25](file:///f:/Notes/assets/css/custom.css#L1244-L1370)
- 文章列表卡：[assets/css/custom.css §23](file:///f:/Notes/assets/css/custom.css#L1075-L1156)
- 模块卡：[assets/css/custom.css §15](file:///f:/Notes/assets/css/custom.css#L475-L644)
- vault 卡：[assets/css/custom.css §16](file:///f:/Notes/assets/css/custom.css#L647-L794)

### 2.4 响应式断点

- 全局断点：[assets/css/custom.css §27](file:///f:/Notes/assets/css/custom.css#L1505-L1512) （`max-width: 720px`）
- 模块卡移动端：[assets/css/custom.css §15 末尾](file:///f:/Notes/assets/css/custom.css#L644-L660)
- 封面装饰元素：[assets/css/custom.css §19 @media](file:///f:/Notes/assets/css/custom.css#L702-L712)

---

## 3. 想加新内容 → 改哪里

### 3.1 加新模块（顶栏分类）

1. [data/modules.yaml](file:///f:/Notes/data/modules.yaml)：加一项 `modules:`
2. [hugo.toml](file:///f:/Notes/hugo.toml)：加 `[[menu.main]]`
3. 新建 `content/<slug>/_index.md`，frontmatter 写 `kicker` / `subtitle`

### 3.2 加 vault 子分类（如 /notes/docs/ 再加一类）

1. [data/vault.yaml](file:///f:/Notes/data/vault.yaml)：在 `sections:` 加一项
2. 新建 `content/notes/<新分类>/_index.md`（作为子 section 的入口，可选）
3. 在 `content/notes/<新分类>/` 下放具体 `.md` 文章

### 3.3 加新文章

- 在 `content/<section>/.../<slug>.md` 写文章
- frontmatter 模板：[archetypes/default.md](file:///f:/Notes/archetypes/default.md)
- 文章会自动出现在所属 section 的列表里（卡片视图）

### 3.4 加新 icon

1. 打开 [layouts/partials/cover/icon.html](file:///f:/Notes/layouts/cover/icon.html)
2. 在下面 `{{ else if eq $name "xxx" }}` 加一个分支
3. SVG 从 [lucide.dev](https://lucide.dev) 拷过来

### 3.5 加新社交链接（封面底部）

编辑 [data/cover.yaml](file:///f:/Notes/data/cover.yaml) → `social` 列表，每项：
```yaml
- name: "Twitter"
  url: "https://x.com/xxx"
  icon: "twitter"   # icon.html 里注册的 name
  title: "悬停提示"
```

### 3.6 加新章节（在顶栏分类里）

- 跟"加新模块"步骤一样，slug、yaml、hugo.toml 三处同步

---

## 4. 想改 UI 行为 / 动画 → 改哪里

| 想改 | 文件 |
|---|---|
| 封面入场动画（Splitting.js 字符级） | [layouts/partials/home/custom.html](file:///f:/Notes/layouts/partials/home/custom.html) 末尾 `<script>` |
| 内页"小封面"入场动画 | [layouts/partials/cover/page-hero.html](file:///f:/Notes/layouts/partials/cover/page-hero.html) 末尾 `<script>` |
| Splitting.js 注入的样式 | [assets/css/custom.css §20](file:///f:/Notes/assets/css/custom.css#L716-L720) |
| 滚动渐入（`.reveal`） | [assets/css/custom.css §14](file:///f:/Notes/assets/css/custom.css#L458-L472) |
| 卡片悬停效果 | 各 .card 的 `:hover` 规则（同文件各 § 节） |
| 第三方库加载（Splitting.js） | [layouts/partials/extend-head.html](file:///f:/Notes/layouts/partials/extend-head.html) |

> 关闭动画的最快方式：把 `extend-head.html` 里 Splitting.js 的 `<script>` 行注释掉。所有 `.is-ready` / `[data-splitting]` 规则都有 `:not(...)` 降级，移除后页面会立刻显示。

---

## 5. 想换主题 / 模板 → 改哪里

| 想改 | 文件 |
|---|---|
| Hugo 全局配置（baseURL / 主题 / 语言 / 输出格式 / 菜单） | [hugo.toml](file:///f:/Notes/hugo.toml) |
| 主题切换（light / dark 默认行为） | [hugo.toml](file:///f:/Notes/hugo.toml) → `defaultAppearance` / `autoSwitchAppearance` |
| Goldmark markdown 渲染 | [hugo.toml](file:///f:/Notes/hugo.toml) → `[markup]` 段 |
| 代码块高亮（chroma 配色、行号） | [hugo.toml](file:///f:/Notes/hugo.toml) → `[markup.highlight]` |
| 主题本身（一般不要改） | [themes/blowfish/](file:///f:/Notes/themes/blowfish/) （Hugo 升级时跟着升） |
| 自定义模板（覆写主题） | [layouts/](file:///f:/Notes/layouts/) — 路径与主题一致的同名文件会优先 |

> 💡 覆写原则：**不直接改** `themes/blowfish/`，在 `layouts/` 下建同路径文件覆写 — 这样升级主题不会丢你的修改。
> 本项目已覆写的文件：
> - `layouts/_default/list.html`（section 主页用 page-hero）
> - `layouts/partials/home/custom.html`（封面）
> - `layouts/partials/cover/icon.html`（Lucide SVG）
> - `layouts/partials/cover/page-hero.html`（内页 hero）
> - `layouts/partials/header/components/desktop-menu.html`（加 GitHub 按钮）
> - `layouts/partials/header/components/mobile-menu.html`（同上）
> - `layouts/shortcodes/modules-grid.html` · `vault-sections.html` · `page-hero.html` · `section-rule.html`

---

## 6. 调试 / 部署

| 想做 | 命令 / 文件 |
|---|---|
| 本地预览（带 hot reload） | `hugo server --themesDir themes --theme blowfish --config hugo.toml --bind 127.0.0.1 --port 1313` |
| 生产构建 | `hugo --themesDir themes --theme blowfish --config hugo.toml --minify` |
| 杀掉占用的 hugo | `Get-Process \| Where-Object { $_.ProcessName -like "hugo*" } \| Stop-Process -Force` |
| 部署到 Cloudflare Pages | [.github/workflows/cloudflare-pages.yml](file:///f:/Notes/.github/workflows/cloudflare-pages.yml) |
| 已知警告（Hugo + Blowfish 不兼容） | 正常，可忽略；详见 `.trae/rules/个人网站开发规则.md` |

---

## 7. 文件总览（一图流）

```
f:\Notes\
├── hugo.toml                       # 全局 Hugo 配置
├── PROJECT_MAP.md                  # ← 你正在看
├── README.md
├── DONE.md
│
├── assets/css/
│   └── custom.css                  # ★ 所有自定义 CSS（27 大节，颜色 / 字体 / 卡片 / prose …）
│
├── archetypes/
│   └── default.md                  # `hugo new` 模板
│
├── content/                        # ★ 所有页面内容
│   ├── _index.md                   # 封面（极简，只放 layout: page）
│   ├── start/_index.md             # /start/ 大厅
│   ├── notes/                      # /notes/ 学习笔记
│   │   ├── _index.md
│   │   └── docs/example.md         # 样式测试样章
│   ├── works/_index.md             # /works/ 作品
│   ├── life/_index.md              # /life/ 生活
│   └── about/_index.md             # /about/ 关于
│
├── data/                           # ★ 数据驱动（改这里就能改 UI）
│   ├── cover.yaml                  # 封面所有内容 + 调色
│   ├── modules.yaml                # 大厅的模块卡
│   └── vault.yaml                  # /notes/ 的 vault 分类卡
│
├── layouts/                        # ★ 自定义模板（覆写主题）
│   ├── _default/list.html          # section 主页 → page-hero 模式
│   ├── partials/
│   │   ├── cover/icon.html         # Lucide SVG icon 字典
│   │   ├── cover/page-hero.html    # 内页"小封面" partial
│   │   ├── home/custom.html        # 封面 partial
│   │   ├── header/components/
│   │   │   ├── desktop-menu.html   # 加 GitHub 按钮
│   │   │   └── mobile-menu.html    # 加 GitHub 按钮
│   │   └── extend-head.html        # 第三方库（Splitting.js）
│   └── shortcodes/
│       ├── page-hero.html          # {{< page-hero >}} 短代码
│       ├── modules-grid.html       # 大厅模块网格
│       ├── vault-sections.html     # /notes/ 分类网格
│       └── section-rule.html       # ✦ 分隔符
│
├── static/                         # 静态资源
│   ├── fonts/                      # 字体文件（本地化）
│   └── image/                      # 装饰 PNG（花边 / 花朵）
│
├── themes/blowfish/                # 主题本体（一般不改）
│
└── .trae/rules/个人网站开发规则.md   # 项目宪法
```

---

## 8. 最短修改路径速查

| 场景 | 路径 |
|---|---|
| 改封面一句话 | `data/cover.yaml` |
| 改某个模块名 | `data/modules.yaml` |
| 改某个分类入口 | `data/vault.yaml` |
| 改主题色（亮 / 暗） | `assets/css/custom.css` 顶部 `:root` 和 `html.dark` |
| 改卡片样式 | `assets/css/custom.css` §15 / §16 / §23 |
| 改文章长文样式 | `assets/css/custom.css` §25 |
| 改某页文案 | `content/<section>/<slug>.md` |
| 加新分类（顶栏） | `data/modules.yaml` + `hugo.toml` + `content/<slug>/_index.md` |
| 加新 icon | `layouts/partials/cover/icon.html` 加分支 |
| 关掉封面动画 | `layouts/partials/extend-head.html` 注释 Splitting.js |

---

> 写于：2026-06-19
> 维护提示：改了文件结构时，记得回头同步本文档的"文件总览"和"最短路径"两节。