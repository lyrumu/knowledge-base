---
title: "AI Gateway, Free AI API & AI Applications"
source: "https://agnes-ai.com/doc/cid2#heading-%E4%BA%8C%E5%87%86%E5%A4%87%E5%B7%A5%E4%BD%9C"
author:
published:
created: 2026-06-12
description: "Agnes AI by Sapiens AI is an AI gateway, free AI API platform, and AI application ecosystem featuring Agnes, Echo, and Pavo. Get free AI API credits, create a free AI API key, use free AI API tokens, and access free AI API models for chatbots, AI agents, content tools, image generation, roleplay, productivity, and intelligent workflows. Build and use scalable generative AI across apps through one unified platform."
tags:
  - "clippings"
---
## HermesAgents 模型配置操作手册

### 一、概述

本文档介绍如何在 HermesAgents 中配置自定义模型服务商。配置完成后，HermesAgents 会将模型请求发送到指定的 API 地址，并使用对应模型完成 Agent 任务。

### 二、准备工作

开始配置前，请确保你已经具备以下条件：

1. 已在设备上安装 HermesAgents。
2. 已获得有效的 API Key。
3. 已确认 API 服务地址。
4. 已确认需要使用的模型名称。
5. 当前终端或命令行环境可正常使用。

### 三、打开终端

在本地设备中打开终端或命令行工具。

macOS 或 Linux 用户可以使用 Terminal。

Windows 用户可以使用 Command Prompt、PowerShell，或开发环境中的终端。

### 四、配置说明

HermesAgents 的配置命令格式通常为：

```bash
hermes config set <配置项> <值>
```

请注意， `set` 需要放在配置项前面。

### 五、配置模型服务商

执行以下命令：

```bash
hermes config set model.provider custom
```

该命令表示 HermesAgents 将使用自定义模型服务商，而不是默认内置服务商。

### 六、配置 API Base URL

执行以下命令：

```bash
hermes config set model.base_url https://apihub.agnes-ai.com/v1
```

该命令用于将 HermesAgents 的模型请求地址设置为 Agnes AI API Gateway。

通常 API Base URL 只需要填写到 `/v1` ，不需要手动添加 `/chat/completions` 。

推荐填写：

```
https://apihub.agnes-ai.com/v1
```

通常不建议填写：

```
https://apihub.agnes-ai.com/v1/chat/completions
```

除非 HermesAgents 明确要求输入完整接口地址。

### 七、配置 API Key

执行以下命令：

```bash
hermes config set model.api_key YOUR_API_KEY
```

请将 `YOUR_API_KEY` 替换为你的实际 API Key。

示例：

```bash
hermes config set model.api_key sk-xxxxxxxxxxxxxxxx
```

如果你希望通过环境变量方式配置 API Key，也可以使用：

```bash
hermes config set OPENAI_API_KEY YOUR_API_KEY
```

但在自定义模型服务商配置中，推荐优先使用：

```bash
hermes config set model.api_key YOUR_API_KEY
```

### 八、配置模型名称

执行以下命令：

```bash
hermes config set model.default agnes-2.0-flash
```

请使用平台提供的完整模型 ID。

模型 ID 通常区分大小写，建议直接复制平台提供的模型名称。

### 九、完整配置示例

```
Model Provider: custom
API Base URL: https://apihub.agnes-ai.com/v1
API Key: YOUR_API_KEY
Model Name: agnes-2.0-flash
```

### 十、完整命令示例

```bash
hermes config set model.provider custom
hermes config set model.base_url https://apihub.agnes-ai.com/v1
hermes config set model.api_key YOUR_API_KEY
hermes config set model.default agnes-2.0-flash
```

### 十一、验证配置

配置完成后，可以运行一个 HermesAgents 任务，或启动一次测试会话。

如果配置正确，HermesAgents 应能够正常调用指定 API 地址，并返回模型响应。

### 十二、常见问题排查

#### 1\. 鉴权失败

请检查 API Key 是否有效。

可以重新执行以下命令设置 API Key：

```bash
hermes config set model.api_key YOUR_API_KEY
```

同时确认账户余额或 credits 是否充足。

#### 2\. API 请求失败

请确认 API Base URL 是否正确：

```
https://apihub.agnes-ai.com/v1
```

通常不需要手动添加 `/chat/completions` 。

正确示例：

```
https://apihub.agnes-ai.com/v1
```

通常不建议填写：

```
https://apihub.agnes-ai.com/v1/chat/completions
```

除非 HermesAgents 明确要求输入完整接口地址。

#### 3\. 服务商未识别

请确认模型服务商已设置为：

```bash
hermes config set model.provider custom
```

#### 4\. 找不到模型

请检查模型名称是否正确。

推荐重新执行以下命令：

```bash
hermes config set model.default agnes-2.0-flash
```

模型 ID 通常区分大小写，建议直接复制平台提供的模型名称。

#### 5\. 网络错误

请确认当前设备可以访问 API 地址。

如果请求失败，请检查防火墙、代理或 VPN 设置。

### 十三、注意事项

HermesAgents 使用类似 OpenAI-Compatible 的配置方式。

对于自定义服务商，API Base URL 通常以 `/v1` 结尾。

推荐格式：

```
https://apihub.agnes-ai.com/v1
```

API Key 推荐通过 `model.api_key` 单独配置。

模型服务商应设置为：

```
custom
```

这样 HermesAgents 才会使用自定义 API 地址，而不是默认模型服务商。