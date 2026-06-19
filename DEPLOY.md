# 部署与维护指南

> 首次部署：2026-06-19 · v1.0.0  
> 平台：Cloudflare Pages · Hugo v0.163.2 · Blowfish 主题

---

## 一、日常更新内容

### 你只需要做三件事

```
1. 在 Obsidian 写文章
2. 终端运行脚本同步
3. git push 部署上线
```

### 详细步骤

#### Step 1：写文章（Obsidian）

在 `/Vault/` 里正常写笔记，图片放在同目录的 `image/` 文件夹。

#### Step 2：同步到 Hugo

```bash
# 在项目根目录执行
powershell -File scripts/vault-to-hugo.ps1
```

脚本会自动：
- 扫描 `/Vault/` 下所有 `.md` 文件
- 按 Vault 中的目录层级创建对应的 Hugo leaf bundle
- 把 `image/` 文件夹一起复制过去
- 只更新有改动的文件（幂等，< 1 秒）

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

## 三、加新文章

### 方式 A：通过 vault-to-hugo 脚本（推荐）

1. 在 `/Vault/` 对应目录下新建 `.md` 文件
2. 参照现有文章格式：一级标题 `# 标题` 开头，图片放在同级 `image/` 目录
3. 运行同步脚本：`powershell -File scripts/vault-to-hugo.ps1`
4. 脚本会自动在 `/content/notes/` 下生成对应的 leaf bundle
5. 提交推送即可

### 方式 B：手动创建 Hugo 文章

```bash
# 创建 leaf bundle
mkdir content/notes/docs/新文章名
vim content/notes/docs/新文章名/index.md
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

---

## 四、加新分类

如果想在 `/notes/` 下加一个全新的大分类（如 `design/`）：

1. 在 [data/vault.yaml](file:///f:/Notes/data/vault.yaml) 中添加 section 定义
2. 在 [hugo.toml](file:///f:/Notes/hugo.toml) 中确认是否需要加新的 `[[menu.main]]` 条目
3. 新建 `content/notes/<新分类>/_index.md`
4. 在 `content/notes/<新分类>/` 下放具体文章（leaf bundle）

---

## 五、本地开发

```bash
# 本地预览（带热更新）
hugo server --themesDir themes --theme blowfish --config hugo.toml --bind 127.0.0.1 --port 1313

# 生产构建
hugo --minify --themesDir themes --theme blowfish --config hugo.toml

# 带着 vault 同步脚本一起 (在另一个终端)
powershell -File scripts/vault-to-hugo.ps1 -Watch
```

> `-Watch` 模式下脚本每 5 秒扫描一次 Vault 变更，配合 `hugo server` 实现 Obsidian 保存 → 浏览器自动刷新。

---

## 六、项目架构速查

```
f:\Notes\
├── vault-to-hugo.ps1     ← 同步脚本（零配置自动发现）
├── hugo.toml             ← 全局 Hugo 配置
├── DEPLOY.md             ← 本文件
├── content/notes/        ← 所有文章 leaf bundle（由脚本维护）
├── data/                 ← 封面 / 模块 / vault 分类数据
├── layouts/              ← 自定义模板（覆写 Blowfish）
├── assets/css/           ← 自定义样式（全部 DIY 在这）
├── static/               ← 字体 / 图片 / 可下载资源
└── .github/workflows/    ← CI（hugo-build.yml 只做构建验证）
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
| 同步脚本中文报错 | 脚本缺少 UTF-8 BOM | 用 VS Code 打开 → 另存为 UTF-8 with BOM |
| 部署后内容没更新 | 忘记跑同步脚本 | `powershell -File scripts/vault-to-hugo.ps1` 后再 push |
