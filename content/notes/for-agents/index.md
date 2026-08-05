---
title: "For Agents"
date: 2026-07-29
draft: false
description: "我常用的 AI Agent 工具配置分享 —— OpenCode、AGENTS.md、MCP、Skill 等"
slug: ""
aliases: []
weight: 0
tags: [agent, skills, mcp, opencode]
categories: [tools]
topics: []
series: []
showDateUpdated: true
dateUpdated: "2026-07-29"
images: []
showHero: true
heroStyle: "background"
showTableOfContents: true
showBreadcrumbs: true
showReadingTime: true
showWordCount: true
showZenMode: true
showRelatedContent: false
showComments: false
sharingLinks: []
---

> 记录自用的agent配置(keep updated)

***

## Skill

- [Vercel官网提供的skill管理工具](https://www.skills.sh/)
- [SkillHub](https://www.skillhub.cn/)


***

## MCP

- [Context7](https://context7.com/) - 给agent提供最新官方文档
- [Tavily](https://www.tavily.com/) - 让agent能够搜索网络信息
- [Playwright](https://playwright.dev/) - Web自动化
- [Shadcn](https://ui.shadcn.com/docs/mcp) - 提供前端组件库

***

## Setup

### OpenCode

以下是opencode配置文件,会不断更新,主要考虑了安全性,然后暂时只做了一些基础配置. 
<details>
<summary>自用的opencode.jsonc(点击展开)</summary>

```jsonc
{
  "$schema": "https://opencode.ai/config.json",//作用：为VScode等编辑工具提供自动补全和校验等 不影响opencode实际使用功能
  "autoupdate": true,
  "small_model": "deepseek/deepseek-v4-flash",
  "default_agent": "plan",//先明确需求再操作文件
  "permission": {
    "read": {
      "*":"allow",
      ".env":"deny",
      ".env/**":"deny",
      "/.env/api_keys.txt":"deny",
      ".env/keys.txt":"deny",
      ".env.example":"allow",
      "*.pem":"deny",
      "*.key":"deny",
      "keys/**":"deny"
    },
    "external_directory":"ask",//外部目录操作需要确认，自行审查命令
    "bash": {
      "*": "ask",
      "ls *": "allow",
      "wc *": "allow",
      "pwd": "allow",
      "echo *": "allow",
      "which *": "allow",
      "git status *": "allow",
      "git diff *": "allow",
      "git log *": "allow",
      "git show *": "allow",
      "git branch *": "allow",
      "npm test": "allow",
      "npm run lint": "allow",
      "npm run build": "allow",
      "pytest *": "allow",
      "go test *": "allow",
      "cargo test *": "allow",
      "rm -rf *": "deny",
      "rm -fr *": "deny",
      "sudo *": "deny",
      "curl * | *": "deny",
      "wget * | *": "deny"
    }
  },
  "plugin": [
    "opencode-supermemory",
    "@dietrichgebert/ponytail"
  ],
  "compaction": {
    "auto": true,
    "prune": true,
    "reserved": 10000
  },
  "watcher": {
    "ignore": ["node_modules/**", ".git/**", "dist/**", "build/**", "*.log", ".env/**", "keys/**"]
  },
  "lsp": true,
  "formatter": true,
  "shell": "zsh",//如果是windows环境，需要修改为powershell
  "agent": {
    "code-reviewer": {
      "description": "Reviews code for best practices and potential issues",
      "model": "deepseek/deepseek-v4-flash",
      "prompt": "You are a code reviewer. Focus on security, performance, and maintainability.",
      "permission": {
        "write": "deny",
        "edit": "deny"
      },
      "steps": 15
    },
    "build": {
      "permission": {
        "bash": {
          "*": "ask",
          "git status *": "allow",
          "git diff *": "allow",
          "git log *": "allow",
          "git show *": "allow",
          "git branch *": "allow",
          "git push *": "deny",
          "git reset --hard *": "deny"
        }
      }
    }
  },
  "command": {//自定义命令，重复性prompt
    "clear": {
      "template": "清理上述过程中临时产生并且没有用处的文件，停止因为临时测试而启动的本地服务.最后检查各个状态是否正常，若不正常，提醒我或者直接修复.最终目的是保持系统和项目环境干净!所以请不要产生其他负面影响!",
      "description": "try to keep your project and system clean",
      "agent": "build",
      "model": "deepseek/deepseek-v4-flash",
      "subtask": true
    },
    "cr": {
      "template": "用 code-reviewer 视角审视本次会话最近的改动（git diff 范围），重点：安全漏洞、性能问题、可维护性、可测试性。给出具体行号和建议，不要泛泛而谈。",
      "description": "Code-review on recent changes (renamed to avoid shadowing built-in /review)",
      "agent": "code-reviewer"
    },
    "test": {
      "template": "识别项目测试命令（查 package.json / pyproject.toml / go.mod / Cargo.toml 等），运行测试套件。如果失败，分析首个失败 case 的根因。",
      "description": "Run project test suite (auto-detect)",
      "agent": "build",
      "model": "deepseek/deepseek-v4-flash",
      "subtask": true
    }
  },
  "mcp": {//MCP配置
    "playwright": {
      "type": "local",
      "command": [
        "npx",
        "-y",
        "@playwright/mcp"
      ],
      "enabled": true,
      "environment": {
        "PLAYWRIGHT_MCP_HEADLESS": "true"
      }
    },
    "context7": {
      "type": "local",
      "command": [
        "npx",
        "-y",
        "@upstash/context7-mcp"
      ],
      "enabled": true,
      "environment": {
        "CONTEXT7_API_KEY": "{env:CONTEXT7_API_KEY}"
      }
    },
    "tavily": {
      "type": "local",
      "command": [
        "npx",
        "-y",
        "tavily-mcp"
      ],
      "enabled": true,
      "environment": {
        "TAVILY_API_KEY": "{env:TAVILY_API_KEY}"
      }
    }
  }
}
```

</details>

配置方式：

将 `opencode.jsonc` 放到项目根目录或OpenCode配置目录(~/.config/opencode/)即可生效：

```bash
# 项目级配置
cp opencode.jsonc /path/to/your/project/

# 全局配置（推荐）
mkdir -p ~/.config/opencode && cp opencode.jsonc ~/.config/opencode/
```

***

## AGENTS.md
