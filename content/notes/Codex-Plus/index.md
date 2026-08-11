---
title: "Codex Plus订阅指南(ios)"
date: 2026-08-03
draft: false
description: "国内订阅 ChatGPT Plus 官方套餐（20 美元）流程：美区 Apple ID、美区礼品卡兑换、iOS 内购升级、Codex 登录"
slug: ""
aliases: []
weight: -1
tags: [chatgpt, agent, subscription]
categories: [tools, ai]
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

> 国内使用 Codex 目前大致有以下几种方法：
- 1. 购买官方订阅，从而大概率不会触发手机验证码（推荐）
- 2. 中转站接入 API，但是部分中转站模型可能掺水（次选）
- 3. 接手机验证码平台，风险极高，若触发二次验证时验证失败，GPT 账号就等于废了
- 4. 利用 Codex++ 或 CCswitch 接入国内 API，个人认为这会导致 Codex 能力锐减，还不如直接用国内 agent

> 另外，Codex 优先适配 macOS，因此有条件的话，使用 macOS 体验更佳。

> **本文内容专注于如何在国内订阅官方 Plus 套餐（20 美元）。**

> **本文具有时效性 最后更新日期:2026.8.3**

***

## 需要准备

- iOS 手机
- 美区 Apple ID
- 稳定科学上网环境
- 美区苹果虚拟礼品卡（20 美元）

***

## 官方充值 Plus 套餐

### Step1: 注册美区 Apple ID

参考教学视频：[B 站教学视频](https://www.bilibili.com/video/BV1zHtmzDEVY/)
![教程截取](image/b站教程.png)

***

### Step2: 在 App Store 登陆你的美区 ID

> 注意：千万不要在系统设置更改你的账号，新注册的 Apple 账号只用于登陆 App Store。

用美区账号登陆后方可下载 ChatGPT 手机端 App。

***

### Step3: 购买美区苹果礼品卡

比如微信小程序搜索 pockytshop。注意一定要买和你新注册 Apple ID 地区一致的礼品卡，否则无法使用（本文均选择美区）。
![pockytshop](image/wechat-pockyt.png)

获得礼品卡兑换码后，打开 App Store：
1. 登陆你的美区 Apple ID；
2. 输入兑换码兑换礼品卡额度；
3. 就可以直接通过苹果账号额度充值了。
![gitfcard](image/appstore-giftcard.png)

***

### Step4: 手机端 App 内充值

1. 打开 ChatGPT App，点击「升级 Plus」；
2. 点击小字「通过 Apple 升级」，然后就会弹出窗口确认；
3. 这里可能会再次弹出「地址无效」的提示，具体地址可以按照注册美区 Apple ID 时再照抄一遍，电话号码可以问 AI 随便填一个（这个不是用于绑定验证的号码，似乎只是要求你填写一个）。

***

### Step5: PC 端安装 Codex

安装好后直接用充值过 Plus 的账号登录即可；具备科学上网的前提下，这就不是问题了。

***

## 其他相关资源
- [Codex++](https://github.com/BigPizzaV3/CodexPlusPlus) - 帮助接入其他api
- [Codex auth Plugin](https://github.com/zhishile/codex-auth-helper) - 安全的登陆token获取插件(Free套餐无法使用work)

