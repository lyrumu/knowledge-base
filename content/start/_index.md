---
title: "Welcome"
subtitle: "Here is the index section"
description: "" 
layout: "page"
showHero: false
showBreadcrumbs: false
showTableOfContents: true
---

{{< modules-grid >}}

{{< section-rule >}}

> 📌 这是网站的大厅 — 上面四个模块卡对应顶部分类的四个入口。
> 想直接翻最近的文章？去分类页里看就行：[**学习笔记**](/notes/) · [**作品**](/works/) · [**生活**](/life/) · [**关于我**](/about/)

---

## 模板使用说明

- 改模块卡：编辑 [`data/modules.yaml`](https://github.com/)
- 改大厅文案：编辑 `content/start/_index.md`
- 想删模块：删 yaml + hugo.toml 里的 menu 即可