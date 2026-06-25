# 部署与维护指南

> 首次部署：2026-06-19 · v1.0.0  
> 最近更新：2026-06-25 · dead code 清理 + CDN 本地化 + scripts/ 冻结  
> 平台：Cloudflare Pages · Hugo v0.163.2 · Blowfish 主题

---

## 一、日常更新内容

### 你只需要做三件事

```
1. 在 content/ 下手写文章（Markdown + frontmatter）
2. hugo server 本地验证
3. git push 部署上线
```

### 详细步骤

#### Step 1：写文章（手写）

在 `content/<section>/<slug>/index.md` 手写 Markdown + frontmatter：
- 图片放 `static/image/<section>/<slug>/*.png`
- 详细 SOP 参见 [PROJECT_MAP.md §7](file:///f:/Notes/PROJECT_MAP.md)

> ⚠️ **2026-06-25 起**：`scripts/vault-to-hugo.ps1` 已冻结，不再日常使用。
> 历史同步脚本仅供回退参考（详见 [scripts/README.md](file:///f:/Notes/scripts/README.md)）。

#### Step 2：本地验证

```bash
hugo server --themesDir themes --theme blowfish --config hugo.toml --bind 127.0.0.1 --port 1313
```

打开浏览器 `http://127.0.0.1:1313/` 预览。

#### Step 3：部署上线

```bash
git add -A
git commit -m "update: 添加/更新了 XXX 文章"
git push
```

Cloudflare Pages 自动检测到 push → 自动构建 → 自动部署（约 2 分钟）

---

## 二、首次部署（已做完，存档用）

> 以下步骤首次已执行完毕，只需了解即可。

### Cloudflare Pages 配置

| 字段 | 值 |
|------|-----|
| Framework preset | Hugo |
| Build command | `hugo --minify --themesDir themes --theme blowfish --config hugo.toml` |
| Build output directory | `/public` |
| Environment variables | `HUGO_VERSION = 0.163.2` |

### Git tag

```bash
git tag -a v1.0.0 -m "初始站点部署"
git push origin v1.0.0
```

---

## 三、加新文章（手写）

```bash
# 创建 leaf bundle 目录
mkdir content/notes/<section>/<slug>
vim content/notes/<section>/<slug>/index.md
```

文章的 frontmatter 参考 [archetypes/default.md](file:///f:/Notes/archetypes/default.md)：

```yaml
---
date: 2026-01-01
draft: false
description: ""
tags: []
categories: []
showHero: true
heroStyle: "background"
---
```

> ⚠️ **2026-06-25 起**：`vault-to-hugo.ps1` 同步脚本已冻结。所有文章改为手写。

---

## 四、加新分类（在 /notes/ 下加 section）

1. 在 `content/notes/<新分类>/_index.md` 建 section 主页
   - frontmatter 含 `title / kicker / subtitle / description`
   - 可选 `cardColumns: 1`（单列）或 3（默认多列）
2. 在 `content/notes/<新分类>/` 下放具体文章（leaf bundle）
3. **不需要改菜单**：`hugo.toml` 的 `[[menu.main]]` 已包含 `/notes/`，新子页通过 `/notes/` 入口可达

> ⚠️ **2026-06-25 起**：旧流程"在 `data/vault.yaml` 中添加 section 定义"已废弃（vault.yaml 已删除）。
> 新流程是直接手写 `_index.md` + frontmatter。

---

## 五、本地开发

```bash
# 本地预览（带热更新）
hugo server --themesDir themes --theme blowfish --config hugo.toml --bind 127.0.0.1 --port 1313

# 生产构建
hugo --minify --themesDir themes --theme blowfish --config hugo.toml
```

---

## 六、项目架构速查

```
f:\Notes\
├── hugo.toml             # 全局 Hugo 配置
├── DEPLOY.md             # 本文件
├── PROJECT_MAP.md        # 项目地图
├── OPTIMIZE.md           # 优化方案 + 决策日志
├── DONE.md               # 开发日志（历史记录，不修改）
├── content/              # 所有页面内容（含 notes 文章、section 主页、子页）
├── data/                 # 数据驱动（封面 / life / music / works / projects / resources）
├── layouts/              # 自定义模板（覆写 Blowfish）
├── assets/css/           # 自定义样式（9 个 _*.css + custom.css 索引）
├── static/               # 字体 / CSS / JS / 图片 / 可下载资源
│   ├── css/aos.css       # ★ 本地化（2026-06-25，原 jsDelivr CDN）
│   ├── js/aos.js         # ★ 本地化
│   ├── js/splitting.min.js  # ★ 本地化
│   ├── js/vanilla-tilt.min.js  # ★ 本地化
│   └── js/music-player.js # 音乐播放器
├── scripts/              # ⚠️ 历史脚本（已冻结，详见 scripts/README.md）
└── themes/blowfish/      # 主题本体（一般不改）
```

想改什么 → 查 [PROJECT_MAP.md](file:///f:/Notes/PROJECT_MAP.md)，里面有逐项对照表。

---

## 七、Hugo 升级维护

当前 Hugo 版本：**0.163.2**（Cloudflare Pages 通过 `HUGO_VERSION` 环境变量指定）

升级步骤：
1. 本地安装新版 Hugo
2. `hugo server` 测试构建无报错
3. 改 Cloudflare Pages 的 `HUGO_VERSION` 环境变量
4. push 触发线上构建验证

---

## 八、常见故障

| 问题 | 原因 | 解决 |
|------|------|------|
| 构建失败：`can't evaluate field Locale` | Hugo 版本不对 | 检查 `HUGO_VERSION` 环境变量 |
| 图片加载 404 | 路径或文件名含中文未转义 | 改用英文 slug 命名 | 
| 样式全没（封面失效、princess 紫调出现） | 不要在 `custom.css` 写 `@import`（见 PROJECT_MAP.md §8） | 用 `resources.Match "css/_*.css"` 机制 | 
| 部署后内容没更新 | push 后 Cloudflare 还在构建 | 等 2-3 分钟再刷新 |