---
# =============================================================================
# 基础信息（必填）
# =============================================================================
title: "python包开发"
date: 2026-06-20
draft: false
description: ""

# =============================================================================
# URL 与权重（slug 留空 = 使用文件夹名）
# =============================================================================
slug: ""
weight: 0

# =============================================================================
# 分类与标签
# =============================================================================
tags: [python, vscode, venv, pip, setuptools]
categories: [development]
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
# - heroStyle: "background" / "basic" / "big" / "thumbAndBackground"
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
showEdit: false
showZenMode: true
showRelatedContent: true
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
# externalUrl: ""

# =============================================================================
# 布局覆写（留空 = 使用主题默认）
# =============================================================================
layout: ""
---

## 环境准备

在 VSCode 扩展商店搜索 `python`，安装 Microsoft 官方 Python 插件即可。

---

## 基础版本管理

### 安装多版本 Python

系统已将 Python 3.14 安装并写入系统 PATH，但某些框架（如 Flask）目前更适合 3.10–3.12 版本，因此需要额外安装 Python 3.12。此时注意两点：

1. 不要再添加进系统环境变量
2. 参考安装选项：

![安装选项 1](image/file-20260609163603242.png)
*只需要 pip 即可，其余都是多余的（已安装过 3.14）*

![安装选项 2](image/file-20260609163609280.png)
*推荐给所有用户安装，按图示配置即可*

### 创建虚拟环境

先检查已安装的 Python 版本：

```bash
py -0
```

应输出 3.14 和 3.12 两个版本。然后创建并激活虚拟环境：

```bash
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

最后安装依赖：

```bash
pip install flask
```

---

## 项目结构

推荐的项目目录结构：

```text
myproject/
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
├── tests/               # pytest 测试
│   └── test_xxx.py
└── src/                 # 核心源码
    └── myproject/
        ├── __init__.py  # 必须
        ├── main.py
        └── utils.py
```

### pyproject.toml 配置示例

```toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "myproject"
version = "0.1.0"
description = "Example project"
readme = "README.md"
requires-python = ">=3.11"

dependencies = [
    "requests>=2.32",
    "rich>=14.0"
]

[project.optional-dependencies]
dev = [
    "pytest",
    "ruff"
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.ruff]
line-length = 88
```

### 安装与开发

确保已有 `pyproject.toml` 和 `__init__.py`，然后以可编辑模式安装：

```bash
pip install -e ".[dev]"
```

Python 会将当前项目以 **editable 模式** 安装到当前虚拟环境中。之后修改 `src/` 中的代码会立即生效，无需重新执行 `pip install`。

### 基础检查

```bash
pytest             # 运行 tests/ 中的自动化测试
ruff check . --fix # 检查代码风格问题
ruff format .      # 统一代码格式
```

安装后，无论在哪个目录都可以通过以下方式导入项目代码：

```python
import myproject
from myproject import main
```

## 构建与发布

### 构建分发包

```bash
python -m build
```

会在 `dist/` 目录生成可分发的包文件。

### 发布到 PyPI

```bash
twine upload dist/*
```

---

## 常见问题

### PowerShell 脚本权限

Windows 的 PowerShell 默认没有执行脚本权限，导致无法自动激活虚拟环境。以管理员身份执行：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

选择 `Y` 确认，即可正常使用 venv 虚拟环境。

若要还原设置：

```powershell
Set-ExecutionPolicy -Scope CurrentUser Undefined
```
