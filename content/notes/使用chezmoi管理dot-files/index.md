---
title: "使用chezmoi管理dot-files"
date: 2026-08-11
draft: false
description: ""
slug: ""
aliases: []
weight: 0
tags: [tools, agent, os]
categories: [tools]
topics: []
series: []
showDateUpdated: false
dateUpdated: ""
images: []
showHero: true
heroStyle: "background"
heroBackground: ""
heroImage: ""
heroBackgroundImage: ""
showTableOfContents: true
showBreadcrumbs: true
showReadingTime: true
showWordCount: true
showZenMode: true
showRelatedContent: false
relatedContentLimit: 3
showComments: false
sharingLinks: []
---

> agent时代 用户目录下会产生很多以点开头的配置文件(下文统一称为dot-files)
> 
> 这些文件常常有重要价值 例如你的agents.md 以及各种记忆 skill/mcp配置
> 同时难以管理 因此用chezmoi这个工具进行备份 同时能够在不同设备间快速同步

- [**chezmoi官方docs**](https://www.chezmoi.io/) - 查看官方使用教程
(还在学习使用中 keep updated)

- **注意 如果你没有使用过git 建议先熟悉git的使用再学习chezmoi**

***
## 安装

### macOS

```zsh
brew install chezmoi && chezmoi --version
```

能输出版本就说明安装成功

```zsh
chezmoi init
```
然后chezmoi会在 `.loacal/share`生成一个名为chezmoi的本地git源仓库

***

## 使用

> chezmoi不仅能管理dot-files 普通文件也是可以管理的 但是建议只管理家目录下文件

> chezmoi管理本机实际配置文件和chezmoi源仓库文件的关系 
> 
> git管理chezmoi源本地仓库和github repo的关系

首先 判断家目录下哪些文件需要使用chezmoi管理
比如.agents .codex .claude等(注意 密钥不要通过chezmoi管理 除非使用加密)

然后就可以使用命令把配置文件拷贝进chezmoi本地源(不会改变你的设备的实际配置)
```zsh
chezmoi add ~/.zshrc 
chezmoi add ~/.zprofile
chezmoi add ~/.agents
chezmoi add ~/.codex/AGENTS.md
```

之后可以在自己的github新建仓库 将本地chezmoi仓库提交上去 日后用git管理

当本机实际配置文件发生改动或者更新 可以使用以下命令检查和同步chezmoi本地源
```zsh
chezmoi status #会显示本机实际配置文件和chezmoi本地源的差异
chezmoi diff #显示详细差异
chezmoi re-add #直接同步所有差异(更新chezmoi本地源)
chezmoi re-add ~/.zshrc #只更新某一个文件
```
