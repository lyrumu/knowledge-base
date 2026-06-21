---
title: "资源"
kicker: "WORKS · RESOURCES"
subtitle: " Maybe something useful that you can download"
description: ""
layout: "page"
showHero: true
showBreadcrumbs: true
showTableOfContents: true
---

> 维护方式
> 1. 准备资源文件：放到 `static/works-resources/<file>.zip`（mp3 / PDF / 字体…任意格式）
> 2. 准备封面图：放到 `static/image/works/resources/<slug>.png`（推荐 16:10）
> 3. 编辑 [data/resources.yaml](../../data/resources.yaml)，加一条：
>
>    ```yaml
>    - name: "资源名"
>      title: "English Subtitle"
>      desc: "衬线斜体描述"
>      cover: "/image/works/resources/<slug>.png"
>      file: "/works-resources/<file>.zip"   # 也支持外链 https://...
>      format: "ZIP"                          # 右上角徽章文本
>      size: "12 MB"                          # 手动写
>      tags: [tag1, tag2]
>      date: "2025-11"
>      source: "https://original.com"         # 可选：原始来源/致谢
>    ```
> **资源命名提醒**：用英文 / 数字，不要空格和中文（避免 URL 编码问题）
>
> 完整教程：[`PROJECT_MAP.md` §7](../../PROJECT_MAP.md)

> 免费下载，自用为主；如果对你也有用就更好。

{{< resources-list >}}

{{< section-rule >}}


---
