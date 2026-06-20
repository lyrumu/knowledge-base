# 项目地图 — 个人网站 `f:\Notes\`

> 最后更新：2026-06-19 · Hugo v0.163.2 · Blowfish v2

---

## 1. 这是什么

一个基于 **本地 Obsidian Vault** 驱动的 **Hugo 静态站点**，部署在 **Cloudflare Pages**。
所有文章用 Obsidian 写 → 跑同步脚本 → `git push` → 自动部署上线。

---

## 2. 快速查阅：我想改什么 → 改哪个文件

| 我想…… | 改这个文件 |
|---------|-----------|
| 改封面的标题 / subtitle / 按钮文案 | [`data/cover.yaml`](file:///f:/Notes/data/cover.yaml) |
| 改封面的颜色（明/暗两套） | [`data/cover.yaml`](file:///f:/Notes/data/cover.yaml) 的 `palette.light` / `palette.dark` |
| 改封面的字距 / 大小 / 花边位置 | [`assets/css/custom.css §28`](file:///f:/Notes/assets/css/custom.css) |
| 改内页"小封面"的文案 | 对应 `content/xxx/_index.md` 的 frontmatter `kicker / subtitle` |
| 换 /start/ 大厅的模块卡 | [`data/modules.yaml`](file:///f:/Notes/data/modules.yaml)（加/删条目改 `items` 数组） |
| 换 /notes/ 的分类卡 | [`data/vault.yaml`](file:///f:/Notes/data/vault.yaml) |
| 加一个 Lucide icon | [`layouts/partials/cover/icon.html`](file:///f:/Notes/layouts/partials/cover/icon.html) 加 `else if` 分支 |
| 改顶栏的菜单项 | [`hugo.toml`](file:///f:/Notes/hugo.toml) 的 `[[menu.main]]` 段 |
| 加一篇新文章 | 见下方 §4 |
| 写 CSS（字体 / 颜色 / 间距） | [`assets/css/custom.css`](file:///f:/Notes/assets/css/custom.css) |
| 改文章内容样式 | `assets/css/custom.css` 搜索 `§ prose` 段 |
| 改"亮色" / "暗色" 主题的 CSS | `assets/css/custom.css` 顶部 `:root`（亮）和 `html.dark`（暗） |
| 部署 / 更新站点 | 见 [`DEPLOY.md`](file:///f:/Notes/DEPLOY.md) |

---

## 3. 项目心智模型

```
你在 Obsidian 里写 `# 标题\n内容`（Vault/）
        │
        ▼
  vault-to-hugo.ps1（自动发现 .md，创建 Hugo leaf bundle）
        │
        ▼
  Hugo（渲染模板 + 数据 + CSS → 完整 HTML 站）
        │
        ▼
  你 `git push`
        │
        ▼
  Cloudflare Pages（自动构建 + 部署）
```

---

## 4. 文件结构总览

```
f:\Notes\
├── hugo.toml                       # 全局 Hugo 配置
├── DEPLOY.md                       # 部署与维护指南
├── PROJECT_MAP.md                  # ← 你正在看（本地保留）
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
│   │   ├── docs/                   # Docs 分类（含 vscode, wsl2, docker 等嵌套）
│   │   ├── language/               # Language 分类（含 cpp, python）
│   │   ├── demo/                   # Demo 分类（含 minecraft, aipython）
│   │   └── tools/                  # 工具脚本页面
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
│       ├── file-tree.html          # 可折叠文件树
│       └── section-rule.html       # ✦ 分隔符
│
├── scripts/                        # ★ 运维脚本
│   └── vault-to-hugo.ps1           # Vault → Hugo 同步（日常使用）
│
├── static/                         # 静态资源
│   ├── fonts/                      # 字体文件（本地化）
│   ├── image/                      # 装饰 PNG（花边 / 花朵）
│   └── notes-assets/               # 可下载资源（aipython, minecraft, tools）
│
├── themes/blowfish/                # 主题本体（一般不改）
│
├── DONE.md                         # 开发日志（本地保留）
└── .trae/rules/个人网站开发规则.md   # 项目宪法
```

---

## 5. 部件对应速查

### 封面（`/_index.md`）

| 元素 | 数据源 | 模板 |
|------|--------|------|
| 封面排版 / 社交链接 / 花边 | [`data/cover.yaml`](file:///f:/Notes/data/cover.yaml) | [`layouts/partials/home/custom.html`](file:///f:/Notes/layouts/partials/home/custom.html) |
| 封面 CSS（字体 / 调色 / 布局） | — | [`assets/css/custom.css §28`](file:///f:/Notes/assets/css/custom.css) |
| 封面主题切换按钮 | — | 内嵌在 `custom.html` 的 JS |
| 封面装饰元素（四角花朵） | — | 直接用 `static/image/` 下的 png |
| 封面调色（明 / 暗） | `cover.yaml` → `palette` | `custom.html` 的 `<style>` 块 |

### 内页"小封面"（section 主页顶部）

| 元素 | 数据源 | 模板 |
|------|--------|------|
| kicker / subtitle / eyebrow | 各 `_index.md` frontmatter | [`layouts/partials/cover/page-hero.html`](file:///f:/Notes/layouts/partials/cover/page-hero.html) |
| 短代码调用 | — | [`layouts/shortcodes/page-hero.html`](file:///f:/Notes/layouts/shortcodes/page-hero.html) |
| CSS | — | `custom.css §20 page-hero` |

### /start/ 大厅

| 元素 | 数据源 | 模板 |
|------|--------|------|
| 模块卡列表 | [`data/modules.yaml`](file:///f:/Notes/data/modules.yaml) | [`layouts/shortcodes/modules-grid.html`](file:///f:/Notes/layouts/shortcodes/modules-grid.html) |
| icon | `modules.yaml` → `icon` | 走 `cover/icon.html` 解释为 Lucide SVG |

### /notes/ 分类页

| 元素 | 数据源 | 模板 |
|------|--------|------|
| 分类卡列表 | [`data/vault.yaml`](file:///f:/Notes/data/vault.yaml) | [`layouts/shortcodes/vault-sections.html`](file:///f:/Notes/layouts/shortcodes/vault-sections.html) |

### 顶栏

| 元素 | 数据源 | 模板 |
|------|--------|------|
| 菜单项 | `hugo.toml` → `[[menu.main]]` | 主题默认 |
| GitHub 按钮 | `data/cover.yaml` → `repo_url` | [`desktop-menu.html`](file:///f:/Notes/layouts/partials/header/components/desktop-menu.html) / [mobile-menu.html](file:///f:/Notes/layouts/partials/header/components/mobile-menu.html) |

---

## 6. 调试 / 部署

| 事项 | 说明 |
|------|------|
| 本地预览 | `hugo server --themesDir themes --theme blowfish --config hugo.toml --bind 127.0.0.1 --port 1313` |
| 生产构建 | `hugo --minify --themesDir themes --theme blowfish --config hugo.toml` |
| vault 同步 | `powershell -File scripts/vault-to-hugo.ps1` 或加 `-Watch` 持续监听 |
| 部署到 Cloudflare Pages | 详见 [DEPLOY.md](file:///f:/Notes/DEPLOY.md) |
| 已知警告（Hugo + Blowfish 不兼容） | 正常，可忽略；详见 `.trae/rules/个人网站开发规则.md` |

---

## 7. 常见修改路径

### 换字体

1. 下载字体文件 → 丢进 `static/fonts/`
2. [`assets/css/custom.css §3`](file:///f:/Notes/assets/css/custom.css) 的 `@font-face` 块里加一行
3. 想改正文就改 `--font-sans`，想改标题就改 `--font-serif`

### 换颜色主题

1. 亮色：改 `assets/css/custom.css` 的 `:root { --color-xxx: … }`
2. 暗色：改同一文件的 `html.dark { --color-xxx: … }`
3. 封面调色：改 `data/cover.yaml` 的 `palette.light` / `palette.dark`

### 加 Lucide icon

在 [`layouts/partials/cover/icon.html`](file:///f:/Notes/layouts/partials/cover/icon.html) 加一个分支：

```html
{{ else if eq $name "github" }}
<svg><!-- 这里的 Lucide SVG path --></svg>
```

然后在 yaml 的 `icon` 字段写 `github` 即可。

### 改页面的 section layout

所有 section 主页（/start/ /notes/ /works/ /life/ /about/）都走 [`layouts/_default/list.html`](file:///f:/Notes/layouts/_default/list.md)。每个页面的 `_index.md` 可以设自己的 `kicker` / `subtitle`。
