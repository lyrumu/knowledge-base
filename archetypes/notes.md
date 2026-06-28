---
# =============================================================================
# notes archetype
# 用法：
#   hugo new content/notes/<slug>/index.md
#
# 说明：
# - 适用于 notes 下的目录式文章（leaf bundle）
# - `notes/_index.md` 的 cascade 已统一兜底：
#   showTaxonomies / showEdit / showPagination / showViews / showLikes
# - `hugo.toml` 的 [params.article] 已兜底：
#   showHero / showBreadcrumbs / showTableOfContents / showReadingTime /
#   showWordCount / showZenMode / showRelatedContent 等常用展示开关
# - 因此这里只保留“每篇文章自己真正需要维护”的字段
# =============================================================================

# =============================================================================
# 基础信息（必填）
# =============================================================================
title: ""
date: {{ .Date }}
draft: true
description: ""

# =============================================================================
# URL 与权重
# - slug 留空 = 使用文件夹名
# - aliases 用于旧链接兼容，未来改路径时再补
# =============================================================================
slug: ""
aliases: []
weight: 0

# =============================================================================
# 分类与标签
# =============================================================================
tags: []
categories: []
topics: []
series: []

# =============================================================================
# 更新时间
# - 仅当你想显式展示“更新日期”时再开启
# =============================================================================
showDateUpdated: false
dateUpdated: ""

# =============================================================================
# Open Graph / SEO
# - 如果该文章有分享封面图，可填到 images
# - 若使用 page resources，优先让图片跟 index.md 放在一起
# =============================================================================
images: []

# =============================================================================
# 页面级覆写（按需打开；留空 = 使用 section / site 默认）
# =============================================================================
# showHero: true
# heroStyle: "background"
# heroBackground: ""
# heroImage: ""
# heroBackgroundImage: ""
# showTableOfContents: true
# showBreadcrumbs: true
# showReadingTime: true
# showWordCount: true
# showZenMode: true
# showRelatedContent: false
# relatedContentLimit: 3
# showComments: false
# sharingLinks: []
---

> 一句话概括这篇笔记写什么、适合谁看、解决什么问题。

## Overview

-
