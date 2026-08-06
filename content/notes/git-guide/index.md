---
# =============================================================================
# 基础信息（必填）
# =============================================================================
title: "Personal Project Git Management"
date: 2026-07-15
draft: false
description: "Git 初始化、日常更新、出错回滚、Remote 管理、.gitignore 实践"

# =============================================================================
# URL 与权重（slug 留空 = 使用文件夹名）
# =============================================================================
slug: ""
weight: 0

# =============================================================================
# 分类与标签
# =============================================================================
tags: [git, project]
categories: [development, devops]
topics: []
series: []

# =============================================================================
# 作者信息
# =============================================================================
showAuthor: true

# =============================================================================
# 日期
# =============================================================================
showDate: true
showDateUpdated: false
dateUpdated: ""

# =============================================================================
# Hero（顶部横幅）
# =============================================================================
showHero: true
heroStyle: "background"
heroBackground: ""
heroImage: ""
heroBackgroundImage: ""

# =============================================================================
# 目录
# =============================================================================
showTableOfContents: true

# =============================================================================
# 阅读信息
# =============================================================================
showReadingTime: true
showWordCount: true

# =============================================================================
# 其他功能
# =============================================================================
showZenMode: true
showRelatedContent: false
relatedContentLimit: 3
sharingLinks: []

# =============================================================================
# 面包屑导航
# =============================================================================
showBreadcrumbs: true

# =============================================================================
# 评论（暂不做）
# =============================================================================
showComments: false

# =============================================================================
# Open Graph / SEO
# =============================================================================
images: []
---

> 目前我常用的git操作流程

---

## 1. 初始化项目为 Git 仓库

### 1.1 在 GitHub 新建仓库

登录 GitHub，点击右上角 `+` → `New repository`，填写仓库名称和描述.

### 1.2 本地初始化

在终端(PowerShell)进入项目目录，执行以下命令：

```powershell
# 依次执行：
git init
git config user.name "YOUR NAME"  # 你的 GitHub 用户名
git config user.email "YOUR EMAIL" # 建议使用 GitHub 提供的隐私邮箱（见 Settings → Emails）
git remote add origin https://github.com/YOUR_NAME/YOUR_REPO_NAME.git
```

> 注意：GitHub 提供隐私邮箱格式 `ID+username@users.noreply.github.com`，可有效避免垃圾邮件。

---

## 2. 日常更新备份仓库

每次在本地完成新的工作并测试无误后，执行以下流程：

### 2.1 确认同步状态

首先在终端进入项目目录，执行 `git fetch && git status`：(先拉取github 防止多设备提交时漏掉状态不一致)

| 输出 | 含义 | 操作 |
|------|------|------|
| `up to date with 'origin/master'` | 本地与仓库同步 | 无需操作 |
| `behind 'origin/master' by X commit` | 本地落后于仓库 | 执行 `git pull` |
| `ahead of 'origin/master' by X commit` | 本地有新内容 | 照常执行 `git push` |

### 2.2 更新仓库

**方式一：一次性提交（推荐）**

```powershell
git add .
git commit -m "Details of new contents"
git push origin master/main
git status  # 最后再检查同步状态
```

**方式二：分批提交（可看到不同文件的提交记录）**

```powershell
git add filename1/
git commit -m "Details_1"
git add filename2/
git commit -m "Details_2"
# 最后统一进行 git push
git push origin master/main
# 这样就能在 GitHub 上看到对每个文件不同的提交信息了
git status
```

> 仅初次提交时可用 `git push -u origin master -f` 避免不必要的麻烦。

---

## 3. 出错回滚特定版本

### 3.1 已经将错误版本提交至 GitHub

查看提交历史：

```powershell
git log --oneline
```

**回退操作：**

- 回退到最新（上一个）提交：`git reset --hard HEAD~1`
- 回退到指定提交：`git reset --hard <commit-id>`

回滚后都需要**强制推送**覆盖远程：

```powershell
git push -f origin master/main
```

### 3.2 还未将错误版本提交至 GitHub

执行以下命令清除本地错误修改：

```powershell
git reset --hard HEAD && git clean -fd
```

然后重新进行正确的工作和代码提交。

### 3.3 回滚个别文件

将某个文件或目录回滚到指定版本的状态（仅修改工作区，不影响提交历史）：

```powershell
git checkout <commit-id> -- FILENAME
```

---

## 4. Remote 与 .gitignore

### 4.1 Git Remote

> ⚠️ **仓库改名后**：在 GitHub 上 rename 了仓库后，本地 `git remote -v` 还是旧地址，**push 前记得先改**：

```powershell
git remote set-url origin YOUR_NEW_URL.git
```

### 4.2 .gitignore 使用

被 `.gitignore` 的文件在本地会变化，但提交时不会上传。

**创建**（Windows：新建文本文件后**把后缀也删掉**）：

```gitignore
.obsidian/workspace.json
config/secret.json
.venv/
*.log
```

**忽略已跟踪的文件**：`gitignore` 只能忽略未被跟踪的文件，已跟踪的需先移除缓存：

```powershell
git rm --cached config/secret.json
git add .gitignore
git commit -m "Ignore config files"
```